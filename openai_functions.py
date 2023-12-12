import openai
import sys
import time


OPEN_API_KEY = "YOUR API KEY"

try:
    # Initialize the API client
    client = openai.OpenAI(api_key=OPEN_API_KEY)
    # Perform a test API call
    client.models.list()
    print("✅ API key is valid.\n")
except: 
    print("❌ API key is invalid.\n")
    sys.exit()

# Create an Assistant
# An assistant is the custom GPT model that will be used to generate responses
def create_assistant(name, instructions, model, tools, file_ids):
    print(f"🛠 Creating Assistant: {name}\n")
    assistant = client.beta.assistants.create(
        name=name,
        instructions=instructions,
        model=model,
        tools=tools,
        file_ids=file_ids
    )
    print(f"🛠 Assistant created successfully: {assistant.id} - {assistant.name} - {assistant.model}\n")
    return assistant

# Upload a file for the Assistant to use
def upload_file(file_name):
    print(f"📁 Uploading file: {file_name}\n")
    file = client.files.create(
        file=open(file_name, "rb"),
        purpose="assistants"
    )
    print(f"📁 File uploaded successfully: {file.id} - {file.filename}\n")
    return file


# Create a Thread
#  A thread is a conversation between a user and an assistant
def create_thread():
    print("🧵 Creating a new thread...\n")
    thread = client.beta.threads.create()
    print(f"🧵 Thread created successfully: {thread.id}\n")
    return thread

# Create a Message in the Thread
def create_message(thread_id, role, content):
    print(f"💬 Adding message to thread {thread_id}...\n")
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role=role,
        content=content
    )
    print("💬 Message added successfully.\n")
    return message

# Create a Run on the Thread
# A run is the process of the assistant generating a response to a message
def create_run(thread_id, assistant_id):
    print(f"🏃‍♂️ Creating a run in thread {thread_id}...\n")
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )
    print(f"🏃‍♂️ Run created successfully: {run.id}\n")
    return run

# Retrieve the status of a run
# The run status will be "queued", "processing", or "completed"
def retrieve_run_status(thread_id, run_id):
    print(f"🔍 Retrieving run status for run {run_id} in thread {thread_id}...\n")
    run_status = client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run_id
    )
    print("🔍 Run status retrieved successfully.\n")
    return run_status

# List all messages in a thread
def list_messages(thread_id):
    print(f"📄 Listing all messages in thread {thread_id}...\n")
    messages = client.beta.threads.messages.list(
        thread_id=thread_id
    )
    print("📄 Messages listed successfully.\n")
    return messages

# Print all messages in chronological order
def print_messages(messages):
    print("📖 Printing all messages in chronological order:\n")
    for message in reversed(messages.data):
        print(message.role + ": " + message.content[0].text.value + "\n")
    print("📖 All messages printed.\n")

# Wait for a run to complete
def wait_for_run_to_complete(thread_id, run_id):
    while True:
        # Retrieve the latest status of the run
        run_status = retrieve_run_status(
            thread_id=thread_id,
            run_id=run_id
        )

        # Check if the run status is completed
        if run_status.status == "completed":
            print("🏃‍♂️ Run completed.\n")
            break
        else:
            # Wait for a short period before checking again
            time.sleep(5)


def run_and_print_messages(thread_id, assistant_id, content=None):
    if content:
        # Create a message in the thread
        create_message(
            thread_id=thread_id,
            role="user",
            content=content
        )

    # Create and wait for the run to complete
    run = create_run(thread_id=thread_id, assistant_id=assistant_id)
    wait_for_run_to_complete(thread_id, run.id)

    # List and print messages
    messages = list_messages(thread_id)
    print_messages(messages)
