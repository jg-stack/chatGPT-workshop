from openai_functions import run_and_print_messages, create_assistant, create_thread, upload_file
import time

ASSISTANT_NAME = "Kramp Assistant"
INSTRUCTIONS = "You will be given a question about a product. Answer the question as if you were a customer service representative. \
                If you don't know the answer, you can say 'I don't know' or 'I will find out and get back to you'. \
                Answer every question in french."

# Upload a file
file = upload_file("Annual_Report_2022_UK.pdf")

# Create an assistant
assistant = create_assistant(
    name=ASSISTANT_NAME,
    instructions=INSTRUCTIONS,
    model="gpt-4-1106-preview",
    tools=[{"type": "retrieval"}],
    file_ids=[file.id] 
)

# Create a thread
thread = create_thread()

# Initial query
initial_query = "What were the biggest project for the company in 2022?"
run_and_print_messages(thread.id, assistant.id, initial_query)

# Ask user if they want to add a message
while True:
    add_message = input("Do you want to add a message? (y/n): ").lower()
    if add_message == "y":
        message_content = input("Enter your message: ")
        run_and_print_messages(thread.id, assistant.id, message_content)
    elif add_message == "n":
        print("No message added, exiting...")
        break
    else:
        print("Invalid input. Please enter 'y' or 'n'.")