# content of test_module.py
import pytest
from time import sleep
import sys


class TestB(object):
    @pytest.fixture(scope='class', autouse=True)
    def setup_class(self, config_b):
        pass

    def test_func_fast__config_b(self):
        sleep(3)

    def test_func_slow__config_b(self):
        sleep(3)
