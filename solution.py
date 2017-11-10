assignments = []

def cross(a, b):
    temp = []
    for s in a:
        for t in b:
            temp.append(s+t)
    return temp

rows = "ABCDEFGHI"
cols = "123456789"

# individual squares
boxes = cross(rows, cols)
# complete rows, columns and 3x3 squares will be called units. 
# there are 27 units in total
rows_units = [cross(r, cols) for r in rows]

cols_units = [cross(rows, r) for r in cols]
square_units = [cross(r, c) for r in ("ABC", "DEF", "GHI") for c in ("123", "456", "789")]

d1_units = [[rows[i] + cols[i] for i in range(len(rows))]]
d2_units = [[rows[i] + cols[::-1][i] for i in range(len(rows))]]

# redefine the unitlist according to specification of the sudoku 
diagonal_sudoku = 1
if diagonal_sudoku == 1:
    unitlist = rows_units + cols_units + square_units +  d1_units + d2_units
else: 
    unitlist = rows_units + cols_units + square_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

# this function creates a dictionary where key is the naked twin and value is a list of two boxes containing naked twins 
def twins_value_box(values, unit):
    d_value_box = dict()
    for u in unit:
        # subset only those that have length two as potential candidates
        if len(values[u]) == 2:
            if not values[u] in d_value_box:
                d_value_box[values[u]] = [u]
            else:
                d_value_box[values[u]].append(u)
    return d_value_box

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # create an empty dictionary that will contain a naked twin pair value and list of the peers 
    peers_of_naked_twin = dict()
    for unit in unitlist:
        # call twins_value_box function
        d_value_box = twins_value_box(values, unit)
        for key, value in d_value_box.items():
            if len(value) == 2:
                if not key in peers_of_naked_twin:
                    peers_of_naked_twin[key]=[unit]
                else:
                    peers_of_naked_twin[key].append(unit)
    # remove the values that are in naked twin in the potential values of other peers              
    for key in peers_of_naked_twin:
        for unit in peers_of_naked_twin[key]:
                for box in unit:
                    if values[box] != key:
                        assign_value(values, box, values[box].replace(key[0], ''))
                        assign_value(values, box, values[box].replace(key[1], ''))
    return values

def cross(A, B):
    "Cross product of elements in A and elements in B."
    pass

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    assert len(grid) == 81 
    temp = {}
    for i in range(len(grid)):
        if grid[i] == ".":
            temp[boxes[i]] = "123456789"
        else:
            temp[boxes[i]] = grid[i]
    return temp

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values 

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box])==1])
        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        #print("eliminated:")
        #print(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        #print("applied only choice")
        #print(values)
        values = naked_twins(values)
        #print("applied naked_twins")
        #print(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    values = reduce_puzzle(values)
    # Choose one of the unfilled squares with the fewest possibilities
    if values is False:
        return False
    if all(len(values[box]) == 1 for box in boxes):
        return values
    n, box_to_start = min((len(values[box]), box) for box in boxes if len(values[box])>1) 
    not_solved = [box for box in values.keys() if len(values[box]) >1]
    for value in values[box_to_start]:
        new_sudoku = values.copy()
        new_sudoku[box_to_start] = value
        attemp = search(new_sudoku)
        if attemp:
            return attemp

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values = search(values)
    return values

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
