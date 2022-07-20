#!/bin/python
from utils import init, handle_args, fetch_config, login_form, play_audio
from selenium_operations import Operations

if __name__ == '__main__':
    handle_args()
    init()
    user, passwd = login_form()
    operations = Operations(config=fetch_config())
    operations.log_in(email=user, password=passwd)
    if operations.main_loop():
        play_audio(success=True)
    else:
        play_audio(success=False)
    input("PRESS ANY KEY TO SHUT DOWN THE WEBDRIVER")
