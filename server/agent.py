from model import Model, GPT_4_1

IDENTIFICATION_PROMPT = \
'''You are a redaction agent. Your task is to evaluate whether a given piece of text contains information that would be considered sensitive from the perspective of the user.

In addition, the user has identified that these elements are particularly sensitive: """SENSITIVE_INFORMATION""".

Respond with: The text may be sensitive because [brief explanation]. The text may not be sensitive if [breif explanation]. [Y/N: Y if the text is sensitive, N if the text is not sensitive.]

Example input: Also, if you need VPN access while traveling, use the temporary credentials: username: j.doe@company.com, password: TempAccess#2025.
Example output: The text may be sensitive because it contains login creditials. The text may not be sensitive if the receiver is trusted. Y
'''

REDACTION_PROMPT = \
'''You are a redaction agent. The user will provide some sensitive text. The user has identified that their text is sensitive because: """HERE""". Your task is to redact the text using one of three methods, provided below. Attempt to use the earlier methods before the later methods.

Example input: Also, if you need VPN access while traveling, use the temporary credentials: username: j.doe@company.com, password: TempAccess#2025.

Method one:
If the sensitivity can be removed by redacting some parts of the text respond with: REPLACE [text to be replaced] REPLACE_WITH [one to two word description of the text]
Example output: REPLACE username: j.doe@company.com, password: TempAccess#2025 REPLACE_WITH VPN credentials 

Method two:
If a short description can remove the sensitive parts of the text, respond with: DESCRIPTION [a short description of the text]
Example output: DESCRIPTION The sender offers VPN credentials for travel.

Method three:
If the other methods don't work, respond with: REDACTED
Example output: REDACTED

With the example input, we would use method one because the sensitive information can be replaced with a short description.
'''

EXAMPLE_TEXT = '''Hi team,

Just a quick update on the Q3 deliverables.
We're on track to hit our deadlines, and the new UI mockups look great-thanks again to Clara and Ben for the quick turnaround.
Please remember to upload your timesheets by Friday.
Also, if you need VPN access while traveling, use the temporary credentials: username: j.doe@company.com, password: TempAccess#2025.
We received the final invoice from DeltaTech-total amount: $48,500—which I've forwarded to Finance.
Let me know if there are any issues with the internal compliance report attached below.

Best,
Samantha'''

class Agent:

    def __init__(self, model: Model = GPT_4_1):
        self.model = model()
        self.sensitive_information = "Company specific information which is not publically avalible."

    def is_sensitive(self, line):
        """
        Determines if a given line of text contains sensitive information.

        Args:
            line (str): The input text to be evaluated for sensitivity.

        Returns:
            tuple:
                - value (bool or None): True if the text is identified as sensitive, False if not, or None if undetermined.
                - explanation (str): An optional explanation provided by the model, empty if not available.
        """

        id_prompt = IDENTIFICATION_PROMPT.replace("SENSITIVE_INFORMATION", self.sensitive_information)
        response = self.model.create_instructed_response(id_prompt, line)
        
        value = None
        explanation = ""

        if len(response) >= 1:
            if response[-1] == "Y":
                value = True
            elif response[-1] == "N":
                value = False
            explanation = response[:-1]

        return value, explanation
    
    def redact_from_explanation(self, line, explanation):
        """
        Redacts a line of text based on the explanation.

        Args:
            line (str): The input text to be redacted.
            explanation (str): The explanation for what needs to be redacted.

        Returns:
            tuple:
                - value (bool or None): True if the text is identified as sensitive, False if not, or None if undetermined.
                - explanation (str): An optional explanation provided by the model, empty if not available.
        """

        response = self.model.create_instructed_response(REDACTION_PROMPT.replace("HERE", explanation), line)
        command = response.split()[0]

        output = line

        # REPLACE
        if command == "REPLACE":
            response = response[len("REPLACE "):]
            split_response = response.split(" REPLACE_WITH ")
            if len(split_response) == 2:
                output = line.replace(split_response[0], '[' + split_response[1].strip() + ']')
            else:
                print("LLM gave invalid replacement command.")
                output = response
        # DESCRIPTION
        elif command == "DESCRIPTION":
            output = "[" + response[len("DESCRIPTION "):] + "]"
        # REDACT
        elif command == "REDACTED":
            output = "[REDACTED]"

        return output
    
    def redact_line(self, line):
        output = line
        value, explanation = self.is_sensitive(example_text)
        if value:
            output = self.redact_from_explanation(example_text, explanation)
        return output
        
        
    
if __name__ == "__main__":
    agent = Agent()
    example_text = "We received the final invoice from DeltaTech-total amount: $48,500—which I've forwarded to Finance."
    redacted_text = agent.redact_line(example_text)
    print(redacted_text)