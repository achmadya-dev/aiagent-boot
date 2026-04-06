import os
from dotenv import load_dotenv
from google import genai
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function
import sys
from google.genai import types

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("eweuh")

prompt = args.user_prompt
verbose = args.verbose

client = genai.Client(api_key=api_key)
messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

for _ in range(20):
    function_responses = []
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt, tools=[available_functions]
        ),
    )

    if response.usage_metadata is None:
        raise RuntimeError("eweuh")

    if response.candidates:
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

    if response.function_calls is not None and len(response.function_calls) > 0:
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose)

            if function_call_result.parts is None:
                raise Exception("Eweuh")

            if function_call_result.parts[0].function_response is None:
                raise Exception("Eweuh")

            if function_call_result.parts[0].function_response.response is None:
                raise Exception("Eweuh")

            if verbose is True:
                print(f"-> {function_call_result.parts[0].function_response.response}")

            function_responses.append(function_call_result.parts[0])

        messages.append(types.Content(role="user", parts=function_responses))
    else:
        print("Final response:")
        print(response.text)
        break
else:
    print("Maximum iterations reached")
    sys.exit(1)
