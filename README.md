# Take That Engine
This is a game engine for the 'Take That' card game.

## Installation

First, set up a virtual environment using:

    python3 -m venv .venv

On macOS and Linux, run:

    . .venv/bin/activate

On Windows, run:

    .\.venv\Scripts\activate

To activate your virtual environment.

Next, to install required packages run:

    pip install -r requirements.txt

## Setup
Create a `.env` file and set the following environment variables:
- `CORS_ORIGINS`
  Allowed CORS hosts
- `SECRET_KEY`
  HS256 key used to encode JWT tokens.

## Execution

To execute, first activate your virtual environment (see above).

Then run:

    uvicorn app.main:app --reload

The engine is now running under http://localhost:8000