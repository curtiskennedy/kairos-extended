from openai import OpenAI
from openai.types.beta.threads.message_create_params import (
    Attachment,
    AttachmentToolFileSearch,
)
import json

# Load the config file
with open("config.json", "r") as config_file:
    config = json.load(config_file)

filename = "graphs/subgraph_2.txt"
prompt = "you are a systems specialist with an expert in reading provenance graphs. Look at the text file and give a brief summary and a suggestion if its benign or not."

client = OpenAI(api_key=config["api_key"])

pdf_assistant = client.beta.assistants.create(
    model="gpt-4o",
    description="An assistant to read the provenance graphs of PDF files.",
    tools=[{"type": "file_search"}],
    name="Systems Analyst assistant",
)

# Create thread
thread = client.beta.threads.create()

file = client.files.create(file=open(filename, "rb"), purpose="assistants")

# Create assistant
client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    attachments=[
        Attachment(
            file_id=file.id, tools=[AttachmentToolFileSearch(type="file_search")]
        )
    ],
    content=prompt,
)

# Run thread
run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id, assistant_id=pdf_assistant.id, timeout=1000
)

if run.status != "completed":
    raise Exception("Run failed:", run.status)

messages_cursor = client.beta.threads.messages.list(thread_id=thread.id)
messages = [message for message in messages_cursor]

# Output text
res_txt = messages[0].content[0].text.value
print(res_txt)