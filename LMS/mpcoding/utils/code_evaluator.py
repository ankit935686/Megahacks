import google.generativeai as genai
from django.conf import settings
from ..code_executor import execute_code

def evaluate_code_with_test_cases(code, language, test_cases):
    results = []
    
    for test_case in test_cases:
        # Prepare code with test input
        test_code = prepare_test_code(code, language, test_case['input'])
        
        # Execute the code
        execution_result = execute_code(test_code, language)
        
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

def prepare_test_code(code, language, test_input):
    """Prepare code with test input based on language"""
    if language == 'python':
        return f"{code}\n\n# Test input\nprint({test_input})"
    elif language == 'javascript':
        return f"{code}\n\n// Test input\nconsole.log({test_input});"
    elif language == 'java':
        # Assuming main class is named Solution
        return f"""
public class Solution {{
    {code}
    
    public static void main(String[] args) {{
        Solution solution = new Solution();
        System.out.println({test_input});
    }}
}}"""
    elif language == 'cpp':
        return f"""
#include <iostream>
using namespace std;

{code}

int main() {{
    cout << {test_input} << endl;
    return 0;
}}"""
    return code

def evaluate_output_with_gemini(actual_output, expected_output, test_input):
    """Use Gemini API to evaluate if the outputs are equivalent"""
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""
    Evaluate if these two outputs are functionally equivalent for the given input.
    
    Input: {test_input}
    Expected Output: {expected_output}
    Actual Output: {actual_output}
    
    Respond with only 'true' if they are equivalent, or 'false' if they are not.
    Consider whitespace and formatting differences as equivalent.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip().lower() == 'true'
    except Exception as e:
        print(f"Error evaluating with Gemini: {e}")
        # Fall back to exact string comparison
        return actual_output == expected_output 