from openai_functions import create_assistant, create_thread, upload_file, create_message, create_run, retrieve_run_status, list_messages, print_messages
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

# Create a message in the thread
message = create_message(
    thread_id=thread.id,
    role="user",
    # Replace the content with your own question / task to the assistant
    content="What were the biggest project for the company in 2022?"
)

# Create a run on the thread
run = create_run(
    thread_id=thread.id,
    assistant_id=assistant.id
)

# Wait for the run to complete
while True:
    # Retrieve the latest status of the run
    run_status = retrieve_run_status(
        thread_id=thread.id,
        run_id=run.id
    )

    # Check if the run status is completed
    if run_status.status == "completed":
        break
    else:
        # Wait for a short period before checking again
        time.sleep(1)

# Now that the run is completed, list and print messages    
messages = list_messages(thread.id)

# Print the messages in reverse order
print_messages(messages)
