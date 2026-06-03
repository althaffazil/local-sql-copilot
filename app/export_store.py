last_result = None


def save_result(result):

    global last_result

    last_result = result


def get_last_result():

    return last_result