from pathlib import Path
import re
import json
import sys

with open("mappings/basics_patterns.json", encoding='utf8') as rd:
    basic_patterns = json.load(rd)
with open("mappings/conditional_structures.json", encoding='utf8') as rd:
    conditonal_structure_map = json.load(rd)
with open("mappings/keywords_to_ignore.json", encoding='utf8') as rd:
    ignore_keywords = json.load(rd)

with open("mappings/linkedlist_functions.json", encoding='utf8') as rd:
    linkexp_map = json.load(rd)

def parse_linklist_line(line):
    matchs = re.finditer(linkexp_map['pattern'], line)
    for match in matchs:
        linkfun = match[0]
        parsed_linkfun = parse_linklist_funcs_rec("", "", linkfun)
        line = line.replace(linkfun, parsed_linkfun)
    return line

def parse_linklist_funcs_rec(result, funcname, text):
    match = re.match(linkexp_map['pattern'], text)
    if not match:
        exp = f"{text}{linkexp_map[funcname]}"
        return result + exp
    else:
        return parse_linklist_funcs_rec(
            result, 
            match.group(1) ,
            match.group(2)
        ) + f"{linkexp_map[funcname]}"

def remove_key_words(line):
    pattern = "\\b({igkey})\\b"
    for igkey in ignore_keywords:
        line = re.sub(pattern.format(igkey = igkey), "", line)
    return line

def apply_basic_pattern(line):
    for basic_pattern in basic_patterns:
        line = re.sub(
            basic_pattern['pattern'], 
            basic_pattern['pyeq'],
            line
        )
    return line

def apply_conditonal_pattern(line):
    cond_patterns = conditonal_structure_map['cond_patterns']
    boolean_exp = conditonal_structure_map['boolean_exp']
    match = False
    for cd_pattern in cond_patterns:
        prev_line = line
        line = re.sub(
            cd_pattern['pattern'], 
            cd_pattern['pyeq'],
            line
        )
        if prev_line != line:
            match = True
            break 
    if match:
        for key, value in boolean_exp.items():
            line = line.replace(key, value)

    exact_patterns = conditonal_structure_map['exact_patterns']
    for ep in exact_patterns:
        line = re.sub(
            ep['pattern'], 
            ep['pyeq'],
            line
        )

    return line

def get_pseudo_lines(filePath):
    with open(filePath, encoding='utf8') as rd:
        return rd.readlines()

def create_python_file(filePath, lines):
    file_name = Path(filePath).stem + "_python.py"
    with open(file_name, 'w', encoding='utf8') as wf:
        for line in lines:
            print(line, file = wf)

def pseudo2python(filePath):
    lines = get_pseudo_lines(filePath)
    n = len(lines)
    for i in range(n):
        lines[i] = lines[i].lower()
        lines[i] = remove_key_words(lines[i])
        lines[i] = apply_basic_pattern(lines[i])
        lines[i] = apply_conditonal_pattern(lines[i])
        lines[i] = parse_linklist_line(lines[i])
    
    create_python_file(filePath, lines)

if __name__ == "__main__":
    filePath = sys.argv[1]
    pseudo2python(filePath)