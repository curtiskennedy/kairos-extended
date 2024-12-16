from openai import OpenAI
from openai.types.beta.threads.message_create_params import (
    Attachment,
    AttachmentToolFileSearch,
)
import json

# Load the config file
with open("config.json", "r") as config_file:
    config = json.load(config_file)

filename = "graphs/subgraph_10.txt"
prompt = '''
You are a cybersecurity expert analyzing a provenance graph for suspicious activities.  
I am uploading a file that has a provenance graph in the DOT language. 
Each node in the graph corresponds to an entity, while the edges are interactions like file accesses, network connections, or process creations. 
Take this file and Think step-by-step:
1. Analyze each node in the graph. Is it a well-known process or entity? Output only the anomalies.
2. For each edge, examine the interaction between the connected nodes. Is the interaction expected or suspicious? Note any anomalies and state them.
3. Based on the previous steps, summarize the behaviour of the graph in 1-3 sentences. Include here any suspicious access and what type of access that is and why that is suspicious.
4. Decide if the activity is benign or an attack. Provide one sentence with a reason.
Example Output:
Step 1: Node Analysis
- Node 1: nginx (Process). - Well-known process. Behavior appears normal.
- Node 2: /tmp/script.sh (File). - Temporary file used by nginx. Suspicious due to unusual naming.
Step 2: Edge Analysis
- Edge (nginx → /tmp/script.sh): Write operation. - Suspicious, as nginx does not typically write to this type of file.
Step 3. Summary
Step 1: Node Analysis
Node 1: smtpd (Process) - A well-known service for handling email via SMTP. Behavior appears normal.
Step 2: Edge Analysis
Edge (smtpd → /usr/local/libexec/postfix/smtpd): Execute operation. - Expected, as smtpd should execute its binary.
Step 3: Graph Behavior Summary
The graph exhibits these behaviours. However, the access to /etc/spwd.db is unusual and warrants further scrutiny.
Step 4: Conclusion
- This is an attack. The unusual interaction between nginx and a temporary script file indicates potential misuse of the web server.
'''
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
    thread_id=thread.id, assistant_id=pdf_assistant.id, timeout=10000, temperature=1.0
)

if run.status != "completed":
    raise Exception("Run failed:", run)

messages_cursor = client.beta.threads.messages.list(thread_id=thread.id)
messages = [message for message in messages_cursor]

# Output text
res_txt = messages[0].content[0].text.value
#save to file with name of text
print(res_txt)