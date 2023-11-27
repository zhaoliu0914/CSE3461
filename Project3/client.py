import sys
import json
import socket
import logging
import configparser

is_quitting = False
quit = "QUIT"
help = "HELP"
show = "SHOW"
valid_commands = ["ADD", "CREATE", "DELETE", "HELP", "QUIT", "REMOVE", "SHOW"]
parameters_required = ["ADD", "CREATE", "DELETE", "REMOVE"]


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


def usage():
    print("add <list item>           - Adds an item to the current list")
    print("create <list>             - Creates a new list")
    print("delete <list>             - Deletes a list")
    print("help                      - Displays a message showing all available commands")
    print("quit                      - Gracefully shuts down both server and client applications")
    print("remove <list item>        - Removes an item from the current list")
    print("show                      - Displays a numbered list of the list items")
    print("")

    """
    logging.info("add <list item>           - Adds an item to the current list")
    logging.info("create <list>             - Creates a new list")
    logging.info("delete <list>             - Deletes a list")
    logging.info("help                      - Displays a message showing all available commands")
    logging.info("quit                      - Gracefully shuts down both server and client applications")
    logging.info("remove <list item>        - Removes an item from the current list")
    logging.info("show                      - Displays a numbered list of the list items")
    logging.info("")
    """


if __name__ == '__main__':
    # set up config file
    config = configparser.ConfigParser()
    config.read("client-configuration.ini", encoding="utf-8")

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
    usage()
    print("Please enter a valid command here: ")
    logging.info("Please enter a valid command here: ")
    for line in sys.stdin:
        line = line.strip()

        # if the input string is empty, prompt a warning message to user
        if len(line) == 0:
            print("Warning: Can not enter empty string!!!")
            logging.info("Warning: Can not enter empty string!!!")
            print()
            usage()
            print("Please enter a valid command here: ")
            logging.info("Please enter a valid command here: ")
            continue

        print()
        #print(f"The input command is: {line}")
        logging.info(f"The input command is: {line}")

        tokens = line.split()
        tokens[0] = tokens[0].upper()

        # Checking for invalid command
        if tokens[0] not in valid_commands:
            print(f"Invalid command entered: {tokens[0].lower()}")
            logging.info(f"Invalid command entered: {tokens[0].lower()}")
            print()
            print("usage: ")
            logging.info("usage: ")
            usage()
            print("Please enter a valid command here: ")
            logging.info("Please enter a valid command here: ")
            continue

        # Checking for missing parameters
        if tokens[0] in parameters_required and len(tokens) == 1:
            print(f"Missing element in command: {tokens[0].lower()}")
            logging.info(f"Missing element in command: {tokens[0].lower()}")
            print()
            print("usage: ")
            logging.info("usage: ")
            usage()
            print("Please enter a valid command here: ")
            logging.info("Please enter a valid command here: ")
            continue

        # Checking for missing parameters
        if (tokens[0] == "CREATE" or tokens[0] == "DELETE") and len(tokens) != 2:
            print(f"There only need one element in command: {tokens[0].lower()}")
            logging.info(f"There only need one element in command: {tokens[0].lower()}")
            print()
            print("usage: ")
            logging.info("usage: ")
            usage()
            print("Please enter a valid command here: ")
            logging.info("Please enter a valid command here: ")
            continue

        # for help command
        if tokens[0] == help:
            print()
            print("usage: ")
            logging.info("usage: ")
            usage()
            print("Please enter a valid command here: ")
            logging.info("Please enter a valid command here: ")
            continue

        # if the first word is "quit", then quit the program
        if tokens[0] == quit:
            print("Shutting down ...")
            logging.info("Shutting down ...")

        tokenizing_str = "The tokenizing of input command is:"
        for token in tokens:
            tokenizing_str = tokenizing_str + " " + token

        #print(tokenizing_str)
        logging.info(tokenizing_str)

        parameter = ""
        for token in tokens[1:len(tokens)]:
            parameter = parameter + " " + token
        parameter = parameter.strip()

        message = {"command": tokens[0],
                   "parameter": parameter}
        message_json = json.dumps(message)
        message_json = message_json.encode(encoding="utf-8")

        # send a request to server
        client.send(message_json)

        #print(f"The message send to Server is: {message_json}")
        logging.info(f"The message send to Server is: {message_json}")

        server_data = client.recv(1024)
        server_data.decode(encoding="utf-8")
        server_json = json.loads(server_data)
        server_response = server_json["response"]
        server_parameter = server_json["parameter"]

        #print(f"The message received from Server is: {server_data}")
        #print(f"Server response: {server_response}")
        #print(f"Server parameter: {server_parameter}")
        print(server_parameter)
        logging.info(f"The message received from Server is: {server_data}")
        logging.info(f"Server response: {server_response}")
        logging.info(f"Server parameter: {server_parameter}")

        if server_response == quit:
            #is_quitting = True
            print("The Server has bean shut down!!!")
            print("Bye Bye!!!")
            logging.info("The Server has bean shut down!!!")
            logging.info("Bye Bye!!!")
            break
        else:
            print()
            logging.info("")
            print("Please enter a valid command here: ")
            logging.info("Please enter a valid command here: ")

    client.close()