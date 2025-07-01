from model import Model, GPT_4_1

IDENTIFICATION_PROMPT = \
'''You are a redaction agent. Your task is to evaluate whether a given piece of text contains information that would be considered sensitive from the perspective of the user.

If the text contains sensitive information, respond with:

Y The text is sensitive because [brief explanation].

If the text does not contain sensitive information, respond with:

N

Do not include anything other than the exact responses above.'''

REDACTION_PROMPT = \
'''You are a redaction agent. The user will provide some sensitive text. The user has identified that the text is sensitive because: """HERE""".

Your task is to respond with the text in one of three ways, provided below. Attempt to use the earlier methods before the later methods.

Method one:
If the sensitivity can be removed by redacting some parts of the text, without including brackets, respond with:

REPLACE [text to be replaced] REPLACE_WITH [one to two word description of the text]

Method two:
If a short description can remove the sensitive parts of the text, respond with:

DESCRIPTION [a short description of the text]

Method three:
If the other methods don't work, respond with:

REDACTED

Do not include anything other than the exact responses above.
'''

EXAMPLE_TEXT = '''Hi team,

Just a quick update on the Q3 deliverables. We're on track to hit our deadlines, and the new UI mockups look great-thanks again to Clara and Ben for the quick turnaround. Please remember to upload your timesheets by Friday. Also, if you need VPN access while traveling, use the temporary credentials: username: j.doe@company.com, password: TempAccess#2025. We received the final invoice from DeltaTech-total amount: $48,500—which I've forwarded to Finance. Let me know if there are any issues with the internal compliance report attached below.

Best,
Samantha'''

class Agent:

    def __init__(self, model: Model = GPT_4_1):
        self.model = model()

    def is_sensitive(self, line):
        """Uses LLM to determine if text is sensitive or not."""
        response = self.model.create_instructed_response(IDENTIFICATION_PROMPT, line)
        value = None

        explanation = ""
        if len(response) >= 1:
            if response[0] == "Y":
                value = True
                if len(response) > 1:
                    explanation = response[1:]
            elif response[0] == "N":
                value = False

        return value, explanation
    
    def redact_line(self, line, explanation):
        """Uses LLM to redact a line of text."""
        output = line
        value, explanation = agent.is_sensitive(line)
        if value:
            response = self.model.create_instructed_response(REDACTION_PROMPT.replace("HERE", explanation), line)
            command = response.split()[0]
            if command == "REPLACE":
                response = response[len("REPLACE "):]
                split_response = response.split(" REPLACE_WITH ")
                if len(split_response) == 2:
                    print(response)
                    output = line.replace(split_response[0], split_response[1])
                else:
                    print("LLM gave invalid replacement command.")
                    print(split_response)
                    output = response
            elif command == "DESCRIPTION":
                output = "[" + response[len("DESCRIPTION "):] + "]"
            elif command == "REDACTED":
                output = "[REDACTED]"
        return output
        
        
    
if __name__ == "__main__":
    agent = Agent()
    example_text = "Also, if you need VPN access while traveling, use the temporary credentials: username: j.doe@company.com, password: TempAccess#2025."
    redacted_text = example_text
    value, explanation = agent.is_sensitive(example_text)
    print((value, explanation))
    if value:
        redacted_text = agent.redact_line(example_text, explanation)
    print(redacted_text)