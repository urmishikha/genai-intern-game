from typing import Optional, Dict, List
import uuid
from backend.db.models import get_db


class GameSession:
    _sessions: Dict[str, 'GameSession'] = {}

    def __init__(self, session_id: str, seed_word: str, db):
        self.session_id = session_id
        self.seed_word = seed_word
        self.guesses = []
        self.score = 0
        self.db = db

    @classmethod
    def get_or_create(cls, session_id: str, seed_word: str, db) -> 'GameSession':
        if session_id not in cls._sessions:
            cls._sessions[session_id] = GameSession(session_id, seed_word, db)
        return cls._sessions[session_id]

    @classmethod
    def get(cls, session_id: str) -> Optional['GameSession']:
        return cls._sessions.get(session_id)

    def has_guess(self, guess: str) -> bool:
        return guess in self.guesses

    def add_guess(self, guess: str):
        self.guesses.append(guess)
        self.score += 1

    def get_history(self) -> List[str]:
        return self.guesses.copy()

    def get_previous_guesses_count(self, guess: str) -> int:
        return self.guesses.count(guess)