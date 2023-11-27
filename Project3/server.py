import os
import json
import socket
import logging
import configparser

list_name = ""
items = []
backup_file_name = "backup_list.txt"

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
    server_host = config["project3"]["serverHost"]
    server_port = config["project3"]["serverPort"]

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

    # load backup list
    if os.path.exists(backup_file_name):
        with open(backup_file_name, encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines()]

        list_name = lines[0]

        for line in lines[1:]:
            items.append(line)

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

        server_message = ""

        if client_command == "CREATE":
            if list_name == "":
                list_name = client_parameter
                items = []
                server_message = f"List \"{client_parameter}\" has been created successfully."
            else:
                server_message = f"List \"{list_name}\" has existed in server. Please delete it first then create a new one."

        elif client_command == "DELETE":
            if list_name == "":
                server_message = "There is not any list existing at the server."
            elif list_name != client_parameter:
                server_message = f"List \"{client_parameter}\" does not exist in server. Please run \"show\" command first to find out existing list."
            else:
                list_name = ""
                items = []
                server_message = f"List \"{client_parameter}\" has been removed successfully."

        elif client_command == "ADD":
            if list_name == "":
                server_message = f"There is not any list existing at the server. Please create a list first before add an item."
            else:
                items.append(client_parameter)
                server_message = f"Item \"{client_parameter}\" has been added to the list \"{list_name}\" successfully."

        elif client_command == "REMOVE":
            if list_name == "":
                server_message = f"There is not any list existing at the server. Please create a list first before remove an item."
            elif client_parameter not in items:
                server_message = f"Item \"{client_parameter}\" does not exist in the list. Please add this item to the list before remove it."
            else:
                items.remove(client_parameter)
                server_message = f"Item \"{client_parameter}\" has been removed from the list \"{list_name}\" successfully."

        elif client_command == "SHOW":
            if list_name == "":
                server_message = f"There is not any list existing at the server."
            else:
                server_message = "List: " + list_name + "\n"
                server_message = server_message + "Items: "
                for item in items:
                    server_message = server_message + item + ", "

        elif client_command == "QUIT":
            server_message = ""

            # If exist_list.txt exists, then delete it.
            if os.path.exists(backup_file_name):
                os.remove(backup_file_name)

            if list_name != "":
                with open(backup_file_name, mode="x", encoding="utf-8") as f:
                    f.write(list_name + "\n")
                    for item in items:
                        f.write(item + "\n")

        # Response a JSON message to client with original command and parameter which adds "Server received: " on it.
        message = {"response": client_command,
                   "parameter": server_message}
        message_json = json.dumps(message)
        message_json = message_json.encode(encoding="utf-8")

        connection.send(message_json)

        print(f"The message send to Client: {message_json}")
        logging.info(f"The message send to Client: {message_json}")

        if client_command == "QUIT":
            print("Receiving a quit command!!!")
            print("Stop running this Server!!!")
            logging.info("Receiving a quit command!!!")
            logging.info("Stop running this Server.")
            break

    connection.close()
    server.close()