import google.generativeai as genai
from django.conf import settings
from ..code_executor import execute_code

def evaluate_code_with_test_cases(code, language, test_cases, function_name):
    results = []
    print(f"Debug: Evaluating code with function name: {function_name}")
    
    for test_case in test_cases:
        # Prepare code with test input
        test_code = prepare_test_code(code, language, test_case['input'], function_name)
        print(f"Debug: Generated test code:\n{test_code}")
        
        # Execute the code
        execution_result = execute_code(test_code, language)
        print(f"Debug: Execution result: {execution_result}")
        
        if execution_result['error']:
            results.append({
                'input': test_case['input'],
                'expected': test_case['output'],
                'actual': None,
                'passed': False,
                'error': execution_result['error']
            })
            continue
        
        # Use Gemini to evaluate the output
        is_correct = evaluate_output_with_gemini(
            execution_result['output'].strip(),
            test_case['output'].strip(),
            test_case['input']
        )
        
        results.append({
            'input': test_case['input'],
            'expected': test_case['output'],
            'actual': execution_result['output'].strip(),
            'passed': is_correct,
            'error': None
        })
    
    return results

def prepare_test_code(code, language, test_input, function_name):
    """Prepare code with test input based on language"""
    if language == 'python':
        return f"""
{code}

# Test input
result = {function_name}('{test_input}')
print(result)
"""
    elif language == 'javascript':
        return f"""
{code}

// Test input
console.log({function_name}('{test_input}'));
"""
    elif language == 'java':
        return f"""
public class Solution {{
    {code}
    
    public static void main(String[] args) {{
        Solution solution = new Solution();
        System.out.println(solution.{function_name}("{test_input}"));
    }}
}}"""
    elif language == 'cpp':
        return f"""
#include <iostream>
#include <string>
using namespace std;

{code}

int main() {{
    Solution solution;
    cout << solution.{function_name}("{test_input}") << endl;
    return 0;
}}"""
    return code

def evaluate_output_with_gemini(actual_output, expected_output, test_input):
    """Use Gemini API to evaluate if the outputs are equivalent"""
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    prompt = f"""
    Evaluate if these two outputs are functionally equivalent for the given input.
    
    Input: {test_input}
    Expected Output: {expected_output}
    Actual Output: {actual_output}
    
    The outputs should be exactly 't' or 'f'.
    Respond with only 'true' if they are exactly equal, or 'false' if they are not.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip().lower() == 'true'
    except Exception as e:
        print(f"Error evaluating with Gemini: {e}")
        # Fall back to exact string comparison
        return actual_output.strip() == expected_output.strip() 