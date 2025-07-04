try:
    from secret import GPT_4_1_SECRET_KEY
except:
    raise FileNotFoundError ("No secret.py file in the server directory. Create one and make sure it is in the .gitignore.")
    
class Model:
    """A base class for models to be used in agent.py."""

    def __init__(self):
        pass

    def create_response(self, text):
        pass
    
class GPT_4_1(Model):

    def __init__(self):
        from openai import AzureOpenAI

        endpoint = "https://aoai-ucla-prjs.openai.azure.com/"
        api_version = "2025-03-01-preview"

        self.model = "gpt-4o"
        self.client = AzureOpenAI(api_version=api_version,
                                  azure_endpoint=endpoint,
                                  api_key=GPT_4_1_SECRET_KEY)
        
    def create_instructed_response(self, instruction, text):
        response = self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "developer",
                    "content": instruction
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )

        return response.output_text
        
    def create_response(self, text):
        response = self.client.responses.create(
            model=self.model,
            input=text
        )
        return response.output_text
    
if __name__=="__main__":
    model = GPT_4_1()
    example_text = "This is a test. Respond with the greeting of your choice!"
    response = model.create_response(example_text)
    print(response)
