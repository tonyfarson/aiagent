import os
from dotenv import load_dotenv
from google import genai

def main():
    # Load environment variables
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not set in .env file")
        return

    # Initialize Gemini client
    client = genai.Client(api_key=api_key)

    # Call Gemini API
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    )

    # Print response text
    print(response.text)

    # Print token usage
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()