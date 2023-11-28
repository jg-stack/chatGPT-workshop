from openai_functions import create_assistant, create_thread, create_message, create_run, retrieve_run_status, list_messages, print_messages
import time

ASSISTANT_NAME = "[YOUR ASSISTANT NAME]"
INSTRUCTIONS = "[YOUR INSTRUCTIONS]"

# Create an assistant
assistant = create_assistant(
    name=ASSISTANT_NAME,
    instructions=INSTRUCTIONS,
    model="gpt-4-1106-preview",
    tools=[{"type": "retrieval"}],
    file_ids=[] 
)

# Create a thread
thread = create_thread()

# Create a message in the thread
message = create_message(
    thread_id=thread.id,
    role="user",
    content="How often do you need to replace an oil filter?"
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
