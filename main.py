import os
from dotenv import load_dotenv
from google import genai
import argparse

from google.genai import types

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("eweh")

prompt = args.user_prompt
verbose = args.verbose

client = genai.Client(api_key=api_key)
messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=messages,
)

if response.usage_metadata is None:
    raise RuntimeError("eweh")

if verbose:
    print(
        f"User prompt: {prompt}\n"
        f"Prompt tokens: {response.usage_metadata.prompt_token_count}\n"
        f"Response tokens: {response.usage_metadata.candidates_token_count}\n"
        f"Response:\n{response.text}"
    )
else:
    print(f"Response:\n{response.text}")
