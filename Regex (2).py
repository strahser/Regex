import re
from io import StringIO
from dataclasses import dataclass
from translate import Translator
import json
import os
from datetime import datetime
import pandas as pd
ST_LIST = ["expander","button","warning","write","selectbox","multiselect"]
class StringBuilder:
    _file_str = None

    def __init__(self):
        self._file_str = StringIO()

    def Append(self, str):
        self._file_str.write(str)

    def __str__(self):
        return self._file_str.getvalue()

def text_between_quotes(text):
    between_quotes = text.split('"')[1::2]
    # if you have an odd number of quotes (ie. the quotes are unbalanced), 
    # discard the last element
    if len(between_quotes) % 2 == 0 and not text.endswith('"'):
        return between_quotes[:-1]
    return between_quotes

def replace_values_in_string(text, args_dict):
    for key in args_dict.keys():
        text = text.replace(key, str(args_dict[key]))
    return text

def remove_special_simbols(input_string:str):
    final_string = "" #define string for ouput
    excludes_charecters ={" ":"_","+":"p_"}
    for character in input_string:
        if(character.isalnum()):
            # if character is alphanumeric concat to final_string
            final_string = final_string + character
        elif character in excludes_charecters.keys():
            final_string = final_string + excludes_charecters[character]
    return final_string
    
def create_replacment_dict(data:str,start_with_befor_qoute:str,new_class:str=""):
    all = re.findall(f'{start_with_befor_qoute}\(\".*?"',data)    
    clear_list =[val.replace(f'{start_with_befor_qoute}(',"") for val in all]#оставляем кавычки, что бы заменить на класс все вложение
    remove_special_simbols_list = [remove_special_simbols(val) for val in clear_list]
    serealasied_list =[f"{new_class}"+val for val in remove_special_simbols_list]
    replaced_dict = dict(zip(clear_list,serealasied_list))
    return replaced_dict

def replace_data_by_dict(data:str,st_list: list[str],new_class:str=""):
    temp_dict = {}
    for val in st_list:
        temp_dict.update(create_replacment_dict(data,val,new_class))
    return temp_dict

def create_default_data_class(temp_dict):
    excludes_charecters ={"🔃":"refresh","🔗":"link" }   
    str_class = StringBuilder()
    str_class.Append("""@dataclass\nclass String:\n""")
    for key,val in temp_dict.items():
        if key in excludes_charecters.keys():
            str_class.Append(f"\t{val.replace(val,excludes_charecters[val])}:str={key}")
            str_class.Append("\n")
            return str_class
        else:
            str_class.Append(f"\t{val}:str={key}")
            str_class.Append("\n")
            return str_class        

def _create_json(dict_: dict,file_path:str):
    with open(file_path,"w",encoding='utf-8') as f:
        json.dump(dict_,
                indent=4,
                ensure_ascii=False,
                fp=f)

def write_list_from_dict_to_txt(data: dict,file_name:str):
    with open(file_name,"w") as f:
        for key,val in data.items():
            f.write(f"{val}\n")

def create_translated_ru_json(en_dict: dict):
    translator= Translator(to_lang = 'ru')
    ru_dict = {k:translator.translate(v) for k,v in en_dict.items()}
    _create_json(ru_dict,"ru_dict.json")

def create_main_dict_all_folders(root_dir):
    main_dict = {}    
    for dname, dirs, files in os.walk(root_dir):
        for fname in files:
            if fname.endswith(".py"):
                try:
                    fpath = os.path.join(dname, fname)
                    with open(fpath) as f:
                        s = f.read()
                    temp_dict = replace_data_by_dict(s,ST_LIST)
                    main_dict.update(temp_dict)
                except:
                    with open("log.txt","a") as lf:
                        lf.write(f"{datetime.now()}:{fpath}\n")
    return main_dict
def _create_ru_dict_from_excel():
    dict_values = pd.read_excel("ru_dict_table.xlsx")[["Variable","ru_data"]].to_dict()
    with open("ru_dict.json","w",encoding='utf-8') as f:
        json.dump(dict_values,
            indent=4,
            ensure_ascii=False,
            fp=f)
def create_data_class(main_dict: dict):
    st_build= StringBuilder()
    st_build.Append("from dataclasses import dataclass\n\n")
    st_build.Append("@dataclass\nclass Translate:\n\t")
    for key,val in  main_dict.items():
        st_build.Append(f"{val}:str={key}\n\t")
    with open("Translate.py","w", encoding='utf-8') as data_file:
        data_file.write(str(st_build))

_create_ru_dict_from_excel()


# root_dir = r"c:\Users\Strakhov\YandexDisk\ProjectCoding\HvacAppStreamlit"
# main_dict= create_main_dict_all_folders(root_dir=root_dir)
# en_dict = {v:k.replace('"',"") for k,v in main_dict.items()}
# write_list_from_dict_to_txt(main_dict,"translation_keys.txt")

# _create_json(en_dict,"en_dict.json")
# create_data_class(main_dict=main_dict)
# create_translated_ru_json(en_dict)






