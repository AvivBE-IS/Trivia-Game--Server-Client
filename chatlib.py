# Protocol Constants

CMD_FIELD_LENGTH = 16  # Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4  # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10 ** LENGTH_FIELD_LENGTH - 1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # 22. Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message
C2S_ORDERS= ["LOGIN", "LOGOUT", "LOGGED","GET_QUESTION","SEND_ANSWER", "MY_SCORE","HIGHSCORE" ] #It must be updated every time a new command is added
S2C_ORDERS=["LOGIN_OK","LOGGED_ANSWER","YOUR_QUESTION","CORRECT_ANSWER","WRONG_ANSWER","YOUR_SCORE","ALL_SCORE","ERROR","NO_QUESTIONS"] #It must be updated every time a new command is added
# Protocol Messages
# In this dictionary we will have all the client and server command names

PROTOCOL_CLIENT = {
    "login_msg": "LOGIN",
    "logout_msg": "LOGOUT",
    "get_my_score_msg": "MY_SCORE",
    "get_highscore_msg": "HIGHSCORE"
}

PROTOCOL_SERVER = {
    "login_ok_msg": "LOGIN_OK",
    "login_failed_msg": "ERROR"
}  # I preferred not to use

# Other constants

ERROR_RETURN = None  # What is returned in case of an error


def build_message(cmd, data):
    """
    Gets command name (str) and data field (str) and creates a valid protocol message
    :param cmd: - In the structure of this message there are 16 characters of a command. Command characters indicate the type of message (eg LOGIN.) The remaining characters
Of the 16 characters are space characters (" ").
    :param data: - Information represented by characters. In this section we will write the message. The message will contain the information we want to convey. Some commands do not require
A message field (such as a LOGOUT message) and in such cases we will not fill in these characters and this field will remain empty.
    :return: Full massage- A string.
    """
    if len(cmd) > CMD_FIELD_LENGTH:
        return None

    if len(data) > MAX_DATA_LENGTH:
        return
    msg = (cmd + " " * (CMD_FIELD_LENGTH - len(cmd)) + DELIMITER + str(len(data)).zfill(4) + DELIMITER + data).strip()

    return msg


def parse_message(data):
    """
	Parses protocol message and returns command name and data field
	Returns: cmd (str), data (str). If some error occured, returns None, None
	"""

    parts_of_msg = data.split(DELIMITER, 2)
    if len(parts_of_msg) < 3:
        return None, None

    if len(parts_of_msg) > 3:
        data = DELIMITER.join(parts_of_msg[2:])
    else:
        data = parts_of_msg[-1]
    # validate the size of data
    temp = str(parts_of_msg[-2]).strip().lstrip('0')
    if temp == "":
        temp = "0"

    if str(len(data)) != temp:
        return None, None
    return parts_of_msg[0].strip(), data  # strip


def parse_message1(data):
    """
    Parses protocol message and returns command name and data field.
    :param data: Information represented by characters.
    :return: A tupple of cmd and data.
    """
    cmd, dataLen, msg = data.split("|", 2)
    if int(dataLen) != len(msg):
        print("Data length doesn't suit to Length.")
        return None, None
    if cmd == "" or msg == "":
        return None, None
    return cmd.strip(), msg

    # Can be used the 'white list' method to avoid injection scripts.

def split_data(msg):
    """
    Helper method. gets a string and number of expected fields in it. Splits the string
    using protocol's data field delimiter (|#) and validates that there are correct number of fields.
    :param msg:
    :param expected_fields:
    :return:  A list of fields if all ok.
     If some error occured returns None.
    """
    dataList = msg.split(DATA_DELIMITER)
    #if len(dataList) != expected_fields:
    #    return

    return dataList




def join_data(msg_fields):
    """
    Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter.
    :param msg_fields:
    :return: A string that looks like cell1#cell2#cell3
    """
    return DATA_DELIMITER.join(msg_fields)