import sys
import logging
import configparser

if __name__ == '__main__':
    # set up log file
    logging.basicConfig(filename="project1.log", encoding="utf-8", level=logging.INFO)

    # set up config file
    config = configparser.ConfigParser()
    config.read("configuration.ini")

    for temp in config:
        if temp != "DEFAULT":
            print("====================")
            print(f"[{temp}]")
            logging.info(f"[{temp}]")

            for child_node in config[temp]:
                print(f"{child_node}: {config[temp][child_node]}")
                logging.info(f"{child_node}: {config[temp][child_node]}")
            print("====================")

    print("Please enter some words here: ", end="")
    logging.info("Please enter some words here: ")
    for line in sys.stdin:
        line = line.strip()
        if len(line) == 0:
            print("Warning: Can not enter empty string!!!")
            logging.info("Warning: Can not enter empty string!!!")
            print()
            print("Please enter some words here: ", end="")
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
        print("Please enter some words here: ", end="")
        logging.info("Please enter some words here: ")