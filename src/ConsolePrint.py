import numpy as np


def print_tree(root, agg_function, p, show_id=False):
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

    for i in range(height - 1, -1, -1):

        for node in tree[i]:
            child_location_sum = 0
            for child in node.children:
                child_location_sum += child.location
            curr_node_location = int(child_location_sum / len(node.children))
            node.location = curr_node_location

    for height in list(tree.keys()):
        for node in tree[height]:
            arr_print[height][node.location] = node
            if node.Q_opponent == -1:
                size_nodes.append(len(str('[{:.0f},{:.0f},{:.0f}]'.format(node.utility_opponent, node.utility_proponent,
                                                              node.Q_aggregated))))
            else:
                size_nodes.append(len(str('[{:.0f},{:.0f},{:.0f},{:.2s}]'.format(node.Q_opponent, node.Q_proponent, node.Q_aggregated, node.id))))

    size_space = max(size_nodes)
    space = ' ' * size_space # if we get the size of the bigger string will be better?

    print('---------------------------------------------------------------')
    print(1 * space, 'Policy type: {} | p = {}'.format(agg_function, p))
    if show_id:
        print(1 * space, 'The caption for each is the following  >  [opponent, proponent, aggregated, id]')
    else:
        print(1 * space, 'The caption for each is the following  >  [opponent, proponent, aggregated]')
    print()

    # PRINTING THE NODES IN ORDER
    for row in arr_print:
        for node in row:
            if node == '-':
                print(space, end='')
            else:
                if node.Q_opponent == -1:
                    if show_id:
                        sentence = ('[{:.0f},{:.0f},{:.0f},{:.2s}]'.format(node.utility_opponent, node.utility_proponent,
                                                              node.Q_aggregated, node.id))
                    else:
                        sentence = ('[{:.0f},{:.0f},{:.0f}]'.format(node.utility_opponent, node.utility_proponent,
                                                              node.Q_aggregated))
                    size_node = len(sentence)
                    centering_value = np.floor((size_space - size_node) / 2)
                    rest = (size_space - size_node) % 2

                else:
                    if show_id:
                        sentence = ('[{:.0f},{:.0f},{:.0f},{:.2s}]'.format(node.Q_opponent, node.Q_proponent, node.Q_aggregated, node.id))
                    else:
                        sentence = ('[{:.0f},{:.0f},{:.0f}]'.format(node.Q_opponent, node.Q_proponent, node.Q_aggregated))
                    size_node = len(sentence)
                    centering_value = np.floor((size_space - size_node)/2)
                    rest = (size_space - size_node) % 2

                ident_space_ini = ' ' * int(centering_value)
                ident_space_end = ' ' * int((centering_value+rest))
                print(ident_space_ini, end='')
                print(sentence, end='')
                print(ident_space_end, end='')

        print()

    print()
