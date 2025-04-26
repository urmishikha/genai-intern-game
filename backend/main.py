import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import os
from backend.core.game_logic import GameSession
from backend.core.ai_client import AIClient
from backend.core.cache import RedisCache
from backend.core.moderation import Moderation
from backend.db.models import init_db, get_db

app = FastAPI()

# Serve frontend files
app.mount("/static", StaticFiles(directory="frontend"), name="static")
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
ai_client = AIClient(os.getenv("AI_API_KEY"))
cache = RedisCache(os.getenv("REDIS_URL", "redis://localhost:6379"))
moderator = Moderation()
db = get_db()

# Initialize database
init_db()

class GuessRequest(BaseModel):
    word: str
    guess: str
    persona: Optional[str] = "serious"

@app.post("/api/guess")
async def make_guess(guess_req: GuessRequest, request: Request):
    ip = request.client.host
    session_id = f"{ip}-session"

    # Check for profanity
    if moderator.has_profanity(guess_req.guess):
        raise HTTPException(status_code=400, detail="Inappropriate content detected")

    # Get or create game session
    game_session = GameSession.get_or_create(session_id, guess_req.word, db)

    # Check if guess already exists in session
    if game_session.has_guess(guess_req.guess):
        return {"status": "game_over", "message": "This guess was already made!"}

    # Check cache first
    cache_key = f"{guess_req.word}:{guess_req.guess}"
    cached_result = cache.get(cache_key)

    if cached_result is None:
        # Ask AI if the guess beats the word
        ai_response = ai_client.ask(
            f"Does '{guess_req.guess}' beat '{guess_req.word}' in a game context? "
            f"Respond with only YES or NO."
        )
        cached_result = ai_response.strip().upper() == "YES"
        cache.set(cache_key, cached_result)

    if cached_result:
        # Update game state
        game_session.add_guess(guess_req.guess)
        global_count = db.increment_global_count(guess_req.guess)

        return {
            "status": "success",
            "message": f"Nice! '{guess_req.guess}' beats '{guess_req.word}'",
            "previous_guesses": game_session.get_previous_guesses_count(guess_req.guess),
            "global_count": global_count,
            "score": game_session.score,
            "history": game_session.get_history()
        }
    else:
        return {
            "status": "fail",
            "message": f"Nope! '{guess_req.guess}' doesn't beat '{guess_req.word}'"
        }

@app.get("/api/history")
async def get_history(request: Request):
    ip = request.client.host
    session_id = f"{ip}-session"
    game_session = GameSession.get(session_id)
    if not game_session:
        return {"history": []}
    return {"history": game_session.get_history()}

@app.get("/api/test")
async def test():
    return {"message": "API is working"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)