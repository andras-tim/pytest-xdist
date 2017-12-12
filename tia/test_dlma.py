# content of test_module.py
import pytest
from time import sleep
import sys


class TestD(object):
    @pytest.fixture(scope='class', autouse=True)
    def setup_class(self, config_asda):
        pass

    def test_func_fast__config_asda(self):
        sleep(1)

    def test_func_slow__config_asda(self):
        sleep(2)
