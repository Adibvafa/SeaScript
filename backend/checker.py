import matlab.engine
import numpy as np
import tempfile
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from bson.objectid import ObjectId

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
        return evaluate_matlab_function(user_input.strip(), func_name, question_data['test'])
    
    print(f"Warning: No question data found for function '{func_name}'")
    return False, None

def fetch_question_data(func_name):
    """
    Fetch the question data (test cases) for a given function from the database.
    """
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    query = {"function": func_name}
    question_data = collection.find_one(query)
    
    if question_data:
        return {
            "test": question_data.get("test", [])
        }
    return None

def convert_to_matlab(eng, value):
    """
    Convert Python values to MATLAB compatible types.
    """
    if isinstance(value, list):
        if all(isinstance(item, str) for item in value):
            return eng.cell(value)
        elif all(isinstance(item, (int, float)) for item in value):
            return matlab.double(value)
        else:
            return [convert_to_matlab(eng, item) for item in value]
    elif isinstance(value, (int, float)):
        return float(value)  # MATLAB uses doubles by default
    elif isinstance(value, str):
        return value
    else:
        raise ValueError(f"Unsupported type: {type(value)}")

def evaluate_matlab_function(user_input, func_name, test_cases):
    """
    Evaluate a MATLAB function by running multiple test cases.
    """
    eng = matlab.engine.start_matlab()
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, f"{func_name}.m")
            with open(file_path, 'w') as f:
                f.write(user_input)
            
            eng.addpath(temp_dir)
            matlab_func = getattr(eng, func_name)
            
            results = []
            all_correct = True

            for test_case in test_cases:
                input_value = test_case['input']
                expected_output = test_case['output']
                
                # Handle both single values and arrays
                if isinstance(input_value, list):
                    matlab_input = [convert_to_matlab(eng, value) for value in input_value]
                else:
                    matlab_input = [convert_to_matlab(eng, input_value)]
                
                result = matlab_func(*matlab_input)
                
                if isinstance(result, matlab.double):
                    result = np.array(result).flatten()[0]  # Convert to scalar if possible
                
                is_correct = np.isclose(result, expected_output)
                results.append({
                    'input': input_value,
                    'expected': expected_output,
                    'actual': result,
                    'correct': is_correct
                })
                
                if not is_correct:
                    all_correct = False
            
            return all_correct, results

    except Exception as e:
        print(f"Error evaluating function '{func_name}': {str(e)}")
        return False, None
    
    finally:
        eng.quit()

if __name__ == "__main__":
    # Example usage
    # func_name = "can_jellyfish_swim"
    # user_input = """
    # function result = can_jellyfish_swim(hour)
    #     result = (hour >= 6 && hour <= 18);
    # end
    # """

    func_name = "count_familiar_sharks"
    user_input = """
    function count = count_labeled_sharks(previous_sharks, new_sharks)
        count = sum(ismember(new_sharks, previous_sharks));
    end
    """
    
    all_correct, results = grade_matlab_function(func_name, user_input)
    if results is not None:
        print(f"Function '{func_name}' evaluation result: {'All Correct' if all_correct else 'Some Incorrect'}")
        for idx, result in enumerate(results):
            print(f"Test case {idx + 1}:")
            print(f"  Input: {result['input']}")
            print(f"  Expected: {result['expected']}")
            print(f"  Actual: {result['actual']}")
            print(f"  Correct: {'Yes' if result['correct'] else 'No'}")
            print()
    else:
        print("No results to display. An error occurred during evaluation.")