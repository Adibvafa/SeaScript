import matlab.engine
import numpy as np
import tempfile
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database constants
MONGO_URI=os.getenv("mongodb_uri")
DATABASE_NAME = "matlab"
COLLECTION_NAME = "matlab"

def fetch_question(func_name):
    """
    Fetch the question.
    """
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    query = {"function": func_name}
    question_data = collection.find_one(query)
    
    if question_data:
        return (question_data["question"])
    return "END"
    
print(MONGO_URI)

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

def convert_to_matlab(eng, value, func_name):
    """
    Convert Python values to MATLAB compatible types based on the function name.
    """
    if func_name == "can_jellyfish_swim":
        return float(value)
    elif func_name == "count_familiar_sharks":
        return [eng.cell(value[0]), eng.cell(value[1])]
    elif func_name == "find_nemos_skyscraper":
        return matlab.double(value)
    elif func_name == "open_treasure_chest":
        return []  # No input for this function
    else:
        raise ValueError(f"Unknown function: {func_name}")

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
                input_value = test_case.get('input')
                expected_output = test_case['output']
                
                matlab_input = convert_to_matlab(eng, input_value, func_name) if input_value is not None else []
                
                if isinstance(matlab_input, list):
                    result = matlab_func(*matlab_input)
                else:
                    result = matlab_func(matlab_input)
                
                if isinstance(result, matlab.logical):
                    result = bool(result)
                elif isinstance(result, matlab.double):
                    result = np.array(result).flatten()[0]  # Convert to scalar if possible
                elif isinstance(result, str):
                    result = result.strip()  # Remove any leading/trailing whitespace
                
                is_correct = result == expected_output
                results.append({
                    'input': input_value,
                    'expected': expected_output,
                    'actual': result,
                    'correct': is_correct
                })
                
                if not is_correct:
                    all_correct = False
                    return False, None
            
            return all_correct, results

    except Exception as e:
        print(f"Error evaluating function '{func_name}': {str(e)}")
        return False, None
    
    finally:
        eng.quit()

def print_results(func_name, all_correct, results):
    if results is not None:
        print(f"Function '{func_name}' evaluation result: {'All Correct' if all_correct else 'Some Incorrect'}")
        for idx, result in enumerate(results):
            print(f"Test case {idx + 1}:")
            if func_name != "open_treasure_chest":
                print(f"  Input: {result['input']}")
            print(f"  Expected: {result['expected']}")
            print(f"  Actual: {result['actual']}")
            print(f"  Correct: {'Yes' if result['correct'] else 'No'}")
            print()
    else:
        print("No results to display. An error occurred during evaluation.")


if __name__ == "__main__":
    # Example usage for each function
    functions = [
        ("can_jellyfish_swim", """
        function result = can_jellyfish_swim(hour)
            result = (hour >= 6 && hour <= 18);
        end
        """),
        ("count_familiar_sharks", """
        function count = count_familiar_sharks(known_sharks, new_sightings)
            count = sum(ismember(new_sightings, known_sharks));
        end
        """),
        ("find_nemos_skyscraper", """
        function max_height = find_nemos_skyscraper(coral_city)
            max_height = max(sum(coral_city));
        end
        """),
        ("open_treasure_chest", """
        function message = open_treasure_chest()
            message = 'Go on!';
        end
        """)
    ]

    for func_name, user_input in functions:
        fetch_question(func_name)
        all_correct, results = grade_matlab_function(func_name, user_input)
        print_results(func_name, all_correct, results)
        print("\n" + "="*50 + "\n")
