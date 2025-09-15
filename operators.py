import copy

def select(condition: str, table: dict) -> dict:
    # 5 types of compare operators: <=, >=, <, >, =
    result = copy.deepcopy(table)
    
    if '<=' in condition:
        var, value = condition.split('<=')
        if var in table['columns']:
            i_data = table['columns'].index(var)
            pointer = 0
            for i in range(len(table['data'])): # table['data'] is a list of list
                data = table['data'][i][i_data]
                if data.isdigit(): # compare numbers
                    data = float(data) 
                    value = float(value)
                if not data <= value:
                    result['data'].pop(pointer)
                else:
                    pointer += 1
            return result        
        
    elif '>=' in condition:
        var, value = condition.split('>=')
        if var in table['columns']:
            i_data = table['columns'].index(var)
            pointer = 0
            for i in range(len(table['data'])): 
                data = table['data'][i][i_data]
                if data.isdigit(): # compare numbers
                    data = float(data) 
                    value = float(value)
                if not data >= value:
                    result['data'].pop(pointer)
                else:
                    pointer += 1
            return result  
        
    elif '<' in condition:
        var, value = condition.split('<')
        if var in table['columns']:
            i_data = table['columns'].index(var)
            pointer = 0
            for i in range(len(table['data'])): 
                data = table['data'][i][i_data]
                if data.isdigit(): # compare numbers
                    data = float(data) 
                    value = float(value)
                if not data < value:
                    result['data'].pop(pointer)
                else:
                    pointer += 1
            return result  
        
    elif '>' in condition:
        var, value = condition.split('>')
        if var in table['columns']:
            i_data = table['columns'].index(var)
            pointer = 0
            for i in range(len(table['data'])): 
                data = table['data'][i][i_data]
                if data.isdigit(): # compare numbers
                    data = float(data) 
                    value = float(value)
                if not data > value:
                    result['data'].pop(pointer)
                else:
                    pointer += 1
            return result
        
    elif '=' in condition:
        var, value = condition.split('=')
        if var in table['columns']:
            i_data = table['columns'].index(var)
            pointer = 0
            for i in range(len(table['data'])): 
                data = table['data'][i][i_data]
                if data.isdigit(): # compare numbers
                    data = float(data) 
                    value = float(value)
                if data != value:
                    result['data'].pop(pointer)
                else:
                    pointer += 1
            return result  
    else:
        return None
                    
                
def project(condition: str, table: dict) -> dict:
    condition = condition.split(',')
    condition_index = []
    result = copy.deepcopy(table)
    
    for i in range(len(condition)):
        idx = table['columns'].index(condition[i])
        condition_index.append(idx)
    
    counter = 0
    for j in range(len(table['columns'])):
        if j not in condition_index:
            result['columns'].pop(j-counter)
            for k in range(len(table['data'])):
                result['data'][k].pop(j-counter)
            counter += 1
            
    return result 
        
        
def join(condition: str, table_a: dict, table_b: dict) -> dict:
    # 2 format of join
    # A join B: no condition needed, when there is(are) a common column(s)
        # if multiple common columns, all need to be the same
        # at this moment, this join format is not implemented
    # A join condition B: no common column (implemented below)
        # I assume only one condition is given, 
        # and the compared parameters name can be the same in 2 tables (which is not valid in relaX)
    
    result = copy.deepcopy(table_a)
    condition = condition.split('=') # [table_a.b, table_b.c]
    a_arg = ''
    b_arg = ''
    
    if (condition[0].split('.')[0] == table_a['table_name']) and (condition[1].split('.')[0] == table_b['table_name']):
        a_arg = condition[0].split('.')[1]
        b_arg = condition[1].split('.')[1]
    elif (condition[1].split('.')[0] == table_a['table_name']) and (condition[0].split('.')[0] == table_b['table_name']):
        a_arg = condition[1].split('.')[1]
        b_arg = condition[0].split('.')[1]
    else:
        return None
    
    result['columns'] += table_b['columns']
    a_idx = table_a['columns'].index(a_arg)
    b_idx = table_b['columns'].index(b_arg)

    for i in range(len(table_a['data'])):
        for j in range(i, len(table_b['data'])):
            if table_a['data'][i][a_idx] == table_b['data'][j][b_idx]:
                result['data'][i] += table_b['data'][j]
                
    return result
    
    
def intersect(table_a: dict, table_b: dict) -> dict:
    if table_a['columns'] != table_b['columns']:
        return None
    
    result = copy.deepcopy(table_a)
    
    counter = 0
    for i in range(len(table_a)):
        pop = True
        for j in range(len(table_b)):
            if table_a['data'][i] == table_b['data'][j]:
                pop = False
                break
        if pop:
            result['data'].pop(i-counter)
            counter += 1
    
    return result


def union(table_a: dict, table_b: dict) -> dict:
    # aftern union, no duplicate items
    if table_a['columns'] != table_b['columns']:
        return None
    
    result = copy.deepcopy(table_a)
    for i in range(len(table_b['data'])):
        if table_b['data'][i] not in table_a['data']:
            result['data'].append(table_b['data'][i])
    
    return result

def minus(table_a: dict, table_b: dict) -> dict:
    if table_a['columns'] != table_b['columns']:
        return None
    
    result = copy.deepcopy(table_a)
    
    # Remove rows from result(table_a) that exist in table_b
    counter = 0
    for i in range(len(table_a['data'])):
        if table_a['data'][i] in table_b['data']:
            result['data'].pop(i - counter)
            counter += 1
            
    return result
