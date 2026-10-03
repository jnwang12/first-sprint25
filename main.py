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
