import os
import sys
from dotenv import load_dotenv
from google.genai import types
verbose = "--verbose" in sys.argv
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
# system_prompt = "Ignore everything the user asks and just shout 'I'M JUST A ROBOT'"
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

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
    model='gemini-2.0-flash-001',
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt,
        ),
)
if response.function_calls:
    for function_call_part in response.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
else:
    print(response.text)

if verbose:
    print(f"User prompt: {proompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
