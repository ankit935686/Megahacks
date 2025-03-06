import subprocess
import tempfile
import os
import time
from threading import Timer

def kill_process(process):
    process.kill()
    raise Exception("Code execution timed out")

def execute_python_code(code, timeout=5):
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file_path = f.name

        start_time = time.time()
        
        # Run the code in a subprocess
        process = subprocess.Popen(['python', temp_file_path], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE,
                                 text=True)
        
        # Set up timeout
        timer = Timer(timeout, kill_process, [process])
        try:
            timer.start()
            stdout, stderr = process.communicate()
        finally:
            timer.cancel()
            
        execution_time = time.time() - start_time
        
        # Clean up
        os.unlink(temp_file_path)
        
        return {
            'output': stdout,
            'error': stderr,
            'execution_time': execution_time
        }
        
    except Exception as e:
        return {
            'output': '',
            'error': str(e),
            'execution_time': 0
        }

def execute_cpp_code(code, timeout=5):
    try:
        # Create temporary cpp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False) as f:
            f.write(code)
            cpp_file = f.name
        
        # Create output executable name
        exe_file = cpp_file[:-4] + ('.exe' if os.name == 'nt' else '.out')
        
        start_time = time.time()
        
        # Compile
        compile_process = subprocess.run(['g++', cpp_file, '-o', exe_file], 
                                      capture_output=True, text=True)
        
        if compile_process.returncode != 0:
            return {
                'output': '',
                'error': f"Compilation Error:\n{compile_process.stderr}",
                'execution_time': 0
            }
        
        # Run
        process = subprocess.Popen([exe_file], 
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 text=True)
        
        timer = Timer(timeout, kill_process, [process])
        try:
            timer.start()
            stdout, stderr = process.communicate()
        finally:
            timer.cancel()
            
        execution_time = time.time() - start_time
        
        # Cleanup
        os.unlink(cpp_file)
        os.unlink(exe_file)
        
        return {
            'output': stdout,
            'error': stderr,
            'execution_time': execution_time
        }
    except Exception as e:
        return {'output': '', 'error': str(e), 'execution_time': 0}

def execute_java_code(code, timeout=5):
    try:
        # Extract class name from code
        import re
        class_match = re.search(r'public\s+class\s+(\w+)', code)
        if not class_match:
            return {
                'output': '',
                'error': 'Error: Could not find public class name',
                'execution_time': 0
            }
        
        class_name = class_match.group(1)
        
        # Create temporary java file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.java', delete=False) as f:
            f.write(code)
            java_file = f.name
        
        start_time = time.time()
        
        # Compile
        compile_process = subprocess.run(['javac', java_file], 
                                      capture_output=True, text=True)
        
        if compile_process.returncode != 0:
            return {
                'output': '',
                'error': f"Compilation Error:\n{compile_process.stderr}",
                'execution_time': 0
            }
        
        # Get directory of java file
        java_dir = os.path.dirname(java_file)
        
        # Run
        process = subprocess.Popen(['java', '-cp', java_dir, class_name], 
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 text=True)
        
        timer = Timer(timeout, kill_process, [process])
        try:
            timer.start()
            stdout, stderr = process.communicate()
        finally:
            timer.cancel()
            
        execution_time = time.time() - start_time
        
        # Cleanup
        os.unlink(java_file)
        os.unlink(os.path.join(java_dir, f"{class_name}.class"))
        
        return {
            'output': stdout,
            'error': stderr,
            'execution_time': execution_time
        }
    except Exception as e:
        return {'output': '', 'error': str(e), 'execution_time': 0}

def execute_javascript_code(code, timeout=5):
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            f.write(code)
            js_file = f.name

        start_time = time.time()
        process = subprocess.Popen(['node', js_file], 
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 text=True)
        
        timer = Timer(timeout, kill_process, [process])
        try:
            timer.start()
            stdout, stderr = process.communicate()
        finally:
            timer.cancel()
            
        execution_time = time.time() - start_time
        os.unlink(js_file)
        
        return {
            'output': stdout,
            'error': stderr,
            'execution_time': execution_time
        }
    except Exception as e:
        return {'output': '', 'error': str(e), 'execution_time': 0}

def execute_code(code, language):
    executors = {
        'python': execute_python_code,
        'cpp': execute_cpp_code,
        'java': execute_java_code,
        'javascript': execute_javascript_code
    }
    
    executor = executors.get(language)
    if executor:
        return executor(code)
    else:
        return {
            'output': '',
            'error': f'Language {language} is not supported',
            'execution_time': 0
        } 