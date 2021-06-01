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

with open("mappings/stack_queues.json", encoding='utf8') as rd:
    stack_queue_expressions = json.load(rd)


post_regex_expressions = []
post_simple_replace_expression = []
header_lines = []

def parse_linklist_line(line):
    matchs = re.finditer(linkexp_map['pattern'], line)
    for match in matchs:
        linkfun = match[0]
        parsed_linkfun = parse_linklist_funcs_rec("", "", linkfun)
        line = line.replace(linkfun, parsed_linkfun)
    return line


previous_names = set()

def look_for_stack_queues_expressions(line):


    stack_expressions = stack_queue_expressions['stack']
    queues_expressions = stack_queue_expressions['queue']

    for pattern in stack_expressions:
        match = re.search(pattern['pattern'], line)
        if match:
            name = match.group(1)
            top_name = match.group(2)
            base_name = match.group(3)
            if name not in previous_names:
                header_lines.append(f"{name} = PseudoStack()")
                post_regex_expressions.append({
                    'replace_exp': rf"\b{top_name}\b",
                    'to_replace': f"{name}.top"
                })
                post_regex_expressions.append({
                    'replace_exp': rf"\b{base_name}\b",
                    'to_replace': f"{name}.size"
                })
            previous_names.add(name)
            line = re.sub(
                pattern['pattern'], 
                pattern['pyeq'],
                line
            )

    for pattern in queues_expressions:
        match = re.search(pattern['pattern'], line)
        if match:
            name = match.group(1)
            base_name = match.group(2)
            top_name = match.group(3)
            if name not in previous_names:
                header_lines.append(f"{name} = PseudoQueue()")
                post_regex_expressions.append({
                    'replace_exp': rf"\b{top_name}\b",
                    'to_replace': f"{name}.top"
                })
                post_regex_expressions.append({
                    'replace_exp': rf"\b{base_name}\b",
                    'to_replace': f"{name}.base"
                })
            previous_names.add(name)
            line = re.sub(
                pattern['pattern'], 
                pattern['pyeq'],
                line
            )
    
    return line


def parse_linklist_funcs_rec(result, funcname, text):
    match = re.search(linkexp_map['pattern'], text)
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


def apply_remaining_expressions(line):

    for exp in post_simple_replace_expression:
        line = line.replace(exp['replace_exp'], exp['to_replace'])

    for pattern in post_regex_expressions:
        line = re.sub(
            pattern['replace_exp'], 
            pattern['to_replace'],
            line
        )

    return line


def get_pseudo_lines(filePath):
    with open(filePath, encoding='utf8') as rd:
        return rd.readlines()

def create_python_file(filePath, lines):
    file_name = Path(filePath).stem + "_python.py"
    with open(file_name, 'w', encoding='utf8') as wf:
        for line in header_lines:
            print(line, file = wf)
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
        lines[i] = look_for_stack_queues_expressions(lines[i])

    for i in range(n):
        lines[i] = apply_remaining_expressions(lines[i])
    
    create_python_file(filePath, lines)

if __name__ == "__main__":
    filePath = sys.argv[1]
    pseudo2python(filePath)