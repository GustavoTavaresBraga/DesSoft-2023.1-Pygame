def can_reach_last_layer(grid):
    gridCopy = [row.copy() for row in grid]
    posInicial = [len(grid) - 1, grid[-1].index('P')]
    new_pos = posInicial
    found = False
    direction = 1
    for i in range(100):
        print(new_pos)
        if new_pos[0] == 0:
            found = True
        if grid[new_pos[0]-1][new_pos[1]] == 'X':
            new_pos = [new_pos[0]-1, new_pos[1]]
        elif grid[new_pos[0]][new_pos[1]+direction] == 'X':
            new_pos = [new_pos[0], new_pos[1]+direction]
        elif grid[new_pos[0]][new_pos[1]-direction] == 'X':
            new_pos = [new_pos[0], new_pos[1]-direction]
        else:
            direction = -direction
            new_pos = posInicial
            grid = [row.copy() for row in gridCopy]

        grid[new_pos[0]][new_pos[1]] = ' '
    if found:
        return True
    else:
        return False
# Example grid
grid = [
    [' ', 'X', 'X', 'X', 'X', 'X', ' ', 'X', ' '],
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'], 
    ['X', ' ', ' ', ' ', 'X', 'X', 'X', 'X', 'X'], 
    ['X', 'X', 'X', 'X', 'X', ' ', 'X', 'X', 'X'],
    ['X', ' ', 'X', ' ', ' ', 'X', ' ', ' ', 'X'], 
    [' ', 'X', 'X', 'P', 'X', 'X', 'X', ' ', 'X']
]
print(can_reach_last_layer(grid))
