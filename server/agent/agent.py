from model import Model, GPT_4_1
from prompts import *

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
        list_of_commands = response.split("\n")

        output = line

        # REPLACE
        for command in list_of_commands:
            split_command = command.split()
            if split_command[0] == "REPLACE":
                command = command[len("REPLACE "):]
                split_response = command.split(" REPLACE_WITH ")
                if len(split_response) == 2:
                    output = output.replace(split_response[0], '[' + split_response[1].strip() + ']')
                else:
                    print("LLM gave invalid replacement command.")
                    output = response

        return output
    
    def redact_line(self, line):
        output = line
        value, explanation = self.is_sensitive(line)
        #print(f"Line: {line}\nValue: {value}\nExplanation: {explanation}")
        if value:
            output = self.redact_from_explanation(line, explanation)
        return output
        
        
    
if __name__ == "__main__":
    agent = Agent()
    example_text = "We received the final invoice from DeltaTech-total amount: $48,500—which I've forwarded to Finance."
    redacted_text = agent.redact_line(example_text)
    example_text_2 = '''The production process for NVIDIA's next-generation "Black Diamond" GPU architecture begins with the proprietary application of photonic lattice etching on sub-2nm graphene-infused wafers. This is executed at our undisclosed Fab-X facility in Nevada, where lithographic patterns are encoded using our classified 7-layer Deep Quantum Phase Shifter (DQPS) technology.'''
    redacted_text_2 = agent.redact_line(example_text_2)
    print("\n" + redacted_text + "\n\n" + redacted_text_2 + "\n")