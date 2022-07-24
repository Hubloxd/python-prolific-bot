from utils import init, handle_args, fetch_config, login_form, play_audio
from selenium_operations import Operations
from selenium.common import JavascriptException
from time import sleep


if __name__ == '__main__':
    handle_args()
    init()
    user, passwd = login_form()
    operations = Operations(config=fetch_config())
    operations.log_in(email=user, password=passwd)
    try:
        if operations.main_loop():
            play_audio(True)
    except JavascriptException:
        play_audio(False)

    sleep(3)
    input("PRESS ANY KEY TO SHUT DOWN THE WEBDRIVER")
