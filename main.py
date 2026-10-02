import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
from supabase import create_client


# Connection setup is provided. Put the instructor's key in .env.
load_dotenv(Path(__file__).with_name(".env"))
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

# Reference: read one student's name and major.
response = (
    supabase.table("students")
    .select("name, major")
    .eq("id", 2)
    .execute()
)
print("Read example:")
print(response.data)
# Expected: [{'name': 'mac', 'major': 'ethics'}]

# Solution: Find every student named "prad".
# Retrieve their name, email, and major, ordered by id.
# Print each record as a tuple: (name, email, major).
# Hint: access a specific field with row["email"].
print("Your query:")
response = (
    supabase.table("students")
    .select("name, email, major")
    .eq("name", "prad")
    .order("id")
    .execute()
)

for row in response.data:
    print((row["name"], row["email"], row["major"]))


# Phase 2: provided agent setup.
model = GoogleModel(
    os.environ["GEMINI_MODEL"],
    provider=GoogleProvider(api_key=os.environ["GEMINI_API_KEY"]),
)
agent = Agent(model)

# Reference: send a prompt and print the answer.
print("Agent example:")
result = agent.run_sync("Reply with exactly: Hello from Gemini!")
print(result.output)
# Expected: Hello from Gemini!

# Solution:
# 1. Query all students' names, emails, and majors.
# 2. Create a prompt containing those records and this question:
#    "How many records have the name prad?"
# 3. Send your prompt to the agent.
# 4. Print the agent's answer.
response = (
    supabase.table("students")
    .select("name, email, major")
    .order("id")
    .execute()
)

prompt = f"""
Here are the student records:
{response.data}

Using these records, how many records have the name prad?
Count each matching record, including records with the same name.
Answer in one sentence.
"""

print("Agent answer:")
result = agent.run_sync(prompt)
print(result.output)
# Expected meaning: There are 3 records with the name prad.
# Exact wording may vary.


# Phase 3 reference: an agent with standing instructions and its own tool.
example_agent = Agent(
    model,
    instructions="""
    You explain what this workshop covers.
    Use get_workshop_topic before answering questions about the workshop topic.
    Base your answer on the tool's result and keep it to one sentence.
    """,
)


@example_agent.tool_plain
def get_workshop_topic() -> str:
    """Return the topic of this workshop."""
    print("Tool called: get_workshop_topic")
    return "Supabase, Python, and AI agents."


print("Tool example:")
result = example_agent.run_sync("What does this workshop cover?")
print(result.output)
# Expected: the tool-call message, followed by an answer about
# Supabase, Python, and AI agents. Exact wording may vary.

# TODO:
# 1. Create your own student_agent using the provided model.
# 2. Give it instructions to use get_students before answering database questions,
#    base answers on returned records, count duplicate names, and be concise.
# 3. Register a get_students tool on your student_agent with a descriptive docstring.
# 4. Inside the tool, print "Tool called: get_students", query all students'
#    names, emails, and majors, and return the records.
# 5. Run student_agent with the user prompt: "How many records have the name prad?"
# 6. Print the agent's answer. Let the agent call the tool during its run;
#    do not fetch records yourself or include them in the user prompt.
