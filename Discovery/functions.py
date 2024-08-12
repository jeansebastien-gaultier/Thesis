import os

def search_for_files(root, ext):
    """
    For all the files that end in .txt in the DataSet (Medecine) folder are put into one list
    """
    ls = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            file = os.path.join(path, name)
            if file.endswith(ext):
                ls.append(file)
    return ls