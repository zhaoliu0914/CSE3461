import sys
import logging
import configparser

if __name__ == '__main__':
    # set up log file
    logging.basicConfig(filename="project1.log", level=logging.INFO)

    # set up config file
    config = configparser.ConfigParser()
    config.read("configuration.ini", encoding="utf-8")

    print("The content of configuration file is:")
    logging.info("The content of configuration file is:")
    for temp in config:
        if temp != "DEFAULT":
            print(f"[{temp}]")
            logging.info(f"[{temp}]")

            for child_node in config[temp]:
                print(f"{child_node}={config[temp][child_node]}")
                logging.info(f"{child_node}={config[temp][child_node]}")

    print("Please enter some words here: ")
    logging.info("Please enter some words here: ")
    for line in sys.stdin:
        line = line.strip()
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

        tokenizing_str = "The tokenizing of input string is:"
        for token in tokens:
            tokenizing_str = tokenizing_str + " " + token

        print(tokenizing_str)
        logging.info(tokenizing_str)

        if tokens[0] == "QUIT":
            print("Shutting down ...")
            logging.info("Shutting down ...")
            break

        print()
        print("Please enter some words here: ")
        logging.info("Please enter some words here: ")
