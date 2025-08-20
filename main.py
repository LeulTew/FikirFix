import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")


def main():
    # Read prompt from command line arguments. Support an optional --verbose flag
    # supplied after the prompt: `uv run main.py "ask me" --verbose`
    args = sys.argv[1:]
    verbose = False
    if args and args[-1] == "--verbose":
        verbose = True
        args = args[:-1]

    if not args:
        print('Error: missing prompt argument. Usage: uv run main.py "your prompt here" [--verbose]')
        sys.exit(1)

    prompt = " ".join(args)

    # Wrap the user's prompt in a list of types.Content so we can extend
    # the conversation later (assistant/system messages, etc.).
    user_prompt = prompt
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    if not api_key:
        print("GEMINI_API_KEY not found in environment. Create a .env with GEMINI_API_KEY=\"your_key\"")
        return

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )

    # Print the model's text response
    print(response.text)

    # If verbose, print extra debug info: the user's prompt and token counts
    if verbose:
        print(f"User prompt: {user_prompt}")
        usage = getattr(response, "usage_metadata", None)
        prompt_tokens = getattr(usage, "prompt_token_count", "unknown")
        response_tokens = getattr(usage, "candidates_token_count", "unknown")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")


if __name__ == "__main__":
    main()
