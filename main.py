from operators import *
from tabulate import tabulate
import sys, json

# input tables, query
# data struction: a big list of: map {'table_name': '', 'columns': [], 'data': []}
# nested operations

# selection
# projection
# join
# intersection
# union
# minus

######################### helper functions #########################
def find_innermost_parentheses(query: str) -> tuple[int, int]:
    """Find the innermost parentheses group"""
    depth = 0
    max_depth = 0
    innermost_start = -1
    
    for i, char in enumerate(query):
        if char == '(':
            depth += 1
            if depth > max_depth:
                max_depth = depth
                innermost_start = i
        elif char == ')':
            if depth == max_depth and innermost_start != -1:
                return (innermost_start, i)
            depth -= 1
    return None                              
               
def change_query_element_order(query: str) -> list[str]:
    query = query.split()
    
    if 'join' in query:
        table_a = query.pop(0)
        query.insert(2, table_a) # ['join', 'condition', 'table_a', 'table_b']
        
    if ('intersect' in query) or ('union' in query) or ('minus' in query):
        table_a = query.pop(0)
        query.insert(1, table_a) # ['set operator', 'table_a', 'table_b']
    
    return query

def find_table(table_name: str, table_list: list[dict]) -> dict:
    for i in range(len(table_list)):
        if table_list[i]['table_name'] == table_name:
            return table_list[i]
    return None
            
################### end of helper functions #########################


def read_file_and_parse_table(filename: str) -> tuple[list, list]:
    with open(filename, 'r') as file:
        lines = file.readlines()
        
    # step 1: parse table

    # [
    #   {'table_name': '', 'columns': [], 'data': [ [], [] ]},
    #   {'table_name': '', 'columns': [], 'data': []},
    # ]
    
    table_list = []
    current_table_index = 0
    
    for i in range(len(lines)):
        if lines[i] == '\n':
            continue
        if '=' in lines[i] and '{' in lines[i]:
            table_list.append({'table_name': '', 'columns': [], 'data': []})
            table_name = lines[i].split('=')[0].strip()
            table_list[current_table_index]['table_name'] = table_name
            i += 1
            
            # table column
            columns = lines[i].strip().split(',')
            columns = [c.strip() for c in columns]
            table_list[current_table_index]['columns'] = columns
            i += 1
            
            # table data
            while (lines[i] != '}\n' and i < len(lines)):
                data = lines[i].strip().split(',')
                data = [d.strip() for d in data]
                table_list[current_table_index]['data'].append(data)
                i += 1
            current_table_index += 1
                    
    # step 2: parse Query
    full_query = ''
    for j in range(len(lines)):
        if 'query:' in lines[j].lower():
            full_query = lines[j][7:].strip()
             
    return table_list, full_query
   
                                
def parse_query(full_query: str) -> list[list]: # return [["operation", "condition", "table", ...], []]   
    # find the innermost ()
    # add the sub query to the result list
    # replace the () with 'temp'
    # loop until no () in query
    
    result = []
    idx_sub = 0
    
    while '(' in full_query:
        innermost_start, innermost_end = find_innermost_parentheses(full_query)
        sub_query = full_query[innermost_start+1:innermost_end] # string without ()
        sub_query = change_query_element_order(sub_query)
            
        result.append(sub_query)
        full_query = full_query[:innermost_start] + ' Result_' + str(idx_sub) + ' ' + full_query[innermost_end+1:]
        
        # the 'table_name' of this sub_query is replaced by 'Result_i'
        # we need to replace the all the left 'table_name.' to 'Result_i.' in full_query
        operator = sub_query[0]
        q_name_of = 'Result_' + str(idx_sub) + '.'
        
        if operator in ['select', 'project']:
            t_name_of = sub_query[2] + '.'
            if t_name_of in full_query:
                full_query = full_query.replace(t_name_of, q_name_of)
        elif operator == 'join':
            t_1_name_of = sub_query[2] + '.'
            t_2_name_of = sub_query[3] + '.'
            if t_1_name_of in full_query:
                full_query = full_query.replace(t_1_name_of, q_name_of)
            if t_2_name_of in full_query:
                full_query = full_query.replace(t_2_name_of, q_name_of)
        elif operator in ['intersect', 'union', 'minus']:
            t_1_name_of = sub_query[1] + '.'
            t_2_name_of = sub_query[2] + '.'
            if t_1_name_of in full_query:
                full_query = full_query.replace(t_1_name_of, q_name_of)
            if t_2_name_of in full_query:
                full_query = full_query.replace(t_2_name_of, q_name_of)
        
        idx_sub += 1
                
    # after parse all the query in (), there should be one last query left
    if full_query:
        query = change_query_element_order(full_query)
        result.append(query)
        
    return result
        

def main():
    file_name = sys.argv[1]    
    table_list, full_query = read_file_and_parse_table(file_name)
    query_list = parse_query(full_query)
    
    # print('query list: \n', query_list, '\n')
     
    for i in range(len(query_list)):
        operator = query_list[i][0]
        result = {}
        
        if operator in ['select', 'project', 'join']:
            condition = query_list[i][1]
            table_name_1 = query_list[i][2]
            table_1 = find_table(table_name_1, table_list)
        if operator in ['intersect', 'union', 'minus']:
            table_name_1 = query_list[i][1]
            table_1 = find_table(table_name_1, table_list)
            table_name_2 = query_list[i][2]
            table_2 = find_table(table_name_2, table_list)
            # print('old table_2: \n', table_2,)
            
        # print('query: \n', query_list[i])
        # print('old table_1:  \n', table_1)
                    
        if operator == 'select':
            result = select(condition, table_1)
        elif operator == 'project':
            result = project(condition, table_1)
        elif operator == 'join':
            table_name_2 = query_list[i][3]
            table_2 = find_table(table_name_2, table_list)   
            # print('old table_2:  \n', table_2,)         
            result = join(condition, table_1, table_2)
        elif operator == 'intersect':
            result = intersect(table_1, table_2)
        elif operator == 'union':
            result = union(table_1, table_2)
        elif operator == 'minus':
            result = minus(table_1, table_2)
            
        result['table_name'] = 'Result_' + str(i)
        table_list.append(result)
        # print('result:  \n', result, '\n')

    table = tabulate(result['data'], headers=result['columns'], tablefmt='fancy_grid')
        
    with open('out.txt', 'w') as file:
        file.write(table)
        file.write('\n')
        json.dump(result, file, indent=2)
        print("All Done")

if __name__ == "__main__":
    main()