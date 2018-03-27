import socket
import logging
import os
import signal


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
	signal.signal(signal.SIGCHLD, grim_reaper)
	child_process_number = 10
	for i in range(child_process_number):
		pid = os.fork()
		if pid == 0:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect(('localhost', 2007))
			sock.send(str('hello world from client').encode('utf-8'))
			szBuf = sock.recv(4096)
			print("recv:{}".format(szBuf.decode('utf-8')))
			sock.close()
			print("end of connect")
			break
		else:
			logging.info("current child_process_number:{}".format(i))