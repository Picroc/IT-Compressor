class Tree(object):
    def __init__(self):
        self.left = None
        self.right = None
        self.data = None


def print_tree(tree=Tree(), lvl=0, code=''):
    if tree.data is not None:
        print('\t' * lvl, tree.data, ' - ' + code)
    else:
        print('\t' * lvl, '*---|')

    if tree.left is not None:
        print_tree(tree.left, lvl + 1, code + '0')

    if tree.right is not None:
        print_tree(tree.right, lvl + 1, code + '1')


class PriorityQueue(object):
    def __init__(self, arr=()):
        self.queue = arr

    def __str__(self):
        return ' '.join([str(i[1]) for i in self.queue])

    def isEmpty(self):
        return len(self.queue) == []

    def isOneElement(self):
        return len(self.queue) - 1 == 0

    def insert(self, data):
        self.queue.append(data)

    def delete(self):
        try:
            min = 0
            for i in range(len(self.queue)-1, 0, -1):
                if self.queue[i][1] < self.queue[min][1]:
                    min = i
            item = self.queue[min]
            del self.queue[min]
            return item
        except IndexError:
            print()
            exit()

def huffman(alphabet):
    queue = PriorityQueue(alphabet)

    while not queue.isOneElement():
        newTree = Tree()
        newTree.right = Tree()
        newTree.left = Tree()

        right_element = queue.delete()
        left_element = queue.delete()

        if isinstance(right_element[0], Tree):
            newTree.right = right_element[0]
        else:
            newTree.right.data = right_element

        if isinstance(left_element[0], Tree):
            newTree.left = left_element[0]
        else:
            newTree.left.data = left_element

        queue.insert((newTree, right_element[1] + left_element[1]))

    return queue.delete()[0]

arr = [('A', 40), ('B', 10), ('C', 20), ('D', 10), ('E', 20)]

tree = huffman(arr)
print(tree)
print_tree(tree)
