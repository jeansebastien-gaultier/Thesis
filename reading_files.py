import os
import re
import sys
import pandas as pd
import re
from itertools import groupby
from xml.dom import minidom
from itertools import groupby


# Retrieve files in a directory
def search_for_files(root, ext) -> list:
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


# For .txt files
def txt_file(file) -> str:
    """
    For text files with individual EHR, open it and read the lines
    """
    with open(file, encoding="utf-8-sig") as f:
        lines = ''.join(f.readlines())
    return lines

# def multi_txt_files(file, keyword) ->list(list(str)):
#     """
#     For text files with multiple
#     """
#     with open(file, encoding="utf-8-sig") as f:
#         lines = ''.join(f.readlines())
#     lines = list(filter(None,re.split(rf'{keyword}', lines)))
#     lines = [list(g) for k,g in groupby(lines,lambda x:x=='Record') if not k]
#     lines = [keyword + ele for ele in lines]
#     return lines

# For .xml files
def xml_file(file,tag, flag = 'ind') -> str or list:
    """
    For xml files that have individual EHR
    """
    file = minidom.parse(file)
    text = file.getElementsByTagName(tag)
    final = []
    for txt in text:
        ls = []
        for element in txt.childNodes:
            if type(element).attributes == None:
                ls.append(element.data)
            else:
                ls.append(element.firstChild.data)
        final.append(''.join(ls))
    if flag =='ind':
        return final[0]
    else:
        return final


def split_text(text) -> list:
    keyword = 'Record date'
    text = re.split(rf'({keyword})', text)
    result = [list(g) for k,g in groupby(text,lambda x:x=='Record') if not k]
    result = [keyword + ele[0] for ele in result]
    return result

def quick_clean(txt):
    txt = txt.replace("\n", "")
    txt = txt.lower()
    txt = txt.strip()
    txt = txt.replace("*", "")
    txt = txt.replace("[ report_end ]", "")
    return txt

if __name__ == '__main__':
    root = sys.argv[1]
    i = 0
    EHR = {}

    text_files = search_for_files(root, '.txt')
    xml_files = search_for_files(root, '.xml')


    print(len(xml_files))

    for file in xml_files:

        files = minidom.parse(file)
        if files.getElementsByTagName('text') != 0:
            tag = 'text'
        else:
            tag = 'TEXT'
        text = files.getElementsByTagName(tag)

        if len(text) == 1:
            EHR[i] = quick_clean(xml_file(file, tag, 'ind'))
            i+=1
        else:
            for ele in xml_file(file, tag, 'multi'):
                EHR[i] = quick_clean(ele)
                i+=1

    print(len(EHR))

    ALL = dict(sorted(EHR.items()))
    ALL_c = ALL.copy()

    a = 1
    for k, v in ALL.items():
        if v in list(ALL.values())[a:]:
            del ALL_c[k]
        a += 1

    ALL = ALL_c

    final = {}
    i = 1

    for idx, txt in ALL.items():
        final[i] = txt
        i += 1

    print(pd.DataFrame.from_dict(EHR, orient = 'index'))


    


    