import os
from pathlib import Path

from dotenv import load_dotenv
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

# Reference: write a major to one student and return the updated fields.
# This uses the existing value so rerunning it keeps the workshop data consistent.
response = (
    supabase.table("students")
    .update({"major": "ethics"})
    .eq("id", 2)
    .select("name, major")
    .execute()
)
print("Write example:")
print(response.data)
# Expected: [{'name': 'mac', 'major': 'ethics'}]

# TODO: Find every student named "prad".
# Retrieve their name, email, and major, ordered by id.
# Print each record as a tuple: (name, email, major).
# Hint: access a specific field with row["email"].
print("Your query:")
