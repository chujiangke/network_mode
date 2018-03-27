import socket
import logging


def handle(client_socket, client_address):
	while True:
		data = client_socket.recv(4096)
		if data:
			send = client_socket.send(data)
			logging.info("data:{}".format(data))
			logging.info("send:{}".format(send))
		else:
			print("disconnect:{}".format(client_address))
			client_socket.close()
			break


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
	while True:
		connection, client_address = server.accept()
		logging.info("connection:{} client_address:{}".format(connection, client_address))
		#print "connection", connection
		print( "%s connect. " %str(client_address) )
		handle(connection, client_address)