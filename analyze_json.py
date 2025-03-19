import json
import os

def analyze_file(file_path):
    print(f"Analyzing file: {file_path}")
    print(f"File size: {os.path.getsize(file_path)} bytes")
    
    with open(file_path, 'r') as f:
        # Read the first 500 characters to check the start of the file
        start = f.read(500)
        print(f"First 500 characters:\n{start}\n")
        
        # Reset file pointer
        f.seek(0)
        
        # Count opening and closing braces and brackets
        content = f.read()
        open_curly = content.count('{')
        close_curly = content.count('}')
        open_bracket = content.count('[')
        close_bracket = content.count(']')
        
        print(f"Opening curly braces: {open_curly}")
        print(f"Closing curly braces: {close_curly}")
        print(f"Opening square brackets: {open_bracket}")
        print(f"Closing square brackets: {close_bracket}")
        
        # Reset file pointer
        f.seek(0)
        
        # Check if it starts with an array
        is_array = content.strip().startswith('[')
        print(f"File starts with '[': {is_array}")
        
        # Try to count JSON objects (this is approximate)
        object_count = 0
        level = 0
        in_string = False
        escape_char = False
        
        for char in content:
            if escape_char:
                escape_char = False
                continue
                
            if char == '\\':
                escape_char = True
                continue
                
            if char == '"' and not escape_char:
                in_string = not in_string
                continue
                
            if not in_string:
                if char == '{':
                    if level == 0:
                        object_count += 1
                    level += 1
                elif char == '}':
                    level -= 1
        
        print(f"Approximate object count: {object_count}")
        
        # Try parsing the first object if it's an array
        if is_array:
            try:
                f.seek(0)
                # Skip the opening bracket
                f.read(1)
                
                # Try to read until we find a complete object
                object_text = ""
                level = 0
                in_string = False
                escape_char = False
                
                for char in f.read():
                    object_text += char
                    
                    if escape_char:
                        escape_char = False
                        continue
                        
                    if char == '\\':
                        escape_char = True
                        continue
                        
                    if char == '"' and not escape_char:
                        in_string = not in_string
                        continue
                        
                    if not in_string:
                        if char == '{':
                            level += 1
                        elif char == '}':
                            level -= 1
                            if level == 0:
                                break
                
                # Try to parse this object
                first_object = json.loads(object_text)
                print(f"\nSample object structure:")
                for key in first_object.keys():
                    value_type = type(first_object[key]).__name__
                    print(f"  {key}: {value_type}")
                    
                    # If it's a list or dict, print the size
                    if value_type == 'list':
                        print(f"    Length: {len(first_object[key])}")
                        if first_object[key] and len(first_object[key]) > 0:
                            print(f"    First item type: {type(first_object[key][0]).__name__}")
                    elif value_type == 'dict':
                        print(f"    Keys: {list(first_object[key].keys())}")
                
            except Exception as e:
                print(f"Error parsing first object: {str(e)}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        analyze_file(sys.argv[1])
    else:
        print("Please provide a file path")