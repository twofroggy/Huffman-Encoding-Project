#add try-error statement to make sure the filename ends in txt
#clear text files before writing to them

import sys
import collections

original_stdout = sys.stdout
while True:
    filename = input(
        "Enter your the filepath to the file, making sure to end your input with '.txt', for example: \n/Users/username/CS430/project.txt\n"
    )  #make sure it ends in txt
    if filename.endswith('.txt'):
        break

with open(filename) as f:
    contents = f.read()
    #print(contents)
f.close()


def count_char(text):
    count = {}
    print("\n LISTING FREQ OF EACH CHARACTER: \n")
    for ch in text:
        # If char already in dictionary increment count
        # otherwise add char as key and 1 as value
        if ch in count:
            count[ch] += 1
        else:
            count[ch] = 1
    for k, v in count.items():
        print('Character {} occurs {} times'.format(k, v))
    return (count)


count_dict = count_char(contents)

chars = list(count_dict.keys())
freq = list(count_dict.values())
''''
print("\n LIST OF chars IN ORDER OF APPEARANCE: \n")
print('chars:', chars) 
print("\n LIST OF frq IN ORDER OF APPEARANCE: \n")
print('freq:', freq)
'''


# declare a huffman node with attributes that we will use later on 
class node:
    def __init__(self, freq, symbol, left=None, right=None):
        # frequency of each unique character
        self.freq = freq

        # the unique character itself 
        self.symbol = symbol

        # left node of current node
        self.left = left

        # right node of current node
        self.right = right

        # huffman tree direction (in binary form)
        self.huff = ''


final_dict = {}

# utility function to print huffman codes for all symbols in the newly created Huffman tree 
def printNodes(node, val=''):
    # set the huffman code for current node to another variable
    newVal = val + str(node.huff)

    # if node is not an edge node then traverse inside it
    if (node.left):
        printNodes(node.left, newVal)

    if (node.right):
        printNodes(node.right, newVal)

        # if node is edge node then display its huffman code
    if (not node.left and not node.right):
        print(f"{node.symbol} -> {newVal}")
        final_dict[node.symbol] = newVal


# make an empty list that will include the unused nodes
nodes = []

# converting characters and frequencies into huffman tree nodes and append it into a list 
for x in range(len(chars)):
    nodes.append(node(freq[x], chars[x]))

while len(nodes) > 1:
    # sort the nodes that we appended into a list before in ascending order based on freq
    nodes = sorted(nodes, key=lambda x: x.freq)

    # pick 2 smallest nodes of the nodes array by choosing the first 2 
    left = nodes[0]
    right = nodes[1]

    # add directional value to the smallest nodes
    left.huff = 0
    right.huff = 1

    # sum up the 2 smallest nodes to create its parent node 
    newNode = node(left.freq + right.freq, left.symbol + right.symbol, left,
                   right)

    # delete the 2 smallest nodes and add their parent as new node among others for cycle to repeat 
    nodes.remove(left)
    nodes.remove(right)
    nodes.append(newNode)

print("\nDictionary of Codewords: \n")
printNodes(nodes[0])

while True:
    filename_encoded = input(
        "\nWhat would you like to name the ENCODED txt file? Make sure to end your input in with '.txt'. \n"
    )  # make sure it ends in txt
    if filename_encoded.endswith('.txt'):
        break


def encoder(contents):
    with open(filename_encoded, 'w') as f:
        sys.stdout = f
        for letter in contents:
            #print(letter)
            try:
                print(final_dict[letter], end='')

            except:
                if letter == "\n":
                    print(letter)
                else:
                    print(letter, end='')
    f.close()
    sys.stdout = original_stdout


encoder(contents)

# print the binary tree
huffman_dict = dict(zip(final_dict.values(), final_dict.keys()))


def huffmanDecode(dictionary, text):

    with open(text) as f:
        text = f.read()
        f.close()
    # print("\nencoded file")
    # print(text)

    while True:
        filename_decoded = input(
            "\nWhat would you like to name the DECODED txt file? Make sure to end your input in with '.txt'. \n"
        )  # make sure it ends in txt
        if filename_decoded.endswith('.txt'):
            break

    # print(contents)
    res = ""
    while text:
        for k in dictionary:
            #print(k)
            if text.startswith(k):
                res += dictionary[k]
                text = text[len(k):]
                #print(res)
    with open(filename_decoded, 'w') as f:
        sys.stdout = f 
        print(res)
        f.close()
    sys.stdout = original_stdout

# decode the txt file back
huffmanDecode(huffman_dict, filename_encoded)




# i made this to start from scratch. It is separate from the previous tree files
import math

keys = []
for i in range(len(chars)):

    if chars[i] == '\n':
        chars[i] = 'newline character'
    if chars[i] == ' ':
        chars[i] = 'space character'
    val = str(chars[i]) + ": " + str(freq[i])
    keys.append(val)
'''
try:
  final_dict['newline character'] = final_dict.pop('\n')
  final_dict['space character'] = final_dict.pop(' ')
  print(str(final_dict))
except:
  print('ERRRRROR')
'''
#keys=['a: 45', 'c: 12', 'b: 13', 'f: 5', 'e: 9', 'd: 16']
values = list(final_dict.values())
frequencies = freq.copy()
res = {keys[i]: frequencies[i] for i in range(len(keys))}
nodes = []
#length is the length of the binary code
length = len(max(values, key=len))
#print(length)
joins = 0
joins2 = 0
nodes_list = []  #alisha 

while len(res) > 0 and length >= 0:
    print('\n\n START HERE! LENGTH: ' + str(length))
    print('\nDICTIONARY BEFORE: ' + str(res))
    print(length)
    joins = joins2  #alisha
    #print(length)
    counter = 0  #joinings per level
    #max_counter=joins
    for val in values:
        if len(val) == length:
            #max_counter+=1
            joins += 1
    joins = math.ceil(joins / 2)  #alisha

    #alisha
    joins2 = 0
    possible_joins = []
    actual_joins = []

    for val in values:
        if len(val) == length:
            possible_joins.append(val)
    print('\nPOSSIBLE JOINS: ', possible_joins)

    print("\njoins at level ", length, ": ", str(joins))

    # for the very last join node, total sum of freqs
    if len(res) == 2:
        check = all(item in nodes for item in nodes_list)
        if check:
            nodes_list = []
        else:
            nodes = nodes_list + nodes
            nodes_list = []
        #find elements with min frequency
        key = min(res, key=res.get)
        #print("\nkey 1: ", str(key))
        nodes_list.append(key)
        new_node = res[key]
        del res[key]

        key = min(res, key=res.get)
        #print("\nkey 2: ", str(key))
        nodes_list.append(key)
        new_node += res[key]
        del res[key]

        node_key = "internal node: " + str(new_node)
        res[node_key] = new_node
        nodes = nodes_list + nodes
        print('finished loop')
        continue

    if len(res) == 1:
        nodes = [list(res.keys())[0]] + nodes
        #print(nodes)
        break 
    counter2 = 0
    for val in values:
        if len(val) == length + 1:
            counter2 += 1
    if counter2 > 0:
        nodes_list = []
    for idx, x in enumerate(values):

        #print(x)
        if len(x) == length - 1:
            nodes_list.append('#')
            nodes_list.append('#')
        elif len(x) == length and counter < joins:
            if idx > 0:
                if int(values[idx - 1]) == int(x) - 1 and len(
                        values[idx]) == len(x):
                    continue
            #find elements with min frequency
            key = min(res, key=res.get)
            #print("\nkey 1: ", str(key))
            nodes_list.append(key)
            new_node = res[key]
            del res[key]

            key = min(res, key=res.get)
            #print("\nkey 2: ", str(key))
            nodes_list.append(key)
            new_node += res[key]
            del res[key]

            node_key = "internal node: " + str(new_node)
            print('\nvalue that causes join: ', x)
            actual_joins.append(x)
            #counter4=1
            while node_key in res:
                node_key = node_key + ' '
            res[node_key] = new_node
            counter += 1
            joins2 += 1  #ADDED
        else:
            if collections.Counter(actual_joins) == collections.Counter(
                    possible_joins) and counter < joins:
                #find elements with min frequency
                key = min(res, key=res.get)
                #print("\nkey 1: ", str(key))
                nodes_list.append(key)
                new_node = res[key]
                del res[key]

                key = min(res, key=res.get)
                #print("\nkey 2: ", str(key))
                nodes_list.append(key)
                new_node += res[key]
                del res[key]

                node_key = "internal node: " + str(new_node)
                print('\nvalue that causes join: ', x)

                counter3 = 0
                for val in values:
                    if len(val) <= length:
                        counter3 += 1
                if counter3 == 0:
                    pass
                    #nodes = nodes_list + nodes
                    #print('\nnodes$$: ', nodes_list)
                if counter3 != 0:
                    actual_joins.append(x)
                #counter4=1
                while node_key in res:
                    node_key = node_key + ' '
                res[node_key] = new_node
                counter += 1
                joins2 += 1  #ADDED

    #joins = joins2 tiff
    print('\nDICTIONARY AFTER: ' + str(res))
    counter3 = 0
    for val in values:
        if len(val) == length:
            counter3 += 1
    if counter3 > 0:
        nodes = nodes_list + nodes
        print('\nnodes: ', nodes_list)

    counter3 = 0
    for val in values:
        if len(val) <= length:
            counter3 += 1
    if counter3 == 0:
        nodes = nodes_list + nodes
        print('\nnodes: ', nodes_list)

    #nodes=nodes_list+nodes
    length -= 1
#print(nodes)

#nodes to hashes if they can't be converted to int
from drawtree import draw_level_order
import random
import sys

original_stdout = sys.stdout


def strings_to_ints(nodes):
    
    def randN(N):
        min = pow(10, N - 1)
        max = pow(10, N) - 1
        return random.randint(min, max)

    hashes = []
    nodes2 = []
    for x in nodes:
        if x == '#':
            nodes2.append(x)
            continue
        try:
            replacement = int(x)
        except:
            hash_value = randN(len(x))
            while (hash_value in hashes):
                hash_value = randN(len(x))
            hashes.append(hash_value)
            replacement = hash_value
        nodes2.append(replacement)
    return (nodes2)


print("\nnodes:\n ", nodes)
print("\n")
'''' we need this format to pass into drawtree
nodes=['internal node: 108', 'a:45', 'internal node: 63', '#','#','internal node: 26','internal node: 37', 'b:13','internal node: 13','d:16','internal node: 21','#','#','g:5','internal node: 8','#','#','e:9','c:12','#','#','z:3','f:5', '#','#','#','#'] 
'''

raw_tree = strings_to_ints(nodes)

res = {raw_tree[i]: nodes[i] for i in range(len(raw_tree))}

def raw_to_tree(raw, res):
    string1 = "{"
    for x in raw:
        string1 += str(x)
        string1 += ","
    string1 = string1[:-1]
    string1 += "}"
    #print(string1)
    filename = input(
        "Enter a filename that ends in txt to store the raw tree in: ")
    with open(filename, 'w') as f:
        print("\n")
        sys.stdout = f
        draw_level_order(string1)
        f.close()
        sys.stdout = original_stdout

    f = open(filename, 'r')
    contents = f.read()
    f.close()
    #print(type(contents))

    for k, v in res.items():
        contents = contents.replace(str(k), str(v))
    print(contents)

# run the raw to tree file to print the binary tree
raw_to_tree(raw_tree, res)
