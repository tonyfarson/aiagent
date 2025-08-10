import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai
from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    if len(sys.argv) < 2:
        print("Error: No prompt provided. Usage: uv run main.py <prompt> [--verbose]")
        sys.exit(1)

    user_prompt = sys.argv[1]
    verbose = "--verbose" in sys.argv

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not set in .env file")
        sys.exit(1)

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        tools=[available_functions],
        system_instruction=system_prompt
    )

    if verbose:
        print(f"User prompt: {user_prompt}")

    messages = [
        {"role": "user", "parts": [{"text": user_prompt}]}
    ]

    response = model.generate_content(messages)

    if response.candidates and response.candidates[0].content.parts:
        candidate = response.candidates[0]
        for part in candidate.content.parts:
            if part.function_call:
                # call_function now returns a dictionary
                function_call_result_dict = call_function(part.function_call, verbose)

                # Validate and print using dictionary key access
                if not function_call_result_dict['parts'][0]['function_response']['response']:
                    raise Exception("Fatal error: Function call did not return a response.")

                if verbose:
                    print(f"-> {function_call_result_dict['parts'][0]['function_response']['response']}")

            elif part.text:
                print(part.text)

    if verbose and response.usage_metadata:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()