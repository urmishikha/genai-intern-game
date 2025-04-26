# What Beats Rock? - AI Game

A simple game where you try to find words that "beat" the current word, with AI judging your answers.

## Setup

1. Clone this repository
2. Create a `.env` file with your OpenAI API key:
3. AI_API_KEY=your_openai_api_key

3. Run `docker-compose up` to start the services

## How to Play

1. The game starts with the word "Rock"
2. Enter something you think "beats" the current word
3. The AI will judge if your answer is valid
4. If correct, your answer becomes the new word to beat
5. Try to get the highest score without repeating any words!

## Features

- AI-powered word validation
- Session-based gameplay
- Global word count tracking
- Redis caching for AI responses
- Simple but polished frontend
- Multiple host personas

## Architecture

- **Backend**: FastAPI (Python)
- **Database**: SQLite (with Redis for caching)
- **Frontend**: Vanilla JS with minimal CSS
- **AI**: OpenAI GPT-3.5-turbo
How to Run the Application

Make sure you have Docker installed on your Mac
Create a .env file with your OpenAI API key:
AI_API_KEY=your_openai_key_here
Run the application:
bash
docker-compose up --build
Open your browser to http://localhost:8000
The game should now be running with:

Backend API on port 8000
Redis for caching
SQLite database for persistence
Frontend served by FastAPI
The implementation includes all required features:

Core game logic with linked list tracking
AI integration with caching
Global guess counter
Profanity filtering
Multiple host personas
Docker deployment
Minimal but functional frontend