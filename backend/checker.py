import numpy as np
import tempfile
from functools import lru_cache
import matlab
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from setup import setup_resources

class MatlabGrader:
    def __init__(self, matlab_engine, mongo_collection, mongo_client):
        self.matlab_engine = matlab_engine
        self.collection = mongo_collection
        self.mongo_client = mongo_client

    @lru_cache(maxsize=None)
    def fetch_question_data(self, func_name):
        """
        Fetch the question data (test cases) for a given function from the database.
        """
        query = {"function": func_name}
        question_data = self.collection.find_one(query)
        
        if question_data:
            return {
                "question": question_data.get("question", ""),
                "test": question_data.get("test", []),
                "puzzle_piece": question_data.get("puzzle_piece", "")
            }
        return None

    def fetch_question(self, func_name):
        """
        Fetch the question.
        """
        question_data = self.fetch_question_data(func_name)
        return question_data["question"] if question_data else "END"

    def fetch_puzzle_piece(self, func_name):
        """
        Fetch the puzzle piece.
        """
        question_data = self.fetch_question_data(func_name)
        return question_data["puzzle_piece"] if question_data else "END"

    def convert_to_matlab(self, value, func_name):
        """
        Convert Python values to MATLAB compatible types based on the function name.
        """
        if func_name == "can_jellyfish_swim":
            return float(value)
        elif func_name == "count_familiar_sharks":
            return [self.matlab_engine.cell(value[0]), self.matlab_engine.cell(value[1])]
        elif func_name == "find_nemos_skyscraper":
            return matlab.double(value)
        elif func_name == "open_treasure_chest":
            return []  # No input for this function
        else:
            raise ValueError(f"Unknown function: {func_name}")

    def evaluate_matlab_function(self, user_input, func_name, test_cases):
        """
        Evaluate a MATLAB function by running multiple test cases.
        """
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                file_path = os.path.join(temp_dir, f"{func_name}.m")
                with open(file_path, 'w') as f:
                    f.write(user_input)
                
                self.matlab_engine.addpath(temp_dir)
                matlab_func = getattr(self.matlab_engine, func_name)
                
                results = []
                for test_case in test_cases:
                    input_value = test_case.get('input')
                    expected_output = test_case['output']
                    
                    matlab_input = self.convert_to_matlab(input_value, func_name) if input_value is not None else []
                    
                    result = matlab_func(*matlab_input) if isinstance(matlab_input, list) else matlab_func(matlab_input)
                    
                    result = self.process_matlab_result(result)
                    
                    is_correct = result == expected_output
                    results.append({
                        'input': input_value,
                        'expected': expected_output,
                        'actual': result,
                        'correct': is_correct
                    })
                    
                    if not is_correct:
                        return False, results
                
                return True, results

        except Exception as e:
            print(f"Error evaluating function '{func_name}': {str(e)}")
            return False, None

    def process_matlab_result(self, result):
        """
        Process the result returned from MATLAB.
        """
        if isinstance(result, matlab.logical):
            return bool(result)
        elif isinstance(result, matlab.double):
            return np.array(result).flatten()[0]  # Convert to scalar if possible
        elif isinstance(result, str):
            return result.strip()  # Remove any leading/trailing whitespace
        return result

    def grade_matlab_function(self, func_name, user_input):
        """
        Main function to handle the grading of a MATLAB function.
        """
        question_data = self.fetch_question_data(func_name)
        print(f"Grading function '{func_name}' with user input")

        if question_data:
            return self.evaluate_matlab_function(user_input.strip(), func_name, question_data['test'])
        
        print(f"Warning: No question data found for function '{func_name}'")
        return False, None

    def print_results(self, func_name, all_correct, results):
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

    def close_resources(self):
        """
        Close the MATLAB engine and MongoDB client.
        """
        self.matlab_engine.quit()
        self.mongo_client.close()

# Example usage
if __name__ == "__main__":
    # Initialize resources
    matlab_engine, collection, mongo_client = setup_resources()

    # Create MatlabGrader instance
    grader = MatlabGrader(matlab_engine, collection, mongo_client)

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
            message = 'Exploration unlocks hidden treasures.';
        end
        """)
    ]

    try:
        for func_name, user_input in functions:
            grader.fetch_question(func_name)
            all_correct, results = grader.grade_matlab_function(func_name, user_input)
            grader.print_results(func_name, all_correct, results)
            print("\n" + "="*50 + "\n")
    finally:
        # Clean up resources
        grader.close_resources()