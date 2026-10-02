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
