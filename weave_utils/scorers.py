import ast
from typing import List
import weave
import re


@weave.op()
def extract_answer(output: str) -> str:
    match = re.search(r"Final Answer:\s*([A-F])", output.strip(), re.IGNORECASE)
    if match:
        return match.group(1).upper()
    else:
        raise ValueError("No answer found in model output")


@weave.op()
def eval_majority_vote(output: List[str], answer: str):
    model_answers = []
    for _output in output:
        try:
            model_answers.append(extract_answer(_output))
        except ValueError:
            continue  # Skip this output if extraction fails
    
    if not model_answers:
        raise ValueError("Failed to extract any valid answers from model outputs")
    
    return model_answers.count(answer) > len(model_answers) / 2


@weave.op()
def eval_multi_choice(output: str, answer: str):
    # model_answer = extract_answer(output)
    # return model_answer == answer
    if "json" in output:
        cleaned_string = output.replace("```json", "").replace("```", "").strip()
        # Convert the cleaned string to a valid dictionary
        data = eval(cleaned_string)  # Use eval cautiously or replace with a safer parser if needed
        cleansed_output = data.get('answer')
        model_answer = cleansed_output
    else:
        cleansed_output = ast.literal_eval(output)
        model_answer = cleansed_output["answer"]
        print("model_answer ", model_answer)

    return model_answer == answer

