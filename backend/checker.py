import matlab.engine
import numpy as np
import tempfile
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from bson.int64 import Int64

# Load environment variables
load_dotenv()

# Database constants
MONGO_URI = os.getenv("mongodb_uri")
DATABASE_NAME = "matlab"
COLLECTION_NAME = "matlab"


def grade_matlab_function(func_name, user_input):
    """
    Main function to handle the grading of a MATLAB function.
    """
    question_data = fetch_question_data(func_name)
    
    print(f"Grading function '{func_name}' with user input")

    if question_data:
        return evaluate_matlab_function(user_input.strip(), func_name, question_data['answer'], question_data['input'])
    
    print(f"Warning: No question data found for function '{func_name}'")
    return False, None

def fetch_question_data(func_name):
    """
    Fetch the question data (answer and input) for a given function from the database.
    """
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    print(f"Searching for function: {func_name}")
    query = {"function": func_name}
    question_data = collection.find_one(query)
    print(f"Query result: {question_data}")
    
    if question_data:
        return {
            "answer": convert_to_python_type(question_data.get("answer")),
            "input": convert_to_python_type(question_data.get("input"))
        }
    return None

def convert_to_python_type(value):
    """
    Convert MongoDB types to Python types.
    """
    if isinstance(value, Int64):
        return int(value)
    elif isinstance(value, list):
        return [convert_to_python_type(item) for item in value]
    elif isinstance(value, dict):
        return {k: convert_to_python_type(v) for k, v in value.items()}
    return value

def evaluate_matlab_function(user_input, func_name, expected_answer, function_input):
    """
    Evaluate a MATLAB function by comparing its output to the expected answer.
    """
    eng = matlab.engine.start_matlab()
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, f"{func_name}.m")
            with open(file_path, 'w') as f:
                f.write(user_input)
            
            eng.addpath(temp_dir)
            matlab_func = getattr(eng, func_name)
            
            result = matlab_func(function_input)
            
            if isinstance(result, matlab.double):
                result = np.array(result).flatten()[0]  # Convert to scalar if possible
            
            if isinstance(expected_answer, (list, np.ndarray)):
                is_correct = np.allclose(result, expected_answer)
            else:
                is_correct = np.isclose(result, expected_answer)
            
            return is_correct, result

    except Exception as e:
        print(f"Error evaluating function '{func_name}': {str(e)}")
        return False, None
    
    finally:
        eng.quit()


if __name__ == "__main__":
    # Example usage
    func_name = "jellyfish"  # This is the function name in your database
    user_input = """
    function y = jellyfish(x)
        y = 1;
    end
    """
    is_correct, result = grade_matlab_function(func_name, user_input)
    print(f"Function '{func_name}' evaluation result: {'Correct' if is_correct else 'Incorrect'}")
    print(f"Output: {result}")