import google.generativeai as genai
from django.conf import settings
import json

# Configure Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

def generate_coding_question(difficulty):
    prompt = f"""Generate a coding question with the following format:
    {{
        "title": "Write a brief title here",
        "description": "Write a detailed problem description here",
        "test_cases": [
            {{"input": "example input 1", "output": "example output 1"}},
            {{"input": "example input 2", "output": "example output 2"}},
            {{"input": "example input 3", "output": "example output 3"}}
        ],
        "difficulty": "{difficulty}"
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        # Try to find JSON-like content in the response
        response_text = response.text.strip()
        # Find the first { and last } to extract the JSON object
        start = response_text.find('{')
        end = response_text.rfind('}') + 1
        if start != -1 and end != 0:
            json_str = response_text[start:end]
            return json.loads(json_str)
        else:
            # Fallback question if API fails
            return {
                "title": "Sum of Two Numbers",
                "description": "Write a function that takes two numbers as input and returns their sum.",
                "test_cases": [
                    {"input": "2, 3", "output": "5"},
                    {"input": "-1, 1", "output": "0"},
                    {"input": "0, 0", "output": "0"}
                ],
                "difficulty": difficulty
            }
    except Exception as e:
        print(f"Error generating question: {e}")
        # Return a fallback question
        return {
            "title": "Sum of Two Numbers",
            "description": "Write a function that takes two numbers as input and returns their sum.",
            "test_cases": [
                {"input": "2, 3", "output": "5"},
                {"input": "-1, 1", "output": "0"},
                {"input": "0, 0", "output": "0"}
            ],
            "difficulty": difficulty
        } 