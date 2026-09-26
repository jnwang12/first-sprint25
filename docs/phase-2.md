# Phase 2 solution: Pydantic AI and Prompting

This branch builds on Phase 1. It retrieves student records with the existing Python query, inserts their names into a prompt, and asks a Pydantic AI agent:

> How many records in the database have a name of Prad?

There are no registered database tools. The records are fetched before the model runs; moving retrieval into a tool is Phase 3.

## Configure and run

Set these in `backend/.env`, alongside your existing Supabase settings:

```dotenv
GEMINI_API_KEY=your-provider-key
GEMINI_MODEL=gemini-3.1-flash-lite
```

`GEMINI_MODEL` is optional and defaults to `gemini-3.1-flash-lite`. Use a Gemini model available to your account. `GOOGLE_API_KEY` is also accepted and takes precedence if both key variables are set. Keep the key on the backend, and restart the backend after changing its environment. Each agent invocation makes a model request and can incur provider charges.

From the repository root with `.venv` activated:

```bash
python -m backend.agent
```

The Phase 1 command `python -m backend.exercise` still prints tuples without invoking a model.

## Frontend

Run these in separate terminals:

```bash
# Repository root, Python environment activated
python -m uvicorn backend.main:app --reload --port 8000
```

```bash
cd frontend
npm run dev
```

Open `http://localhost:3000` and click **Ask about Prad**. The student tuples remain visible below the agent panel. No model call is made just by loading the page.

The button calls `POST /api/agent/prad`. This fixed-question endpoint is provided now to support the requested frontend preview; later API and frontend exercises can generalize it. It is not a conversational chatbot.

```bash
curl -X POST http://localhost:8000/api/agent/prad
```

The response contains `question`, `answer`, and `records_analyzed`. The latter describes the freshly retrieved snapshot, which can differ from the directory if the database changed since that view loaded.

## Follow the implementation

1. `backend/exercise.py` retrieves the table records.
2. `backend/agent.py` builds JSON containing one name per record. Emails and majors are unnecessary for this question and are not sent to the model.
3. Agent instructions require complete-name matching, ignoring capitalization and surrounding whitespace. Thus `prad` matches `Prad`, while `Pradeep` does not. Duplicate names count as separate records.
4. Pydantic AI runs the model with that prompt and returns plain text. No count is hard-coded or calculated in Python.
5. FastAPI returns the answer; the frontend displays it as text with loading and error states.

The model is asked to count, so an answer is not a mathematically verified database aggregation. Compare it with the live records when evaluating your prompt. Empty data is passed as an empty list. Database errors are kept separate from empty results. The query uses Supabase's response-size limit and is intended for this small workshop dataset; larger tables require pagination and a prompt-size strategy.

Missing provider configuration returns `503`, database failures return `503`, model failures return `502`, and a model run exceeding 45 seconds returns `504`. Each run permits one model request. The local preview has no authentication or rate limiting; add these before public deployment.

## Tests

```bash
python -m pytest -q
```

The agent tests run the real Pydantic AI pipeline with a local `FunctionModel`. They verify prompt data, instruction delivery, plain-text output, and absence of tools. API tests cover the returned answer, missing configuration, and provider failures. These tests do not establish a live model's counting accuracy and need no provider key.

[Official Pydantic AI agent guide](https://pydantic.dev/docs/ai/core-concepts/agent/)
