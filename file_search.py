import os

results = []
def search_files(filename_keyword):
    """
    Searches a file based on a certain keyword if the file contains the keyword then it returns it. 
    Skips hidden directories.
    """
    start_path = os.environ('USERPROFILE')
    for root, dirs, files in start_path:
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != "AppData"]
        for file in files:
            if filename_keyword.lower in file.lower:
                full_path = os.path.join(root, file)
                results.append(full_path)

                if len(results) > 5:
                    return results
    return results
