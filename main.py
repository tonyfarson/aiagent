import os
import sys
from dotenv import load_dotenv
from google import genai

def main():
    # Check for command-line argument
    if len(sys.argv) < 2:
        print("Error: No prompt provided. Usage: uv run main.py <prompt>")
        sys.exit(1)

    # Get the prompt from command-line arguments
    prompt = sys.argv[1]

    # Load environment variables
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not set in .env file")
        sys.exit(1)

    # Initialize Gemini client
    client = genai.Client(api_key=api_key)

    # Call Gemini API
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=prompt
    )

    # Print response text
    print(response.text)

    # Print token usage
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()