# Phase 3 solution: Tool Calls

This branch starts from `phase2` and replaces prompt-injected records with a read-only Pydantic AI tool. The CLI and frontend still ask how many records have the name Prad.

## Run

Keep your existing Supabase and Gemini settings in `backend/.env`. The agent accepts `GEMINI_API_KEY` or `GOOGLE_API_KEY` (the latter takes precedence), plus optional `GEMINI_MODEL`.

From the repository root with `.venv` activated:

```bash
python -m backend.agent
```

For the frontend, run FastAPI and Next.js in separate terminals:

```bash
python -m uvicorn backend.main:app --reload --port 8000
```

```bash
cd frontend
npm run dev
```

Open `http://localhost:3000` and click **Ask about Prad**. The answer panel includes the number of successful database tool calls and records retrieved. Each click starts an independent run and can incur model usage charges.

## What changed from Phase 2

| Phase 2 | Phase 3 |
| --- | --- |
| Python queries before invoking the model | The model requests a registered lookup tool |
| Initial prompt includes the names as JSON | Initial prompt contains only the question |
| Model answers in one request | Model calls the tool, receives its result, then answers |
| No tool execution requirement | Output validation rejects answers without a successful tool call |

The model still receives database data, but as a tool result rather than data preloaded into the user prompt. Emails and majors are excluded from the tool result because only names are needed for this question.

## Follow the flow

1. `backend/agent.py` creates a Gemini agent and registers `get_student_names`.
2. Each run gets its own `StudentTools` dependencies. These contain a callable and run metadata, not retrieved records.
3. The agent receives the question and chooses the lookup tool.
4. `backend/tools.py` executes the Phase 1 read query in a worker thread, returns one name per record, and records the lookup metadata.
5. The model counts the names from the tool result and returns its answer. Matching ignores case and surrounding whitespace; duplicate names remain separate records.
6. The output validator checks that a successful lookup occurred. If the model skips it, it gets a retry instruction rather than returning an unsupported answer.
7. FastAPI returns `question`, `answer`, `records_analyzed`, and `tool_calls`. The frontend displays the answer and lookup metadata.

There is no hard-coded count, arbitrary SQL tool, write access, or conversation memory. The Phase 1 tuple view remains separate and does not supply data to the agent. Tool metadata is recorded by Python, not claimed by the model.

## Limits and failures

Runs allow up to three model requests, two tool calls, one validation retry, and a 45-second deadline. Normally two model requests suffice: tool selection and the final answer. A retry allows correction if the model initially skips the tool. Persistent refusal is an error.

A failed database lookup is not treated as zero records. The API returns `503` for lookup or setup failures, `504` for timeouts, and `502` for provider/agent failures. The tool uses the same small-table Supabase query as Phase 1; larger datasets need pagination. The model's count is not a mathematically verified aggregation.

This is a local workshop preview. Authentication and rate limiting are still required before public deployment.

## Verification

```bash
python -m pytest -q
```

Offline `FunctionModel` tests drive the real Pydantic AI tool loop. They verify that the loader has not run before the tool call, no records appear in the initial prompt, duplicate names survive, empty results work, lookup failures propagate, and a missing tool call triggers a retry or rejection. Tests also cover API errors and frontend response metadata.

Compare `phase2` and `phase3` to see prompting versus tool retrieval. The earlier [Phase 2 guide](phase-2.md) describes the implementation on the `phase2` branch.

[Official Pydantic AI tool guide](https://pydantic.dev/docs/ai/tools-toolsets/tools/)
