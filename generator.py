import random
import sys

#x = 100000
#sys.setrecursionlimit(x)

n = int(sys.argv[1])
m = int(sys.argv[2])
p = float(sys.argv[3])
nr_walls = int(p * (n - 2) * (m - 2))

def matrix_border(matrix):
    global nr_walls
    for i in range(n):
        matrix[i][0] = 1
        matrix[i][m - 1] = 1
    for i in range(m):
        matrix[0][i] = 1
        matrix[n - 1][i] = 1
    return matrix
def print_matrix(matrix):
    #for i in range(n):
        #for j in range(m):
            #print(matrix[i][j], end=' ')
        #print()
    return
def get_walls(matrix):
    nr = 0
    for i in range(n):
        for j in range(m):
            if(matrix[i][j] == 1 and i != 0 and j != 0 and i != n - 1 and j != m - 1):
                nr += 1
    return nr
def get_free(matrix):
    nr = 0
    for i in range(n):
        for j in range(m):
            if(matrix[i][j] == 0):
                nr += 1
    return nr
global_fill = 0
def fill(matrix, i, j):    
    global global_fill
    if(i >= 0 and i < n and j >= 0 and j < m and matrix[i][j] == 0):
        global_fill += 1
        matrix[i][j] = -1
        #print(i,j)
        fill(matrix, i + 1, j)
        fill(matrix, i, j + 1)
        fill(matrix, i - 1, j)
        fill(matrix, i, j - 1) 
def unfill(matrix, i, j):
    if(i >= 0 and i < n and j >= 0 and j < m and matrix[i][j] == -1):
        matrix[i][j] = 0
        #print(1)
        unfill(matrix, i + 1, j)
        unfill(matrix, i, j + 1)
        unfill(matrix, i - 1, j)
        unfill(matrix, i, j - 1)
def matrix_is_ok(matrix):
    saved_i = -1
    saved_j = -1
    global global_fill
    for i in range(n):
        for j in range(m):
            if(matrix[i][j] == 0):
                saved_i = i
                saved_j = j
                break
    #print(saved_i, saved_j)
    all_empty = get_free(matrix)
    global_fill = 0
    fill(matrix, saved_i, saved_j)
    unfill(matrix, saved_i, saved_j)
    #print(global_fill, all_empty)
    if(global_fill != all_empty):
        return False
    return True
def matrix_form_walls(matrix):
    current_walls = 0
    while(current_walls < nr_walls):
        ok = 0
        while(ok == 0):
            #print(get_free(matrix))
            chosen_one = random.randint(0, get_free(matrix) - 1)
            current = 0
            saved_i = -1
            saved_j = -1
            for i in range(n):
                for j in range(m):
                    if(matrix[i][j] == 0):
                        if(current == chosen_one):
                            saved_i = i
                            saved_j = j
                            break
                        current += 1
                if(saved_i != -1):
                    break
            matrix[saved_i][saved_j] = 1
            if(matrix_is_ok(matrix)):
                ok = 1
                break
            else:
                matrix[saved_i][saved_j] = 0
        current_walls += 1
    return matrix
def matrix_place_val(matrix, val):
    try:
        chosen_one = random.randint(0, get_free(matrix) - 1)
    except:
        print("Percentage too high, no free space for pacman and 2 fruits")
        exit(0)
    current = 0
    saved_i = -1
    saved_j = -1
    for i in range(n):
        for j in range(m):
            if(matrix[i][j] == 0):
                if(current == chosen_one):
                    saved_i = i
                    saved_j = j
                    break
                current += 1
        if(saved_i != -1):
            break
    matrix[saved_i][saved_j] = val
    return matrix

def main():
    #print(sys.argv[0])  
    #print(nr_walls)
    #0 - free
    #1 - wall
    #2 - pacman
    #3 - fruit
    matrix = []
    for i in range(n):
        matrix.append([])
        for j in range(m):
            matrix[i].append(0)
    matrix = matrix_border(matrix)
    matrix = matrix_form_walls(matrix)
    matrix = matrix_place_val(matrix,2)
    #doar doua fructe
    matrix = matrix_place_val(matrix,3)
    matrix = matrix_place_val(matrix,3)
    
    #print(get_walls(matrix))
    #print_matrix(matrix)
    for i in range(n):
        for j in range(m):
            if(matrix[i][j] == 0):
                sys.stdout.write('.')
                #print('.', end='')
            if(matrix[i][j] == 1):
                sys.stdout.write('%')
                #print('%', end='')
            if(matrix[i][j] == 2):
                sys.stdout.write('P')
                #print('P', end='')
            if(matrix[i][j] == 3): 
                sys.stdout.write('o')
                #print('o', end='')
        sys.stdout.write('\n')
    return
main() 
#VTM
