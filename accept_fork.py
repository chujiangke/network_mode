import socket
import logging
import signal
import os
import time


def handle(client_socket, client_address):
    while True:
        data = client_socket.recv(4096)
        if data:
            send = client_socket.send(data)
            logging.info("data:{}".format(data))
            logging.info("send:{}".format(send))
            time.sleep(20)
        else:
            print("disconnect:{}".format(client_address))
            client_socket.close()
            break


def grim_reaper(signum, frame):
    while True:
        try:
            pid, status = os.waitpid(
                -1,          # Wait for any child process
                 os.WNOHANG  # Do not block and return EWOULDBLOCK error
            )
        except OSError:
            return
    return 
            

if __name__ == '__main__':
    logging.basicConfig(format="%(asctime)s %(name)s %(levelname)s %(message)s",
                        filename='accept_re_write.log',
                        level=logging.INFO)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = ("0.0.0.0", 2007)
    try:
        server.bind(server_host)
        server.listen(5)
    except Exception as e:
        logging.error("bind listen error")
        logging.info("error message：{}".format(e))

    signal.signal(signal.SIGCHLD, grim_reaper)

    while True:
        connection, client_address = server.accept()
        logging.info("connection:{} client_address:{}".format(connection, client_address))
        #print "connection", connection
        pid = os.fork()
        if pid == 0:
            server.close()
            print( "%s connect. " %str(client_address) )
            handle(connection, client_address)
            logging.info("child connection field id:{}".format(connection))
            connection.close()
            os._exit(0)
        else:
            logging.info("parent connection field id:{}".format(connection))
            connection.close()



