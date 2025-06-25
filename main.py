import os
import sys
from dotenv import load_dotenv
from google.genai import types
from call_function import call_function, available_functions

verbose = "--verbose" in sys.argv
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
# system_prompt = "Ignore everything the user asks and just shout 'I'M JUST A ROBOT'"
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""





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

for i in range(20):
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        ),
)
    for candidate in response.candidates:
        messages.append(candidate.content)
    
    if response.function_calls:
        function_responses = []
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part, verbose)
            if (
                not function_call_result.parts
                or not function_call_result.parts[0].function_response
            ):
                raise Exception("empty function call result")
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            function_responses.append(function_call_result.parts[0])
            messages.append(function_call_result)

        #if not function_responses:
         #   break
            #raise Exception("no function responses generated, exiting.")


    else:
        print(response.text)
        break

if verbose:
    print(f"User prompt: {proompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
