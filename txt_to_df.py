import os
def main():
    ls = []
    dict_of_str = {}
    def txt_to_dataset(file) -> list:
        '''
        INPUT:
        file: a file that needs to be read

        OUTPUT:
        lines: the string of the EHR

        Return the string version of the EHR from the .txt file
        '''

        with open(file, encoding='utf-8-sig') as f:
            lines = f.readlines()
        lines = ' '.join(lines)
        lines = lines.replace('\n', '')
        return lines

    for path, subdirs, files in os.walk('DataSet (Medecine)/2010 - Relations'):
        for name in files:
            file = os.path.join(path, name)
            if file.endswith('.txt'):
                ls.append(file)

    for file in ls:
        dict_of_str[file] = txt_to_dataset(file)
    return dict_of_str
        
if __name__ == "__main__":
    main()
