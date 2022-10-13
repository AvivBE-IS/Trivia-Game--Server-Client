import socket
import chatlib
import sys

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678


# HELPER SOCKET METHODS

def build_and_send_message(conn, cmd, data):
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    :param conn: Socket object.
    :param cmd: In the structure of this message there are 16 characters of a command. Command characters indicate the type of message (eg LOGIN.) The remaining characters
Of the 16 characters are space characters
    :param data: - Information represented by characters. In this section we will write the message. The message will contain the information we want to convey. Some commands do not require
A message field (such as a LOGOUT message) and in such cases we will not fill in these characters and this field will remain empty
    :return: None.
    """
    """

    Paramaters: conn (), code (str), data (str)
    Returns: Nothing
    """
    full_msg = chatlib.build_message(cmd, data)
    conn.send(full_msg.encode())
    # print("The client sent " + full_msg)


def recv_message_and_parse(conn):
    """
    Recieves a new message from given socket,
    then parses the message using chatlib.
    :param conn: Socket object.
    :return: A tuple which consists 2 strings: msg_code and data.
    msg_code- Describes the command returned from the server.
    data- The server's response to client's command.
    """
    full_msg = conn.recv(1024).decode()
    print("[CLIENT] ", full_msg)
    cmd, data = chatlib.parse_message(full_msg)
    return cmd, data


def connect():
    """
    Establishing a physical connection to the server using socket functions.
    127.0.0.1 is the local address of the computer.
    8822 is the prescribed port. It can be changed.
    :return: None.
    """
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (SERVER_IP, SERVER_PORT)
    my_socket.connect(server_address)
    return my_socket


def error_and_exit(error_msg):
    """
    Printing an error message and immediate termination of the program.
    :param error_msg: None.
    :return: None.
    """
    sys.exit(error_msg)

def build_send_recv_parse(conn, cmd, data):
    """
    The function will shorten our processes and use the sending and receiving functions one after the other.
    :param conn: Socket object.
    :param cmd: Command line.
    :param data: Data to server.
    :return: A tuple which consists 2 strings: msg_code and data.
    """
    build_and_send_message(conn, cmd, data)
    return recv_message_and_parse(conn)

# Functional Requirements

def login(conn):
    """
    Requests a username and password from the program operator,
    than creates and sends a login command according to the protocol using the build_and_send_message function.
    The function will receive a response from the server by the recv_message_and_parse function,
    and will check whether the login was successful or failed according to the type of message returned (command).
    The program will print to the user whether the login was successful or failed.
    :param conn: Socket object.
    :return: None.
    """
    while(True):
        username = input("Please enter username:\n")
        password = input("Please enter password:\n")
        data = chatlib.join_data([username, password])
        build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["login_msg"], data)
        cmd, data = recv_message_and_parse(conn)
        if cmd == "LOGIN_OK":
            print("LOGGED IN")
            break
        else:
            print("LOGGING FAILD. PLEASE TRY AGAIN.\n")




def logout(conn):
    """
    The function sends a logout command according to the protocol using the build_and_send_message function.
    :param conn: Socket object.
    :return: None.
    """
    build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["logout_msg"], "")
    print("GOODBYE.\n")

def get_score(conn):
    """
    Prints the user's current score.
    :param conn: Socket object.
    :return: None.
    """
    cmd, data = build_send_recv_parse(conn, "MY_SCORE", "")
    if cmd == "YOUR_SCORE":
        print("Your score is ", data)
    else:
        print("Error.\n")


def get_highscore(conn):
    """
    Prints the Highscores table as it comes from the server.
    :param conn: Socket object.
    :return: None.
    """
    cmd, data = build_send_recv_parse(conn, "HIGHSCORE", "")
    if cmd == "ALL_SCORE":
        listed_data = data.split("\n")
        for user_score in listed_data:
            print(user_score)
    else:
        print("Error.\n")


def play_question(conn):
    """
    Ask a question from the server.
Print the question to the user.
Ask the user for the answer he thinks is correct.
Send the answer the user entered to the server.
Receive feedback from the server as to whether the answer the user chose is correct or incorrect, and print the correct answer.
If there is any problem, the function will simply print an error and stop with return.
    :param conn: Socket object.
    :return: None.
    """
    cmd, quest_data = build_send_recv_parse(conn, "GET_QUESTION", "")
    if cmd == "YOUR_QUESTION":
        id_quest = show_question(quest_data)
        ans = input("Please choose an answer [1-4]: ")
        data_ans = id_quest + chatlib.DATA_DELIMITER + ans
        cmd, data = build_send_recv_parse(conn, "SEND_ANSWER", data_ans)

        if cmd == "CORRECT_ANSWER":
            cmd, data = build_send_recv_parse(conn, "MY_SCORE", "")
            print("Your score is ", data)
        elif cmd == "WRONG_ANSWER":
            print("Nope, correct answer is ", data)
        elif cmd == "NO_QUESTIONS":
            print("No more questions. GAME OVER. ")

    else:
        print("Error.\n")
        print("cmd=", cmd)

def show_question(quest_data):
    """
    The function will parse the string received from the server, and present it as a question to the client.
    :param quest_data: Massage from the server.
    :return: id_quest.
    """
    quest_data_listed = chatlib.split_data(quest_data)
    quest_id = quest_data_listed[0]
    print(quest_data_listed[1])
    print("\t1. ",quest_data_listed[2])
    print("\t2. ", quest_data_listed[3])
    print("\t3. ", quest_data_listed[4])
    print("\t4. ", quest_data_listed[5])
    return quest_id


def get_logged_users(conn):
    """
    Prints the list of all users currently connected to the server.
    :param conn: Socket object.
    :return: None.
    """
    cmd, data = build_send_recv_parse(conn, "LOGGED", "")
    if cmd == "LOGGED_ANSWER":
        print(data)
    else:
        print("Error.")


def main():
    conn = connect()
    login(conn)
    if conn:
        while True:
            choice = input("""
p        Play a trivia question
s        Get my score
h        Get high score
l        Get logged users
q        Quit
Please enter your choice: """)
            if choice == 's':
                get_score(conn)
            elif choice == 'p':
                play_question(conn)
            elif choice == 'h':
                get_highscore(conn)
            elif choice == 'l':
                get_logged_users(conn)
            elif choice == 'q':
                logout(conn)
                break
    print("Thank you for playing :)")

if __name__ == '__main__':
    main()
