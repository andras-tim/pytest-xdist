# content of test_module.py
import pytest
from time import sleep
import sys


class TestC(object):
    @pytest.fixture(scope='class', autouse=True)
    def setup_class(self, config_c):
        pass

    def test_func_fast__config_c(self):
        sleep(1)

    def test_func_slow__config_c(self):
        sleep(2)
