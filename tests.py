import unittest
from selenium_operations import Operations
from utils import play_audio, fetch_config
from selenium.common import JavascriptException


class MyTest(unittest.TestCase):
    def test_sound(self):
        operations = Operations(fetch_config())
        try:
            if operations.main_loop():
                play_audio(True)
        except JavascriptException:
            play_audio(False)


if __name__ == '__main__':
    unittest.main()
