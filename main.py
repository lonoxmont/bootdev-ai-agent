import os
import sys
from dotenv import load_dotenv
verbose = "--verbose" in sys.argv
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

from google import genai

client = genai.Client(api_key=api_key)
args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
if not args:
    print("you need to give me a proompt, dumpass! usage: main.py prompt [--verbose]")
    sys.exit(1)
proompt = " ".join(args)
from google.genai import types
messages = [
    types.Content(role="user", parts=[types.Part(text=proompt)])
]


response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=messages
)
print(response.text)
if verbose:
    print(f"User prompt: {proompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
