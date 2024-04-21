import copy

class algorithm:

    def get_tick(speed):
        #tick min. 100:

        if speed == 0:
            100, 1
        elif speed < 100:
            #tick is faster than speed
            return 100, 10000/speed
        #tick is speed
        return speed, 1
    
    def scores(name, score, moves, size):
        with open ("./results/" + name + ".txt", "a") as file:
            if score == size[0] * size[1]:
                file.write(str(size[0])+"x"+str(size[1]) + " P " + str(moves) + "\n")
            else:
                file.write(str(size[0])+"x"+str(size[1]) + " " + str(score) + "\n")

    def opposite_list(a, b):
        #returns if a and be are opposite directions
        return (a[0] == b[0] *-1 and a[0] != 0) or (a[1] == b[1] *-1 and a[1] != 0)

    def survive(CELLS, snake, pos, current_move, last_move):
        #return true if the snake will survive the next step
        return pos in CELLS and pos not in snake[1:] and not algorithm.opposite_list(current_move, last_move)
    
    def move_snake(entity, move):
        #theoreticly moves the snake in one direction
        last_head = entity[0].copy()
        for i in range(2):
            entity[0][i] += move[i]
        if len(entity) >= 2:
            for part in range(len(entity)-1, 1, -1):
                entity[part] = entity[part-1]
            entity[1] = last_head
        return entity

    def reach(CELLS, snake):
        #not working perfekt: 100 empty fields and loosing
        moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        queue, checked = [snake[0]], [snake[0]]
        reachable = []

        while queue:
            pos_x, pos_y = queue.pop(0)

            for move_x, move_y in moves:
                new_x, new_y = pos_x + move_x, pos_y + move_y

                if [new_x, new_y] in CELLS and not [new_x, new_y] in snake[1:] and [new_x, new_y] not in checked:
                    reachable.append([new_x, new_y])
                    queue.append([new_x, new_y])
                    checked.append([new_x, new_y])
        
        return reachable

    def set_param(val):
        #reach, on edge, food
        PARAM = [1, 1, 1]

        show = [PARAM[0] * val[0], PARAM[1] * val[1], PARAM[2] * val[2]]
        return sum(show), show


    def decide(scores):
        #if there is a snake body next to the head, the snake is not allowed to move near the edge unless its the only way
        RED = (235, 64, 52)
        WHITE = (255, 255, 255)

        #name, alive, reach, edge, distance food
        all = 0
        val = []
        show = []

        for dir in scores:
            if not dir[0]:
                val.append(0)
                show.append(0)
            else:
                tmp = algorithm.set_param(dir[1:])
                show.append(tmp[1])
                val.append(tmp[0])
                all += tmp[0]


        out = [[], [], [], []]
        for i in range(4):
            if all != 0:
                out[i] = [val[i] / all]
            else:
                out[i] = [0.25]

            #show parameters
            out[i].append(show[i])

            #apply color
            if out[i][0] <= 0.1:
                out[i].append(RED)
            else:
                out[i].append(WHITE)

        return out
            

#algorithms
    def straight(head, food):
        # straight to food
        dif_x = food[0][0] - head[0]
        dif_y = food[0][1] - head[1]
        
        if abs(dif_y) > abs(dif_x):
            if dif_y > 0:
                decision = [0, 1]   #down
            else:
                decision = [0, -1]  #up
        else:
            if dif_x > 0:
                decision = [1, 0]   #right
            else:
                decision = [-1, 0]  #left

        return "straight", decision



    def turning(head, food, last_move):
        # ability to turn
        dif_x = food[0][0] - head[0]
        dif_y = food[0][1] - head[1]

        if abs(dif_y) > abs(dif_x):
            if dif_y > 0:
                decision = [0, 1]   #down
            else:
                decision = [0, -1]  #up

            #turn
            if decision[1] == last_move[1] * -1:
                if dif_x > 0:
                    decision = [1, 0]   #right
                else:
                    decision = [-1, 0]  #left


        else:
            if dif_x > 0:
                decision = [1, 0]   #right
            else:
                decision = [-1, 0]  #left
            
            #turn
            if decision[0] == last_move[0] * -1:
                if dif_y > 0:
                    decision = [0, 1]   #down
                else:
                    decision = [0, -1]  #up

        return "turning", decision



    def smart(CELLS, snake, food):
        # add: not crashing into wall or itself as far as possible

        dif_x = food[0][0] - snake[0][0]
        dif_y = food[0][1] - snake[0][1]

        possibilities = [
            #x, y, score
            [0, 1, 0],  #down
            [0, -1, 0], #up
            [-1, 0, 0], #left
            [1, 0, 0]   #right
        ]

        #rates every option
        for option in possibilities:

            #check that decision won´t kill snake by going out of map or eating body
            new_pos = [snake[0][i] + option[i] for i in range(2)]
            if new_pos not in CELLS or new_pos in snake[1:]:
                option[2] = -1
            else:
                #checks if the snake will get closer to food
                new_dis = abs(food[0][0] - new_pos[0]) + abs(food[0][1] - new_pos[1])
                if new_dis == 0:
                    option[2] = 2
                elif new_dis < abs(dif_x) + abs(dif_y):
                    option[2] = 1/new_dis


        decision = max(possibilities, key=lambda sc: sc[2])[:2]
        return "smart", decision



    def perfect(CELLS, snake, food, last_move, num_free):
        #uses smart and looks how many tiles are reachable from new_pos at leas 80% of free tiles???
        #when theres food in you need to move first until there is more space

        # add: not trapping inside itself

        possibilities = [
            #x, y, reach, food
            ["down", 0, 1, 0, 0],   #down
            ["up", 0, -1, 0, 0],    #up
            ["left", -1, 0, 0, 0],  #left
            ["right", 1, 0, 0, 0]   #right
        ]

        for option in possibilities:
            new_pos = [snake[0][i] + option[i+1] for i in range(2)]
            
            #check that decision won´t kill snake by going out of map or eating body
            if new_pos in CELLS and new_pos not in snake[1:] and not algorithm.opposite_list(option[1:3], last_move):
                #tiles that are reachable from head
                option[3] = len(algorithm.reach(CELLS, algorithm.move_snake(copy.deepcopy(snake), option[1:3]))) / num_free

                #distance to food
                new_dis = abs(food[0][0] - new_pos[0]) + abs(food[0][1] - new_pos[1])
                if new_dis == 0:
                    option[4] = 1
                else:
                    option[4] = 1/ new_dis


        decision = max(possibilities, key=lambda sc: (sc[3] * sc[4]))
        return "perfect", decision[1:3]
    


    def gab(CELLS, snake, food, last_move, num_free):
        # add: leaving gabs at edges

        LIGHT_GREEN = (30, 212, 65)
        moves = [
            #x, y
            ["down", 0, 1],   #down
            ["up", 0, -1],    #up
            ["left", -1, 0],  #left
            ["right", 1, 0]   #right
        ]

        score = [[], [], [], []]
        for dir in range(len(moves)):
            new_pos = [snake[0][i] + moves[dir][i+1] for i in range(2)]
  
            #check that decision won´t kill snake by going out of map or eating body
            if not algorithm.survive(CELLS, snake, new_pos, moves[dir][1:], last_move):
                score[dir].append(False)
                score[dir].append(0)
            else:
                #tiles that are reachable from head
                score[dir].append(True)
                score[dir].append(len(algorithm.reach(CELLS, algorithm.move_snake(copy.deepcopy(snake), moves[dir][1:]))) / num_free )
                

                #check if snake is near edge by getting reach of the 2nd move
                next_reach = []
                new_snake = algorithm.move_snake(copy.deepcopy(snake), moves[dir][1:3])
                for move in moves:
                    if algorithm.survive(CELLS, new_snake, new_snake[0], move[1:], moves[dir][1:]):
                        next_reach.append(len(algorithm.reach(CELLS, algorithm.move_snake(copy.deepcopy(new_snake), move[1:]))) / num_free)
                
                score[dir].append(sum(next_reach) / len(next_reach))


                #distance to food
                new_dis = abs(food[0][0] - new_pos[0]) + abs(food[0][1] - new_pos[1])
                if new_dis == 0:
                    score[dir].append(2)
                else:
                    score[dir].append(1 / new_dis)

        results = algorithm.decide(score)
        most = results.index(max(results, key=lambda val: val[0]))
        results[most][2] = LIGHT_GREEN
        decision = moves[most][1:3]

        show = []
        for i in range(len(results)):
            show.append([moves[i][0] + ": " + str(int(results[i][0] * 100)) + "%, " + str(results[i][1]), results[i][2]])
        
        return "gab", decision, show


#hamiltonian cycle

    def move_along(path, head):
        start = path.index(tuple(head))
        return "follow_ham", [path[start +1][i] - path[start][i] for i in range(2)]


    def skippable(path, snake, start, end):
        queue = []
        #is array end between:
        if start <= end:
            for i in path[start: end + 1]:
                queue.append(i)
        else:
            for i in path[start:]:
                queue.append(i)
            for i in path[:end + 1]:
                queue.append(i)


        #check if gab is skippable
        for cell in queue:
            if cell in snake[1:]:   # cannot skip section, cause there is part of the snake
                return False
        #shortcut to food
        return True


    def shortcut(path, snake, food, last_move):
        name = "skip_ham"

        moves = [["down", 0, 1],
                ["up", 0, -1],
                ["left", -1, 0],
                ["right", 1, 0]]

        index_head = path.index(tuple(snake[0]))
        distance = (abs(food[0][0] - snake[0][0]) + abs(food[0][1] - snake[0][1]))

        cycle_move = algorithm.move_along(path, snake[0])

        for move in moves:
            new_pos = tuple([snake[0][i] + move[i+1] for i in range(2)])

            #value determinates how much closer the snkae will get   greater -> closer
            new_dif = distance - (abs(food[0][0] - new_pos[0]) + abs(food[0][1] - new_pos[1]))
            #in field, not move in opposite direction
            if algorithm.survive(path, snake, new_pos, move[1:3], last_move):
                move.append(new_dif/2 +0.5)
            else:
                move.append(-1)
            #1 -> to food
            #0 -> away from food
            #-1 -> dead

            #mark cycle_move
            if move[1:3] == cycle_move[1]:
                cycle_move = move


        best_move = max(moves, key=lambda val: val[3])
        pos = tuple([snake[0][i] + best_move[i+1] for i in range(2)])

        if cycle_move[3] == -1 or (best_move[3] > cycle_move[3] and algorithm.skippable(path, snake, index_head, path.index(pos))):
            #skip a section of path
            return name, best_move[1:3]
        #move normal along path except its opposite of moving direction
        return name, cycle_move[1:3]


    def pre_hamiltonian(ROWS, COLS):
        """this concept won't work"""

        #follow Hamiltonian path and skip when theres no snake in the skipped path
        #show on screen
        #path is layed out simple

        path = [(0, 0)]
        for row in range(ROWS):
            if row % 2 == 0:
                for col in range(1, COLS):
                    path.append((row, col))
            else:
                for col in range(COLS -1, 0, -1):
                    path.append((row, col))
        #upper lane
        for row in range(ROWS -1, -1, -1):
            path.append((row, 0))
        
        return path