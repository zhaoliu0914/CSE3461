import sys
import json
import socket
import logging
import configparser

is_quitting = False
quit = "QUIT"
quitting = "QUITTING"


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
    config.read("client-configuration.ini", encoding="utf-8")

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

    # print the configuration file to console
    # write the configuration file to log file
    print("The content of configuration file is:")
    logging.info("The content of configuration file is:")
    for temp in config:
        if temp != "DEFAULT":
            print(f"[{temp}]")
            logging.info(f"[{temp}]")

            for child_node in config[temp]:
                print(f"{child_node}={config[temp][child_node]}")
                logging.info(f"{child_node}={config[temp][child_node]}")

    server_address = (server_host, int(server_port))

    # Set up socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(server_address)

    print(f"Connected to Server address: {server_address}")
    logging.info(f"Connected to Server address: {server_address}")

    # keeping ask input string from user
    # print and record input string to console and log file
    # tokenizing all the input string
    print("Please enter some words here: ")
    logging.info("Please enter some words here: ")
    for line in sys.stdin:
        line = line.strip()

        # if the input string is empty, prompt a warning message to user
        if len(line) == 0:
            print("Warning: Can not enter empty string!!!")
            logging.info("Warning: Can not enter empty string!!!")
            print()
            print("Please enter some words here: ")
            logging.info("Please enter some words here: ")
            continue

        print(f"The input string is: {line}")
        logging.info(f"The input string is: {line}")

        tokens = line.split()
        tokens[0] = tokens[0].upper()

        if is_quitting and tokens[0] != quit:
            print("The Server has shut down!!!")
            print("Please enter 'quit' to exit this program!!!")
            logging.info("The Server has shut down!!!")
            logging.info("Please enter 'quit' to exit this program!!!")
            continue

        tokenizing_str = "The tokenizing of input string is:"
        for token in tokens:
            tokenizing_str = tokenizing_str + " " + token

        print(tokenizing_str)
        logging.info(tokenizing_str)

        # if the first word is "quit", then quit the program
        if tokens[0] == quit:
            print("Shutting down ...")
            logging.info("Shutting down ...")
            break

        parameter = ""
        for token in tokens[1:len(tokens)]:
            parameter = parameter + " " + token
        parameter = parameter.strip()

        message = {"command": tokens[0],
                   "parameter": parameter}
        message_json = json.dumps(message)
        message_json = message_json.encode(encoding="utf-8")
        client.send(message_json)

        print(f"The message send to Server is: {message_json}")
        logging.info(f"The message send to Server is: {message_json}")

        server_data = client.recv(1024)
        server_data.decode(encoding="utf-8")
        server_json = json.loads(server_data)
        server_response = server_json["response"]
        server_parameter = server_json["parameter"]

        print(f"The message received from Server is: {server_data}")
        print(f"Server response: {server_response}")
        print(f"Server parameter: {server_parameter}")
        logging.info(f"The message received from Server is: {server_data}")
        logging.info(f"Server response: {server_response}")
        logging.info(f"Server parameter: {server_parameter}")

        if server_response == quitting:
            is_quitting = True
            print("The Server has shut down!!!")
            print("Please enter 'quit' to exit this program!!!")
            logging.info("The Server has shut down!!!")
            logging.info("Please enter 'quit' to exit this program!!!")
        else:
            print()
            print("Please enter some words here: ")
            logging.info("Please enter some words here: ")

    client.close()