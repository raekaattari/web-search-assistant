import anthropic 

client = anthropic.Anthropic() 

message = client.messages.create(
    model = "claude-opus-4-6",
    max_tokens=1000,
    messages=[
    {
        "role":"user",
        "content":"What should I search for to find the latest news on Formula 1?"
    }]
)

print(message.content)