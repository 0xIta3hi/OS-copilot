import platform
import subprocess
import os


def read_files(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            content = f.read(10000)
            if len(content) == 10000:
                print("[!] File too long to read showing first 10000 character")
                print(content)

                user_agreement = input("Do you want to read the rest of file (y/n)")
                if user_agreement in ["y", "yes"]:
                    remaining_content = f.read()
                    print(remaining_content)
                    return content + remaining_content
                else:
                    return content + "__Truncated__"
            return content
    except FileNotFoundError:
        print(f"The requested file not found")
    except Exception as e:
        print(f"The following ran occured : {e}")

def open_files(file_name):
    try:
        os.startfile(file_name)
        return f"File Opened: {file_name}"
    except Exception as e:
        return f"Error : {e}"
    
