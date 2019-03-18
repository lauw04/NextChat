import multiprocessing
import socket
 
def handle_com(con, addr):
    print("process identity %r" % (addr,))
    try:
        print("connection information %r at %r", con, addr)
        while True:
            data = con.recv(1024)
            if data == "":
                print("Socket closed by client ?")
                break
            print("Received data %r", data)
            con.sendall(data)
            print("Sent data")
    except:
        print("Problem in request ?")
    #finally:
        #print("finally : Closed socket")
        #con.close()
 
 
if __name__ == "__main__":
    try:
        socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.bind(("0.0.0.0",8888))
        socket.listen(1)
        print("Listening")
        while True:
            con, addr = socket.accept()
            print("Got a new connection")
            process = multiprocessing.Process(target=handle_com, args=(con, addr))
            process.daemon = True
            process.start()
            print("process %r", process)

    except:
        print("Unexpected exception")
    finally:
        print("Shutting down")
        for process in multiprocessing.active_children():
            print("Shutting down process %r", process)
            process.terminate()
            process.join()
    print("END")
