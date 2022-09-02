# Kelompok 6 Teknologi Multimedis Kelas B

from http import client
import socket
from functools import reduce
from functools import total_ordering

def decimalToBinary(n):
    return "{0:b}".format(int(n)) 

HEADER = 64
PORT = 5053
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

word = input("Input Word: ")
arr_word = []
arr_word = [0 for i in range(115)]

original_bit = ''
for i in range(len(word)):
    original_bit = original_bit + decimalToBinary(ord(word[i]))

original_bit_length = len(original_bit)
send("Original bits: " + str(original_bit_length))
print("Original bits: " + str(original_bit_length) + " bits")
bit = ''

for i in range(len(word)):
    arr_word[ord(word[i])] = arr_word[ord(word[i])] + 1
    # print(arr_word[ord(word[i])])

max_number = 0

for i in range(115):
    if(arr_word[i] > max_number):
        max_number = arr_word[i]
        # print(max_number)

max_number_binary = len(decimalToBinary(max_number))

for i in range(115):
    if arr_word[i] != 0:
        binary_now = decimalToBinary(arr_word[i])
        while(max_number_binary > len(binary_now)):
            bit =  bit + '0'
            binary_now = binary_now + '1'
            # print(arr_word[i])
            # print(bit)
            # print(binary_now)

        bit = bit + decimalToBinary(arr_word[i])
        bit = bit + decimalToBinary(i)

send("Bits right now: " + str(len(bit)))
print("Decompressed bits: " + str(len(bit)) + " bits")