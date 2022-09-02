from http import client
import socket
from functools import reduce
from functools import total_ordering
from math import log

class NodeTree(object):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def children(self):
        return (self.left, self.right)

    def nodes(self):
        return (self.left, self.right)

    def __str__(self):
        return '%s_%s' % (self.left, self.right)

# Main function implementing huffman coding
def huffman_code_tree(node, left=True, binString=''):
    if type(node) is str:
        return {node: binString}
    (l, r) = node.children()
    d = dict()
    d.update(huffman_code_tree(l, True, binString + '0'))
    d.update(huffman_code_tree(r, False, binString + '1'))
    return d

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

text = ' '
while True:
    choice = int(input("Choose --> Enter a message (1) or exit (2): "))
    if choice == 1:
        string = str(input("Enter your text: "))
        strlen = len(string)

        # Calculating frequency
        freq = {}
        for c in string:
            i = ord(c) - 65
            if i in freq:
                freq[c] += 1
            else:
                freq[c] = 1

        freq2 = [0]*256
        for c in string:
            j = ord(c)
            freq2[j] += freq[c]

        freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        nodes = freq

        while len(nodes) > 1:
            (key1, c1) = nodes[-1]
            (key2, c2) = nodes[-2]
            nodes = nodes[:-2]
            node = NodeTree(key1, key2)
            nodes.append((node, c1 + c2))

        nodes = sorted(nodes, key=lambda x: x[1], reverse=True)
        huffmanCode = huffman_code_tree(nodes[0][0])

        # efficiency of compression
        res = 0.00
        for i in range(256):
            if (freq2[i] != 0):
                pi = round(freq2[i]/strlen, 4)
                tlog = round(log(strlen/freq2[i], 2), 4)
                res += ((pi)*tlog)
                res = round(res, 4)
                print(chr(i) + " " + str(res))
                # send(str(chr(i) + " " + str(res)))
                temp = huffmanCode[chr(i)]
                fres = chr(i) + " " + str(res) + " " + temp
                send(str(fres))
                # send(huffmanCode(chr(i)))
        rat = round((strlen*8)/(res*strlen), 4)
        print("Compression ratio =  %.4f" % rat)
        send("Compression Ratio: " + (str(rat)))
    elif choice == 2:
        send(DISCONNECT_MESSAGE)
        break;
