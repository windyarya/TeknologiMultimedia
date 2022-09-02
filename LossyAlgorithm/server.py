import matplotlib.pyplot as plt
import numpy as np
import time
from PIL import Image
import socket 
import threading
from functools import reduce

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def imgcomp(fname):
    img = Image.open(fname)
    imggray = img.convert('LA')

    imgmat = np.array(list(imggray.getdata(band=0)), float)
    imgmat.shape = (imggray.size[1], imggray.size[0])
    imgmat = np.matrix(imgmat)

    U, sigma, V = np.linalg.svd(imgmat)
    reconstimg = np.matrix(U[:, :1]) * np.diag(sigma[:1]) * np.matrix(V[:1, :])

    reconstimg = np.matrix(U[:, :100]) * np.diag(sigma[:100]) * np.matrix(V[:100, :])
    plt.imshow(reconstimg, cmap='gray')
    plt.show()
    plt.imsave('compressed.JPG', reconstimg, cmap='gray')
    return 1

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                # print("masuk")
                break;
            flag = imgcomp(msg)
            if (flag == 1):
                msg2 = "Compression completed"
                print(f"[{addr}] {msg2}")
            conn.send(" ".encode(FORMAT))

    conn.close()
        
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
    
    thread.close()

print("[STARTING] server is starting...")
start()