# content of test_module.py
import pytest
from time import sleep
import sys


class TestA(object):
    @pytest.fixture(scope='class', autouse=True)
    def setup_class(self, config_b):
        pass

    def test_func_fast__config_asda(self, config_asda):
        sleep(1)

    def test_func_slow__config_e(self, config_e):
        sleep(2)

    def test_a__config_e(self, config_e):
        sleep(1)

    def test_b__config_e(self, config_e):
        sleep(1)

    def test_c__config_e(self, config_e):
        sleep(1)

    def test_d__config_e(self, config_e):
        sleep(1)

    def test_e__config_e(self, config_e):
        sleep(1)

    def test_f__config_e(self, config_e):
        sleep(1)
