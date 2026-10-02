# Phase 3: Build an agent with a tool

Create an agent with standing instructions and a Python function it can call.
The user supplies a question; the agent requests the tool and uses the returned
data to answer. All code stays in `main.py`.

## Setup

Use your Phase 2 environment and `.env`. No new dependencies or keys are needed.

```bash
source .venv/bin/activate
python main.py
```

For a fresh checkout, use Python 3.11 or newer:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Fill in `SUPABASE_KEY` and `GEMINI_API_KEY` in `.env`. The workshop Supabase URL and
Gemini model name are already supplied. Use a model available to your account.
Get a Gemini key from [Google AI Studio](https://aistudio.google.com/apikey).
Keep `.env` out of Git.

On Windows PowerShell, use `py -m venv .venv`, activate with
`.venv\Scripts\Activate.ps1`, and copy with `Copy-Item .env.example .env`.

## What is already provided

- The completed Phase 1 read queries and tuple output.
- The completed Phase 2 greeting and database prompt.
- The existing Supabase client and Gemini model configuration.
- A Phase 3 reference agent with its own instructions and tool.

The earlier phases run first when you run `main.py`. The new reference begins at
`Tool example:`. Each agent run starts fresh; earlier answers are not automatically
passed in as conversation history. Model calls use your provider quota and may
incur charges.

## Walk through the reference

`example_agent` has three separate pieces:

1. **Standing instructions:** `instructions` sets its role and tells it to use
   `get_workshop_topic` before answering a question about the workshop topic.
2. **Tool:** `@example_agent.tool_plain` registers a Python function. Its docstring
   describes what it returns. It prints a message when called and returns the topic.
3. **User prompt:** `example_agent.run_sync("What does this workshop cover?")`
   supplies only the user's question.

Gemini requests the tool, Pydantic AI runs the function locally, and its return
value goes back to Gemini so it can compose the answer.

Expected reference output (answer wording may vary):

```text
Tool example:
Tool called: get_workshop_topic
This workshop covers Supabase, Python, and AI agents.
```

The tool-call message shows that the function actually ran. A plausible answer
alone does not demonstrate tool use.

## Your task

Complete the TODO at the bottom of `main.py`:

1. Create a separate `student_agent` using the provided `model`.
2. Give it standing instructions to use `get_students` before answering database
   questions, answer from the returned records, count records individually even
   when names repeat, and keep answers concise.
3. Register your own `get_students` tool on that agent. Add a docstring explaining
   what it returns.
4. Inside the tool, print `Tool called: get_students`, query all students' names,
   emails, and majors from Supabase, and return the records.
5. Run your agent with the user prompt: `How many records have the name prad?`
6. Print the returned answer.

The tool should retrieve all students, including those whose name is not `prad`.
Let the agent request the tool during its run. Keep database records and tool-use
instructions out of the user question. Reuse the Supabase query pattern from
Phase 2 inside your tool.

Expected solution output after the reference example (answer wording may vary):

```text
Student agent answer:
Tool called: get_students
There are 3 records with the name prad.
```

The count assumes the existing workshop table is unchanged. Confirm both that your
tool ran and that the answer matches the database. If no tool-call message appears,
check your tool registration, docstring, and agent instructions.

## Branches

```text
phase-2-solution
└── phase-3-base
    └── phase-3-solution
```

- `phase-3-base`: previous solutions, a complete sample agent and tool, and the TODO.
- `phase-3-solution`: the same files with the student agent and tool implemented.

## Database access

Use the existing `public.students` table with `id`, `name`, `email`, and `major`.
The workshop key needs SELECT access to the sample records. All queries are reads.
If a query returns `[]` unexpectedly, check the project, filters, and read policies.

## References

- [Agent instructions and user prompts](https://ai.pydantic.dev/agents/)
- [Function tools](https://ai.pydantic.dev/tools/)
- [Supabase read queries](https://supabase.com/docs/reference/python/select)
