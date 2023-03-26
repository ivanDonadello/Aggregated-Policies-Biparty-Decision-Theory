from collections import Counter
import numpy as np


def old_print(root, agg_function, p):
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

def print_tree(root, agg_function, p):
    tree = root.dict_tree
    size_nodes = []
    # tree height and the id for the leaves values
    height = list(tree)[-1]
    points = len(tree[height])
    width = int(points * 2) + 1
    leaf_array = tree[height]

    # array with zeroes to store the nodes
    arr_print = np.full([height + 1, width], "-", dtype=object)
    idx_array = []
    arr = np.arange(width)

    N = len(arr)  # 7
    val = ((1 / (points + 1)) * (N - points))
    val = int(val)
    idx_array.append(val)
    leaf_array[0].location = val

    for i in range(1, points):
        arr = arr[val + 1:]
        val = ((1 / (points + 1)) * (N))
        val = int(val)
        leaf_array[i].location = arr[val]

    #     idx_array.append(arr[val])
    # idx_matrix.append(idx_array)
    #
    # print(idx_matrix)

    # print(idx_matrix)
    # ConsolePrint.print_tree(bdt.root, 'bimaximax', -1)
    for i in range(height - 1, -1, -1):

        for node in tree[i]:
            child_location_sum = 0
            for child in node.children:
                child_location_sum += child.location
            curr_node_location = int(child_location_sum / len(node.children))
            node.location = curr_node_location

    # test_node = bdt.root.dict_tree[3][1]
    # print(test_node.id,test_node.children, test_node.location)

    for height in list(tree.keys()):
        for node in tree[height]:
            arr_print[height][node.location] = node
            if node.Q_opponent == -1:
                size_nodes.append(len(str('[{:.0f},{:.0f},{:.0f}]'.format(node.utility_opponent, node.utility_proponent,
                                                              node.Q_aggregated)))-1)
            else:
                size_nodes.append(len(str('[{:.0f},{:.0f},{:.0f}]'.format(node.Q_opponent, node.Q_proponent, node.Q_aggregated))))

    size_space = max(size_nodes)
    space = ' ' * size_space # if we get the size of the bigger string will be better?
    # space = ' '  # size for ID

    print('---------------------------------------------------------------')
    # print(int((N/4)) * space, 'Policy type: {} | p = {}'.format(agg_function, p))
    # print(1 * space, 'Policy type: {} | p = {}'.format(agg_function, p))
    print(1 * space, 'The caption for each is the following  >  [opponent, proponent, aggregated, id]')
    print()

    # PRINTING THE NODES IN ORDER
    for row in arr_print:
        for node in row:
            if node == '-':
                print(space, end='')
            else:
                if node.Q_opponent == -1:
                    result = ('[{:.0f},{:.0f},{:.0f}]'.format(node.utility_opponent, node.utility_proponent,
                                                              node.Q_aggregated))
                    # result = ('[{:.0f},{:.0f},{:.0f},{:.2s}]'.format(node.utility_opponent, node.utility_proponent,
                    #                                                  node.Q_aggregated, node.id))
                else:
                    # result = ('[{:.0f},{:.0f},{:.0f},{:.2s}]'.format(node.Q_opponent, node.Q_proponent, node.Q_aggregated, node.id))
                    result = ('[{:.0f},{:.0f},{:.0f}]'.format(node.Q_opponent, node.Q_proponent, node.Q_aggregated))
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