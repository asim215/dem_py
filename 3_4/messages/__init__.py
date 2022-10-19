from messages.messages import msgs


def get_message(msg_name, *args, **kwargs):
    return msgs.get(msg_name, "Unkown message").format(*args, **kwargs)