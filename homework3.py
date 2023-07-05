from queue import PriorityQueue


def ASTAR(search_space, start_x, start_y, dest_x, dest_y, max_row, max_col, parent, max_rock_height):
    def heuristic(i1, i2, dest_x, dest_y):
        dx, dy = abs(i1 - dest_x), abs(i2 - dest_y)
        return 10 * (dx + dy) + (14 - 2 * 10) * min(dx, dy)

    row = [-1, 1, 0, 0, -1, -1, 1, 1]
    col = [0, 0, -1, 1, 1, -1, -1, 1]

    rock_height = 0

    destination_reached = False
    hrstc = heuristic(start_x, start_y, dest_x, dest_y)

    if search_space[start_x][start_y] < 0:
        rock_height = abs(search_space[start_x][start_y])

    open_q = PriorityQueue()
    # (f_n, x, y, rock_height, step_cost, g_n)
    open_q.put((0, start_x, start_y, rock_height, 0, 0))
    open_q_dict = {}
    open_q_dict[(start_x, start_y)] = 0

    closed_q_dict = {}

    # open_q is a priority queue.

    while not open_q.empty() and not destination_reached:

        f_n, x, y, rock_height, step_cost, g_n = open_q.get()

        # print('open_q_dict ', open_q_dict)
        # print('closed_q_dict ', closed_q_dict)

        # remove it from the open_q and put it in the closed q
        if (x, y) in open_q_dict:
            del open_q_dict[(x, y)]
        closed_q_dict[(x, y)] = g_n

        # print('open_q_dict after removing ', open_q_dict)
        # print('closed_q_dict ', closed_q_dict)

        if x == dest_x and y == dest_y:
            #print(g_n)
            t1, t2 = parent[x][y]

            path = str(y) + ',' + str(x)
            # print('path ',path)
            while t1 != -1:
                path = str(t2) + ',' + str(t1) + ' ' + path

                t1, t2 = parent[t1][t2]
            destination_reached = True
            path = path + '\n'
            # print(path)
            f = open('output.txt', 'a')
            f.write(path)

            break

        for i in range(8):
            r = x + row[i]
            c = y + col[i]

            if i < 4:
                dist = 10
            else:
                dist = 14

            # child_in_open_q,child_in_closed_q=False,False
            mud_level_destination, height_change = 0, 0

            if r >= 0 and r < max_row and c >= 0 and c < max_col:
                hrstc = heuristic(r, c, dest_x, dest_y)

                if search_space[r][c] < 0:
                    height_change = abs(rock_height - abs(search_space[r][c]))
                    mud_level_destination = 0

                    cost = g_n + dist + height_change + mud_level_destination
                    rh = abs(search_space[r][c])
                else:
                    height_change = rock_height
                    mud_level_destination = search_space[r][c]

                    cost = g_n + dist + height_change + mud_level_destination
                    rh = 0

                if height_change <= max_rock_height:
                    child = (cost + hrstc, r, c, rh, step_cost + dist, cost)

                    if (r, c) in open_q_dict:
                        if open_q_dict[(r, c)] > cost:
                            del open_q_dict[(r, c)]

                    if (r, c) in closed_q_dict:
                        if closed_q_dict[(r, c)] > cost:
                            del closed_q_dict[(r,c)]

                    if (r, c) not in open_q_dict and (r, c) not in closed_q_dict:
                        open_q_dict[(r, c)] = cost
                        open_q.put(child)
                        parent[r][c] = (x, y)


    if not destination_reached:
        path = 'FAIL\n'
        f = open('output.txt', 'a')
        f.write(path)


def UCS(search_space, start_x, start_y, dest_x, dest_y, max_row, max_col, parent, max_rock_height):
    # print(start_x,start_y)
    # print(search_space[start_x][start_y])
    row = [-1, 1, 0, 0, -1, -1, 1, 1]
    col = [0, 0, -1, 1, 1, -1, -1, 1]

    rock_height = 0

    destination_reached = False

    # if the start location is a rock then we change its height.
    if search_space[start_x][start_y] < 0:
        rock_height = abs(search_space[start_x][start_y])

    open_q = PriorityQueue()
    # (step_cost,x,y,rock_height)
    open_q.put((0, start_x, start_y, rock_height))
    open_q_dict = {}
    open_q_dict[(start_x, start_y)] = 0

    closed_q_dict = {}

    # open_q is a priority queue.

    while not open_q.empty():

        step_cost, x, y, rock_height = open_q.get()

        if (x, y) in open_q_dict:
            del open_q_dict[(x, y)]

        if x == dest_x and y == dest_y:

            t1, t2 = parent[x][y]
            #print("my cost ", step_cost)
            path = str(y) + ',' + str(x)
            # print('path ',path)
            while t1 != -1:
                path = str(t2) + ',' + str(t1) + ' ' + path
                t1, t2 = parent[t1][t2]
            destination_reached = True
            path = path + '\n'
            # print(path)
            f = open('output.txt', 'a')
            f.write(path)

            break

        for i in range(8):
            r = x + row[i]
            c = y + col[i]

            if i < 4:
                dist = 10
            else:
                dist = 14

            # child_in_open_q,child_in_closed_q=False,False
            height_change = 0

            if r >= 0 and r < max_row and c >= 0 and c < max_col:

                if search_space[r][c] < 0:
                    height_change = abs(rock_height - abs(search_space[r][c]))
                    rh = abs(search_space[r][c])
                else:
                    height_change = rock_height
                    rh = 0

                if height_change <= max_rock_height:
                    score = step_cost + dist
                    child = (score, r, c, rh)

                    if (r, c) not in open_q_dict and (r, c) not in closed_q_dict:
                        open_q_dict[(r, c)] = score
                        open_q.put(child)
                        parent[r][c] = (x, y)

                    elif (r, c) in open_q_dict:

                        if open_q_dict[(r, c)] > score:
                            open_q_dict[(r, c)] = score
                            open_q.put(child)
                            parent[r][c] = (x, y)
                            # break

                    elif (r, c) in closed_q_dict:
                        if closed_q_dict[(r, c)] > score:
                            del closed_q_dict[(r, c)]
                            open_q.put(child)
                            parent[r][c] = (x, y)
                            # break

        closed_q_dict[(x, y)] = step_cost

    if not destination_reached:
        path = 'FAIL\n'
        f = open('output.txt', 'a')
        f.write(path)


def BFS(search_space, start_x, start_y, dest_x, dest_y, max_row, max_col, parent, max_rock_height):
    # print(search_space)

    visited = set()
    row = [-1, 1, 0, 0, -1, -1, 1, 1]
    col = [0, 0, -1, 1, 1, -1, -1, 1]

    rock_height = 0

    destination_reached = False

    # if the start location is a rock then we change its height.
    if search_space[start_x][start_y] < 0:
        rock_height = abs(search_space[start_x][start_y])

    # [start_x,start_y,rock_height,step_cost])
    q = [[start_x, start_y, rock_height, 0]]

    # in this queue we are appending from the end and poping from the begining.
    while q:
        # print(q)
        x, y, rock_height, step_cost = q.pop(0)
        visited.add((x, y))

        if x == dest_x and y == dest_y:
            t1, t2 = parent[x][y]
            #print("my cost ", step_cost)
            path = str(y) + ',' + str(x)
            while t1 != -1:
                path = str(t2) + ',' + str(t1) + ' ' + path
                t1, t2 = parent[t1][t2]
            destination_reached = True
            path = path + '\n'
            f = open('output.txt', 'a')
            f.write(path)
            break

        for i in range(8):
            r = x + row[i]
            c = y + col[i]

            height_change = 0
            if r >= 0 and r < max_row and c >= 0 and c < max_col and (r, c) not in visited:

                if search_space[r][c] < 0:
                    height_change = abs(rock_height - abs(search_space[r][c]))
                    rh = abs(search_space[r][c])
                else:
                    height_change = rock_height
                    rh = 0
                if height_change <= max_rock_height:
                    visited.add((r, c))

                    parent[r][c] = (x, y)

                    q.append([r, c, rh, step_cost + 1])

    if not destination_reached:
        path = 'FAIL\n'
        f = open('output.txt', 'a')
        f.write(path)


def preprocess():

    with open("input.txt", 'r') as file:
        search_algorithm = file.readline().rstrip()
        # print('search_algorithm ', search_algorithm)
        dimension = tuple(map(int, file.readline().split()))
        max_col, max_row = dimension[0], dimension[1]
        # print('colums ', max_col, 'rows ', max_row)
        start_location = tuple(map(int, file.readline().split()))
        # print('start_location ', start_location)
        max_rock_height = int(file.readline())
        # print('max_rock_height ', max_rock_height)
        no_of_destinations = int(file.readline())
        # print('no_of_destinations ',no_of_destinations)
        destinations = []
        for _ in range(no_of_destinations):
            destinations.append(tuple(map(int, file.readline().split())))
        # print('destinations ', destinations)
        search_space = []
        for line in file:
            search_space.append(tuple(map(int, line.split())))
        # print('search_space ',search_space[33][82],search_space[32][83])
        return search_algorithm, max_col, max_row, start_location, max_rock_height, no_of_destinations, destinations, search_space


def main():
    search_algorithm, max_col, max_row, start_location, max_rock_height, no_of_destinations, destinations, search_space = preprocess()
    # print(max_col,max_row)
    if search_algorithm == "BFS":
        # start_time = t.time()
        for i in destinations:
            # visited=[[False for _ in range(max_col)]for _ in range(max_row)]
            parent = [[(-1, -1) for _ in range(max_col)] for _ in range(max_row)]
            BFS(search_space, start_location[1], start_location[0], i[1], i[0], max_row, max_col, parent,
                max_rock_height)
            # BFS(search_space,start_location[1],start_location[0],i[1],i[0],max_row,max_col,max_rock_height)

        # end_time = t.time()
        # print("TIME ", end_time - start_time)

    elif search_algorithm == "UCS":
        # start_time = t.time()
        for i in destinations:
            # search_space,start_x,start_y,dest_x,dest_y,max_row,max_col,max_rock_height
            parent = [[(-1, -1) for _ in range(max_col)] for _ in range(max_row)]
            UCS(search_space, start_location[1], start_location[0], i[1], i[0], max_row, max_col, parent,
                max_rock_height)
        # end_time = t.time()
        # print("TIME ", end_time - start_time)

    elif search_algorithm == "A*":
        # start_time = t.time()
        for i in destinations:
            parent = [[(-1, -1) for _ in range(max_col)] for _ in range(max_row)]
            ASTAR(search_space, start_location[1], start_location[0], i[1], i[0], max_row, max_col, parent,
                  max_rock_height)
        # end_time = t.time()
        # print("TIME ", end_time - start_time)


main()
