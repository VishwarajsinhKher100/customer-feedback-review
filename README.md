# Customer Feedback Review

A small web app for analyzing customer reviews. Paste one review per line to
classify its sentiment, assign a score, and identify its main topic. The app
also summarizes results and can save them to a local SQLite database.

## Features

- Analyze reviews with Groq using LangChain's `ChatGroq` integration.
- Return a sentiment label (`positive`, `negative`, or `neutral`), a score
  from 1 to 5, and a one-word lowercase theme.
- View the results, average score, positive-review percentage, and most common
  theme in a Streamlit interface.
- Save and view analysis history in `feedback.db`.

## Requirements

- Python 3.12 or later
- [uv](https://docs.astral.sh/uv/)
- A Groq API key

## Setup

From the project root, install the project dependencies:

```powershell
uv sync
```

Create a `.env` file in the project root and add your Groq API key:

```dotenv
GROQ_API_KEY=your_groq_api_key
```

Keep the `.env` file private; do not commit your API key.

## Run the application

Start the API in one terminal:

```powershell
uv run uvicorn customer_feedback_review.api:app --reload
```

Start the Streamlit app in another terminal:

```powershell
uv run streamlit run src/customer_feedback_review/app.py
```

Open the local URL printed by Streamlit. The interface sends analysis requests
to the API at `http://127.0.0.1:8000/analyze`. The API documentation is
available at `http://127.0.0.1:8000/docs`.

## API

`POST /analyze` accepts one review:

```json
{
  "text": "The delivery was quick and the food was excellent."
}
```

It returns a structured analysis, for example:

```json
{
  "label": "positive",
  "score": 5,
  "theme": "delivery"
}
```

The score must be between 1 and 5, and the theme must be one lowercase word.

## Data storage

Saved results are stored in the SQLite database `feedback.db`, created in the
working directory when the Streamlit app starts. Use **Save to database** in
the app to add the current results to history.

## Project layout

```text
src/customer_feedback_review/
├── api.py       # FastAPI endpoint and Groq review analysis
├── app.py       # Streamlit user interface
├── database.py  # SQLite initialization and history functions
└── __init__.py  # Package entry point
```
