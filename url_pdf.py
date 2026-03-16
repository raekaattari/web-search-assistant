import anthropic 

client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[
    {
        "role": "user",
        "content": [
            {
                "type": "document",
                "source": {
                    "type": "url",
                    "url": "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf" # pdf url
                    },
            },
            {"type": "text", "text": "What are the key findings in this document?"}
            
            ],
        }
    ],
)

print(message.content)