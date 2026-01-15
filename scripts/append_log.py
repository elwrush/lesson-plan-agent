import os
import argparse
import sys

def append_to_log(log_type, content, project_root):
    """
    Appends content to the specified log file with proper formatting.
    """
    if log_type == "errors":
        file_path = os.path.join(project_root, "errors-fix.md")
        header_prefix = "## "
    elif log_type == "session":
        file_path = os.path.join(project_root, "session-log.md")
        header_prefix = "## "
    else:
        # Generic file path if strictly provided, though discouraged for this specific skill
        file_path = log_type

    if not os.path.exists(file_path):
        print(f"Error: Log file not found at {file_path}")
        return False

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()
        
        # Ensure we have a clean break from the previous content
        # If the file doesn't end with a newline, add one.
        # If it doesn't end with TWO newlines (blank line), add them.
        
        prefix = ""
        if existing_content:
            if not existing_content.endswith('\n'):
                prefix = "\n\n"
            elif not existing_content.endswith('\n\n'):
                prefix = "\n"
        
        # If we are starting a new section (usually content starts with ##), ensure visual separator
        # But allow the user's content to dictate fully.
        # We just guarantee ONE blank line minimum.
        
        final_content = prefix + content
        
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(final_content)
            
        print(f"Successfully appended to {file_path}")
        return True

    except Exception as e:
        print(f"Failed to write to log: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Safely append to project log files.")
    parser.add_argument("log_type", choices=["errors", "session"], help="Which log to update")
    parser.add_argument("content", help="The content string to append (use \\n for newlines or pass a file path with @file)")
    
    args = parser.parse_args()
    
    # Handle @file input for long content
    content_to_write = args.content
    if args.content.startswith("@"):
        input_file = args.content[1:]
        if os.path.exists(input_file):
            with open(input_file, 'r', encoding='utf-8') as f:
                content_to_write = f.read()
        else:
             # Assume literal string starting with @ if file doesn't exist? 
             # Or just fail. Let's assume literal if file missing but warn.
             print(f"Warning: Input file {input_file} not found, treating as literal string.")
    
    # Unescape newlines if passed as literal string \\n
    if not args.content.startswith("@"):
        content_to_write = content_to_write.replace("\\n", "\n")

    PROJECT_ROOT = os.getcwd() # Assumption: running from root
    success = append_to_log(args.log_type, content_to_write, PROJECT_ROOT)
    
    if not success:
        sys.exit(1)
