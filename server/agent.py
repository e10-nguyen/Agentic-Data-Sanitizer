from model import Model, GPT_4_1

class Agent:

    def __init__(self, model: Model = GPT_4_1):
        self.model = model()

    def test_model(self):
        example_text = "This is a test. Respond with the greeting of your choice!"
        response = self.model.create_response(example_text)
        return response
    
if __name__ == "__main__":
    agent = Agent()
    print(agent.test_model())
