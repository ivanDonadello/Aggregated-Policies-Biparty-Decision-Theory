from collections import Counter
import numpy as np


def print_tree(root, agg_function, p):
    tree = root.dict_tree

    height = list(tree.keys())[-1]
    lenght_leaf = len(tree[height])
    N = int(lenght_leaf * 3)
    arr_print = np.full([height+1, N],"-", dtype=np.object)
    idx_matrix = []
    arr = np.arange(N)
    #print(arr)

    for i in range(height+1):
        arr = np.arange(N)
        points = len(tree[i])
        idx_array = []

        N = len(arr)  # 7
        val = ((1 / (points + 1)) * (N - points))
        val = int(val)
        idx_array.append(val)

        for i in range(points - 1):
            arr = arr[val + 1:]
            val = ((1 / (points + 1)) * (N))
            val = int(val)
            #print('val = ', arr[val])
            idx_array.append(arr[val])
        idx_matrix.append(idx_array)

    #print(idx_matrix)

    for _x, x in enumerate(idx_matrix):
        for _y ,y in enumerate(x):
            node = tree[_x][_y]
            arr_print[_x][y] = node

    # print(arr_print)

    space = '         '  # if we get the size of the bigger string will be better?
    # space = ' '  # size for ID

    print('---------------------------------------------------------------')
    #print(int((N/4)) * space, 'Policy type: {} | p = {}'.format(agg_function, p))
    print(1 * space, 'Policy type: {} | p = {}'.format(agg_function, p))
    print(1 * space, 'The caption for each is the following  >  [opponent, proponent, aggregated, id]')
    print()

    # PRINTING THE NODES IN ORDER
    for row in arr_print:
        for node in row:
            if node == '-':
                print(space, end='')
            else:
                if node.Q_opponent == -1:
                    result = ('[{:.0f},{:.0f},{:.0f},{:.2s}]'.format(node.utility_opponent, node.utility_proponent,
                                                              node.Q_aggregated, node.id))
                else:
                    result = ('[{:.0f},{:.0f},{:.0f},{:.2s}]'.format(node.Q_opponent, node.Q_proponent, node.Q_aggregated, node.id))
                # result= node.id
                print(result, end='')

        print()

    print()

    # counter_row = Counter(root.row_count)
    # print(counter_row)
    # counter_row_max = max(counter_row.values())
    # print(counter_row_max)
    # mlist = [[] for i in range(len(np.unique(root.row_count)))]
    # print(mlist)