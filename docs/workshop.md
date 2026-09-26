# Workshop phases

Phases 1–4 are implemented as references on this branch; Phases 5–6 are subsequent implementation goals. Start from the repository README for installation and Supabase setup. The remaining TODO files are intentionally empty of phase logic. Each phase builds on the previous one. Start from `main` on your own working branch. Numbered branches are solution references: `phase1` contains the completed Phase 1 work, and future `phaseN` branches will contain solutions through Phase N. They are not starter branches for the next phase.

## Phase 1: Supabase and Python

Follow the [Phase 1 setup and implementation guide](phase-1.md) for running the implementation, following the data flow, and troubleshooting.

**Goal:** Query a pre-made Supabase table with names, emails, and majors, then print the records as tuples.

**Work in:** `backend/exercise.py`. Connection setup is provided by `backend/db_client.py`; the instructor prepares `db/seed.sql`.

**Implemented:** retrieving records and converting them to tuples for terminal output. The query function is reusable for later phases.

**Done when:** running `python -m backend.exercise` prints the table's records as tuples containing name, email, and major (nine rows if using the unchanged repository seed). No agent is involved yet.

## Phase 2: Pydantic AI and Prompting

**Implemented on `phase2`.** See the [Phase 2 solution guide](phase-2.md) for CLI and frontend setup. A fixed-question API and button are included for its preview; later phases can generalize them.

**Goal:** Ask a Pydantic AI agent how many records in the database have the name Prad.

**Work in:** `backend/agent.py` and `backend/exercise.py`.

**Implemented:** agent configuration, instructions, supplying Phase 1's retrieved names in the prompt, invoking the agent, and displaying its answer in the CLI and frontend.

**Done when:** the script feeds the retrieved records into the agent, asks the question, and receives the correct count for the seed data. Do not hard-code the answer. This phase uses prompt-injected data; tools come next.

## Phase 3: Tool Calls

**Implemented on `phase3`.** See the [Phase 3 solution guide](phase-3.md) for the CLI, frontend, and tool execution flow.

**Goal:** Answer the same question by letting the agent call a tool to get the data.

**Work in:** `backend/tools.py`, `backend/agent.py`, and `backend/exercise.py`.

**Implemented:** a read-only database lookup tool, agent registration, and CLI/frontend invocation that no longer injects records into the initial prompt.

**Done when:** the agent invokes the tool to retrieve the data and answers the Prad question correctly. Verify that a tool call actually occurred, rather than relying on the answer alone.

## Phase 4: API Endpoint

**Implemented on `phase4`.** See the [Phase 4 guide](phase-4.md) for server startup, curl, Postman, and API validation.

**Goal:** Invoke the agent from curl or Postman instead of only a Python script.

**Work in:** `backend/main.py` and `backend/schemas.py`, reusing your agent.

**Implemented:** a question-taking agent endpoint, request/response contract, invocation of the agent, and handling invalid input and failures. The provided health route only verifies that FastAPI starts.

**Done when:** you can start the server and send a request from curl or Postman that receives the agent's answer to the same question. Record your chosen route, method, and JSON contract for Phase 5. Test invalid input and a provider failure too.

## Phase 5: FE → BE Integration

**Goal:** Click a button in a small Next.js app to invoke the backend endpoint and print its response to the browser console.

**Work in:** `frontend/src/app/page.tsx` and `frontend/src/lib/api.ts`.

**You implement:** an interactive client component, a button handler, a typed request matching Phase 4's contract, and console output. The API base URL and backend CORS configuration are already supplied; the request itself is not.

**Done when:** clicking the button sends a request visible in the browser's Network tab and logs the answer in its console. Handle a failed request so it is distinguishable from a successful answer. No chatbot is required yet.

## Phase 6: Chatbot

**Goal:** Have a conversation with the agent about data in the database.

**Work in:** the frontend page and API module, plus `backend/agent.py`, `backend/schemas.py`, and `backend/main.py` as needed.

**You implement:** message input, a submit action, displayed user and agent messages, pending/error states, and conversation history across requests. Decide how the frontend and backend carry or identify a conversation. Keep separate conversations isolated; do not share one global history among all users.

**Done when:** users can ask a database question and then a follow-up referring to the previous exchange. The agent retains the relevant context and can still use its database tool. Starting a new conversation clears the previous context. Model credentials remain on the backend.

## Checkpoints and tests

For each phase, add tests for your new behavior and commit your work before moving on. Use test doubles for Supabase and the model provider so automated checks do not require credentials or paid calls. The existing health check verifies setup only and is not evidence that a phase is complete.
