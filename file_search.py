import os
import string

def get_drives():
    """Returns a list of available drives (C:\, D:\, etc.)"""
    drives = []
    # FIX: Use wmic to get actual mounted drives
    for letter in string.ascii_uppercase:
        # FIX: Check for the letter variable, not the string "letter"
        drive_path = f"{letter}:\\"
        if os.path.exists(drive_path):
            drives.append(drive_path)
    return drives

def search_files(filename_keyword):
    """
    Searches a file based on a keyword.
    """
    results = []
    # FIX: lower() needs parentheses
    search_terms = filename_keyword.lower().split()
    # Get all drives to search
    search_roots = get_drives()
    print(f"DEBUG: Searching drives: {search_roots}")

    for start_dir in search_roots:
        # FIX: Added os.walk() - without this, you are just looping over letters
        for root, dirs, files in os.walk(start_dir):
            
            # FIX: Skip system folders to prevent freezing
            if 'Windows' in root or 'Program Files' in root:
                continue

            # FIX: 'not in' list, not '!=' list
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ["AppData", "node_modules", "__pycache__", "$RECYCLE.BIN"]]

            for file in files:
                # FIX: full path creation
                full_path = os.path.join(root, file)
                full_path_lower = full_path.lower()

                # FIX: Check if ALL terms are in the path
                if all(term in full_path_lower for term in search_terms):
                    print(f"[+] Found: {full_path}")
                    results.append(full_path)

                    if len(results) >= 5:
                        return results
                     
    return results