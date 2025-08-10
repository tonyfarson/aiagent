import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.types import GenerationConfig
from prompts import system_prompt
from call_function import available_functions

def main():
    # Check for command-line argument
    if len(sys.argv) < 2:
        print("Error: No prompt provided. Usage: uv run main.py <prompt> [--verbose]")
        sys.exit(1)

    # Get the prompt and check for --verbose flag
    user_prompt = sys.argv[1]
    verbose = "--verbose" in sys.argv

    # Load environment variables
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not set in .env file")
        sys.exit(1)

    # Configure the GenAI SDK
    genai.configure(api_key=api_key)

    # Initialize the GenerativeModel with tools and system prompt
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        tools=[available_functions],
        system_instruction=system_prompt
    )

    # Print user prompt if verbose
    if verbose:
        print(f"User prompt: {user_prompt}")

    # Create messages list with user prompt
    messages = [
        {"role": "user", "parts": [{"text": user_prompt}]}
    ]

    # Call Gemini API
    response = model.generate_content(messages)

    # Check for function calls in the response
    if response.candidates and response.candidates[0].content.parts:
        candidate = response.candidates[0]
        for part in candidate.content.parts:
            if part.function_call:
                args_str = ", ".join([f"'{k}': '{v}'" for k, v in part.function_call.args.items()])
                print(f"Calling function: {part.function_call.name}({args_str})")
            else:
                print(part.text)

    # Print token usage if verbose
    if verbose and response.usage_metadata:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()