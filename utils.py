from os.path import join, exists
from os import remove
from sys import argv
from time import sleep

import simpleaudio as sa


class FileIsMissingException(Exception):
    """
    Exception raised while checking for files.

    Attributes:
        filename -- exact filename of the missing file
    """

    def __init__(self, filename: str):
        self.message = f"One of the necessary files is missing: {filename}"
        super().__init__(self.message)


class UnknownArgumentPassed(Exception):
    """Exception raised when an unknown argument is passed"""

    def __init__(self, argument: str):
        self.message = f"Argument '{argument}' is not known"
        super().__init__(self.message)


def init() -> None:
    """
    checks for all necessary files
    :return: None
    """

    necessary_files = ['config.ini', 'success.wav', 'fail.wav', ]

    for filename in necessary_files:
        if exists(join('./', filename)):
            print(f"Searching for {filename}", end='... ')
        else:
            raise FileIsMissingException(filename)
        print('OK')


def handle_args() -> None:
    for arg in argv[1:]:
        match arg:
            case '-h' | "--help":
                print("-r or --reset to reset credentials")
            case '-r' | "--reset":
                for filename in ('data.dat', 'session_id.cookie'):
                    try:
                        remove(join('./', filename))
                    except FileNotFoundError:
                        print(f"File '{filename}' was not found")
                        input("Press any key to continue...")
            case _:
                raise UnknownArgumentPassed(argument=arg)


def fetch_config() -> dict[str: str]:
    """
    Loops through whole config.ini file returning every line
    :return: dict[str: str]
    """
    config: dict[str:str] = {}
    with open('config.ini', 'r') as f:
        lines = [line.strip() for line in f.readlines() if line]
    for index, line in enumerate(lines):
        split = line.replace(' ', '').split('=')
        key = split[0]
        if len(split) > 1:
            value = split[1]
        else:
            value = ''
        config[key] = value

    return config


def encode_text(string: str, n: int, reverse: bool) -> str:
    data = string.strip().encode('utf8')
    if reverse:
        data_rotated: bytes = bytes([x - n for x in data])
    else:
        data_rotated: bytes = bytes([x + n for x in data])

    return data_rotated.decode('utf8')


def register_user() -> tuple[str, str]:
    username = input("Please enter Prolific username: \n").strip()
    passwd = input("Please enter Prolific password: \n").strip()
    data = encode_text(f"{username};{passwd}", 4, False)
    with open('data.dat', 'w', encoding='utf8') as f:
        f.write(data)

    return username, passwd


def log_in_user() -> tuple[str, str]:
    with open('./data.dat', 'r', encoding='utf8') as f:
        lines = f.readlines()[0].strip()
    user, passwd = encode_text(lines, 4, True).split(';')
    return user, passwd


def login_form() -> tuple[str, str]:
    if not exists(join('./', 'data.dat')):
        user, passwd = register_user()
    else:
        user, passwd = log_in_user()

    return user, passwd


def play_audio(success: bool):
    if success:
        wave_obj = sa.WaveObject.from_wave_file('./success.wav')
    else:
        wave_obj = sa.WaveObject.from_wave_file('./fail.wav')
    play_obj = wave_obj.play()
    play_obj.wait_done()


if __name__ == '__main__':
    # init()
    print(fetch_config().items())
    # handle_args()
    # u, p = login_form()
    # play_audio(success=False)
