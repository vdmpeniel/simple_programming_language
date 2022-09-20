import basic


def main_loop():
    while True:
        text = input('basic > ')
        result, error = basic.run(text)
        if error:
            print(error.as_string())
        else:
            print(result)
