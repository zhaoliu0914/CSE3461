import json
import socket
import logging
import configparser


def look_up_config_file(level: str):
    logging_level = logging.INFO
    if level == "DEBUG":
        logging_level = logging.DEBUG
    elif level == "WARNING":
        logging_level = logging.WARNING
    elif level == "ERROR":
        logging_level = logging.ERROR
    elif level == "FATAL":
        logging_level = logging.FATAL

    return logging_level


if __name__ == '__main__':
    # set up config file
    config = configparser.ConfigParser()
    config.read("server-configuration.ini", encoding="utf-8")

    # print("The content of configuration file is:")
    server_host = config["project2"]["serverHost"]
    server_port = config["project2"]["serverPort"]

    log_filename = config["logging"]["logFile"]
    log_level = config["logging"]["logLevel"]
    log_file_mode = config["logging"]["logFileMode"]

    logging_level = look_up_config_file(log_level)

    # set up log file
    logging.basicConfig(filename=log_filename, level=logging_level, filemode=log_file_mode)

    print(f"server_host = {server_host}")
    print(f"server_port = {server_port}")
    print(f"log_filename = {log_filename}")
    print(f"log_level = {log_level}")
    print(f"log_file_mode = {log_file_mode}")
    logging.info(f"server_host = {server_host}")
    logging.info(f"server_port = {server_port}")
    logging.info(f"log_filename = {log_filename}")
    logging.info(f"log_level = {log_level}")
    logging.info(f"log_file_mode = {log_file_mode}")

    print("Start a Server:")
    print(f"IP Address: {server_host}")
    print(f"Port: {server_port}")
    print("Waiting for connection.........")
    logging.info("Start a Server:")
    logging.info(f"IP Address: {server_host}")
    logging.info(f"Port: {server_port}")
    logging.info("Waiting for connection.........")

    server_address = (server_host, int(server_port))

    # Set up socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(server_address)
    server.listen(5)

    # Wait for an incoming connection.
    # Return a new socket representing the connection, and the address of the client.
    connection, client_address = server.accept()

    print(f"Connection accepted from {client_address}")
    logging.info(f"Connection accepted from {client_address}")

    while True:
        # Keep looking and receiving JSON message from client until receiving "QUITTING" command
        # If command from client is "QUITTING", then the "response" element is "QUITTING" and "parameter" element is empty.
        client_data = connection.recv(1024)
        client_data = client_data.decode(encoding="utf-8")

        client_json = json.loads(client_data)
        client_command = client_json["command"]
        client_parameter = client_json["parameter"]

        print(f"The message received from client : {client_data}")
        print(f"Client command: {client_command}")
        print(f"Client parameter: {client_parameter}")
        logging.info(f"Client message: {client_data}")
        logging.info(f"Client command: {client_command}")
        logging.info(f"Client parameter: {client_parameter}")

        if client_command == "QUITTING":
            client_parameter = ""
        else:
            client_parameter = "Server received: " + client_parameter

        # Response a JSON message to client with original command and parameter which adds "Server received: " on it.
        message = {"response": client_command,
                   "parameter": client_parameter}
        message_json = json.dumps(message)
        message_json = message_json.encode(encoding="utf-8")

        connection.send(message_json)

        print(f"The message send to Client: {message_json}")
        logging.info(f"The message send to Client: {message_json}")

        if client_command == "QUITTING":
            print("Receiving a quit command!!!")
            print("Stop running this Server!!!")
            logging.info("Receiving a quit command!!!")
            logging.info("Stop running this Server.")
            break

    connection.close()
    server.close()