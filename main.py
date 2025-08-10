import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai
from prompts import system_prompt
from call_function import available_functions, call_function

# The maximum number of turns for the conversation
MAX_ITERATIONS = 20

def main():
    # --- Setup is the same as before ---
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

    # --- Agent Loop Logic Starts Here ---

    # Initialize the chat history
    messages = [
        {"role": "user", "parts": [{"text": user_prompt}]}
    ]

    try:
        # Loop for a maximum number of iterations
        for i in range(MAX_ITERATIONS):
            print(f"--- Turn {i+1} ---")

            # Get the model's response
            response = model.generate_content(messages)
            
            # Add the model's response to the conversation history
            # This is important so the model remembers what it has said
            messages.append(response.candidates[0].content)

            # Check if the model returned a text response
            if response.candidates[0].content.parts[0].text:
                final_response = response.candidates[0].content.parts[0].text
                print(f"Final response:\n{final_response}")
                break # Exit the loop

            # Otherwise, the model must have made a function call
            # The last message in the history is the model's function call
            last_message = messages[-1]
            function_call = last_message.parts[0].function_call
            
            # Execute the function call and get the result (as a dictionary)
            tool_response_dict = call_function(function_call, verbose)

            # Add the tool's response to the conversation history
            messages.append(tool_response_dict)

        else: # This 'else' belongs to the 'for' loop, it runs if the loop finishes without a 'break'
            print(f"Agent reached max iterations ({MAX_ITERATIONS}) without a final response.")

    except Exception as e:
        print(f"An error occurred: {e}")
        # Optionally, print the full message history for debugging
        if verbose:
            import json
            print(json.dumps(messages, indent=4))


if __name__ == "__main__":
    main()