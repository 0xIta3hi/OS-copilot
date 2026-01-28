import os
import string

def get_drives():
    """Returns available drives (C:\, D:\) using standard os check."""
    drives = []
    for letter in string.ascii_uppercase:
        drive_path = f"{letter}:\\"
        if os.path.exists(drive_path):
            drives.append(drive_path)
    return drives

def search_files(keyword):
    """
    Smart Search with Relevance Ranking.
    Prioritizes exact matches and shorter paths.
    """
    results = [] # List of tuples: (score, file_path)
    keyword = keyword.lower()
    
    # Get all drives
    search_roots = get_drives()
    
    print(f"DEBUG: Searching for '{keyword}' in {search_roots}...")

    for start_dir in search_roots:
        for root, dirs, files in os.walk(start_dir):
            
            if 'WinSxS' in root or 'Servicing' in root or 'Program Files' in root:
                continue

            # Skip hidden/trash folders
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ["AppData", "$RECYCLE.BIN", "System Volume Information"]]

            for file in files:
                file_lower = file.lower()
                full_path = os.path.join(root, file)

                # --- THE SCORING LOGIC ---
                score = 0
                
                # Check 1: Is the keyword in the file name?
                if keyword in file_lower:
                    # Case A: Exact Match (e.g. "hosts" == "hosts") -> JACKPOT
                    if file_lower == keyword:
                        score += 100
                    
                    # Case B: Starts With (e.g. "hosts.txt") -> Good
                    elif file_lower.startswith(keyword):
                        score += 50
                        
                    # Case C: Contains (e.g. "LocalHost") -> Okay
                    else:
                        score += 10
                    
                    score -= len(full_path) * 0.1 
                    
                    results.append((score, full_path))

    results.sort(key=lambda x: x[0], reverse=True)
    
    # Return top 5 paths only
    final_paths = [path for score, path in results[:5]]
    
    return final_paths