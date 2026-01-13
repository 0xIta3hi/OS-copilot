import os

results = []
def search_files(filename_keyword):
    """
    Searches a file based on a certain keyword if the file contains the keyword then it returns it. 
    Skips hidden directories.
    """
    start_path = os.environ('USERPROFILE')
    search_terms = filename_keyword.lower.split()
    for root, dirs, files in start_path:
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != ["AppData", "node_modules", "__pycache__"]]
        for file in files:
            if filename_keyword.lower in file.lower:
                full_path = os.path.join(root, file)
                full_path_lower = full_path.lower()
                if all(term in full_path_lower for term in search_terms):
                    results.append(full_path)

                    if len(results) > 5:
                        return results
    return results

