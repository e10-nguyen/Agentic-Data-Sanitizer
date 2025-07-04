import os
from openai import AzureOpenAI
from secret import GPT_4_1_SECRET_KEY

endpoint = "https://aoai-ucla-prjs.openai.azure.com/"
model_name = "gpt-4o"
deployment = "gpt-4o"
subscription_key = GPT_4_1_SECRET_KEY
api_version = "2025-03-01-preview"

client = AzureOpenAI(api_version=api_version,
                     azure_endpoint=endpoint,
                     api_key=subscription_key)

response = client.responses.create(
    model="gpt-4.1",
    input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)