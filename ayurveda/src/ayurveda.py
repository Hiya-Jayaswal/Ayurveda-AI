import openai
from dotenv import load_dotenv
import time
import logging
from datetime import datetime
from keys.api_key import thread_id, assistant_id
# import re
# from fuzzywuzzy import fuzz


load_dotenv()

client = openai.OpenAI()
model = "gpt-3.5-turbo-16k-0613"
chat_history_file = "chat_history.txt"  # File to store conversation


def save_to_chat_history(message, response):
    """
    Saves the conversation between user and assistant to a text file.

    Args:
        message (str): User's message.
        response (str): Assistant's response.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(chat_history_file, "a") as f:
        f.write(f"\n** {timestamp} User: {message} \n")
        f.write(f"Assistant: {response} \n")

def answer_ayurvedic_questions(message):
    ayurvedic_keywords = [
        "Dosha assessment", "Ayurvedic questionnaire", "Dosha identification",
        "Pitta dosha", "Vata dosha", "Kapha dosha", "Ayurvedic lifestyle",
        "Ayurvedic diet plan", "Ayurvedic fitness regimen", "Dosha balancing techniques",
        "Ayurvedic herbs", "Ayurvedic practices", "Ayurvedic remedies", "Ayurvedic principles",
        "Ayurvedic wellness", "Ayurvedic consultation", "Dosha-specific recommendations",
        "Ayurvedic body type", "Ayurvedic health assessment", "Ayurvedic personalized plans"
    ]
    is_ayurvedic_related = any(keyword in message.lower() for keyword in ayurvedic_keywords)
    
    if is_ayurvedic_related:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-16k-0613", 
            prompt=message,
            temperature=1.3,
            max_tokens=200
        )
        return response.choices[0].text.strip()
    else:
        return "I'm sorry, I can only answer questions related to Ayurveda."

def send_message_and_get_response(message):
    """
    Sends a message to the assistant via OpenAI API and retrieves the response.

    Args:
        message (str): The message to be sent to the assistant.

    Returns:
        str: The assistant's response to the message.
    """

    num_dots = 0  # Track number of dots printed for waiting animation

    def print_waiting_message():
        nonlocal num_dots
        print("Waiting for response...", end="")
        for _ in range(num_dots):
            print(".", end="", flush=True)
        num_dots += 1  # Increment dots for next iteration

    print_waiting_message()  # Initial waiting message

    # Send the message to the thread
    message = client.beta.threads.messages.create(
        thread_id=thread_id, role="user", content=message
    )

    # Start a run of the assistant
    # dataset directions
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions="You are hiya, (gender = female)! an Ayurvedic doctor. Provide a diagnosis and treatment plan for the patient."
    )

    # Wait for the run to complete and retrieve the response
    response = wait_for_run_completion(client, thread_id, run.id)

    # Clear waiting message and newline after receiving response
    print("\r" + (" " * len("Waiting for response...")), end="", flush=True)
    response = answer_ayurvedic_questions(message)

    # Save conversation to chat history
    save_to_chat_history(message.content, response)

    return response


def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
    """
    Wait for a run to complete and print the elapsed time.
    Args:
        client: OpenAI client instance
        thread_id: The ID of the thread whose run is associated with model
        run_id: The ID of the run
        sleep_interval: The time in seconds to wait between checks

    Returns:
        str: The assistant's response to the message
    """

    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.completed_at:
                elapsed_time = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime(
                    "%H:%M:%S", time.gmtime(elapsed_time)
                )
                logging.info(f"Run completed in {formatted_elapsed_time}")

                # Get messages and return the assistant's response
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                return response
            

        except Exception as e:
            logging.error(
                f"An error occurred while retrieving data from the server: {e}"
            )

        print("", end="", flush=True)  # Print a dot for continuous waiting
        time.sleep(sleep_interval)




# loop for continuous conversation, type 'quit' to exit
while True:
    message = input("\nEnter your message (or type 'quit' to exit): ")
    
    trimmed_message = message.lower().strip()
    if trimmed_message == "quit":
        break

    response = send_message_and_get_response(message)
    print(f"\nAssistant Response: {response}")  
    
    break

    response = send_message_and_get_response(message)
    print(f"\nAssistant Response: {response}")
    print(f"\nAssistant Response: {response}")