import hashlib

class Tree:
    def __init__(self, input_data):
        self.input_data = input_data
        self.build()

    def build(self):
        self.create_leaf_level()
        self.assign_leafs()

        while len(self.levels[0]) != 1:
            self.add_parent_level()
            self.assign_parents()

    def value_of(self, index):
        if type(index) is not tuple:
            raise TypeError("Only supports indexing with tuple")
        return self.levels[index[0]][index[1]]

    def parent_of(self, index):
        if type(index) is not tuple:
            raise TypeError("Only supports indexing with tuple")
        return (index[0]-1, self.row_index_of_parent(index[1]))

    def right_child_of(self, index):
        if type(index) is not tuple:
            raise TypeError("Only supports indexing with tuple")
        return (index[0]+1, self.row_index_of_right_child(index[1]))

    def left_child_of(self, index):
        if type(index) is not tuple:
            raise TypeError("Only supports indexing with tuple")
        return (index[0]+1, self.row_index_of_left_child(index[1]))

    def is_right_sibling(self, index):
        if type(index) is not tuple:
            raise TypeError("Only supports indexing with tuple")
        return index[1]%2 == 1

    def is_left_sibling(self, index):
        if type(index) is not tuple:
            raise TypeError("Only supports indexing with tuple")
        return index[1]%2 == 0

    def left_node_of(self, index):
        if type(index) is not tuple:
            raise TypeError("Only supports indexing with tuple")
        return (index[0], index[1]-1)

    def right_node_of(self, index):
        if type(index) is not tuple:
            raise TypeError("Only supports indexing with tuple")
        return (index[0], index[1]+1)

    def is_root(self, index):
        if type(index) is not tuple:
            raise TypeError("Only supports indexing with tuple")
        return index == (0, 0)

    def merkle_path_for(self, index):
        if type(index) is not tuple:
            raise TypeError("Only supports indexing with tuple")
        node = index
        result = []
        while not self.is_root(node):
            if self.is_left_sibling(node):
                # Take right
                right_node = self.right_node_of(node)
                result.append('R' + tree.value_of(right_node))
            else:
                # Take left
                left_node = self.left_node_of(node)
                result.append('L' + tree.value_of(left_node))
            node = self.parent_of(node)
        return result

    def bottom_layer_index(self):
        return len(self.levels)-1

    def create_leaf_level(self):
        leaf_count = len(self.input_data)
        leaf_count += 1 if leaf_count%2 != 0 else 0
        self.levels = [[None] * leaf_count]
    
    def assign_leafs(self):
        for i in range(len(self.input_data)):
            val = self.input_data[i].strip()
            self.levels[-1][i] = val

        if self.levels[-1][-1] == None:
            self.levels[-1][-1] = self.levels[-1][-2]

    def add_parent_level(self):
        child_level = self.levels[0]
        parent_length = int(len(child_level) / 2)
        if parent_length == 1:
            pass
        else:
            parent_length += 1 if parent_length%2 != 0 else 0
        self.levels = [[None] * parent_length] + self.levels

    def assign_parents(self):
        for i in range(len(self.levels[0])):
            try:
                left_child = self.levels[1][self.row_index_of_left_child(i)]
                right_child = self.levels[1][self.row_index_of_right_child(i)]
            except IndexError:
                self.levels[0][i] = self.levels[0][i-1]

            self.levels[0][i] = self.create_parent_hash(left_child, right_child)

    def row_index_of_left_child(self, node_index):
        return node_index*2

    def row_index_of_right_child(self, node_index):
        return node_index*2 + 1

    def row_index_of_parent(self, node_index):
        node_index -= 1 if node_index%2 != 0 else 0
        return int(node_index / 2)

    def hash_string(self, string):
        return hashlib.sha1(bytearray.fromhex(string)).hexdigest()

    def create_parent_hash(self, left_child, right_child):
        return self.hash_string(left_child + right_child)

file = open("merkle_2_input.txt", "r")

# Parse file
input_data = []
for i in enumerate(file):
    index = i[0]
    row = i[1].strip()
    if index == 0:
        interesting_leaf_index = int(row)
    elif index == 1:
        interesting_path_depth = int(row) - 1
    else:
        input_data.append(row)

tree = Tree(input_data)

interesting_node = (tree.bottom_layer_index(), interesting_leaf_index)

merkle_path = tree.merkle_path_for(interesting_node)
merkle_root = tree.value_of((0, 0))
merkle_node = merkle_path[::-1][interesting_path_depth]

print("___Merkle node + Merkle root___")
print(merkle_node + merkle_root)

print()

print("___Merkle path___")
for node in merkle_path:
    print(node)

# Hitta root
# Hitta en nod i merkle path på bestämt djup
# Hela merkle path