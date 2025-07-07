from openai import OpenAI

client = OpenAI(
    api_key="sk-or-v1-Use Your Own API Key",
    base_url="https://openrouter.ai/api/v1"
)

response = client.chat.completions.create(
     model="Your own OpenAI api key",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa, Siri and Google Cloud."},
        {"role": "user", "content": "What is coding?"}
    ]
)

print(response.choices[0].message.content)
