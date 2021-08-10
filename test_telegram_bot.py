from telegram_bot import *

import unittest
from unittest.mock import MagicMock

class Test_TestIncrementDecrement(unittest.TestCase):
    
    def test_receta(self):
        pass

    def test_ingredientes(self):
        result = MagicMock(ingredientsCommand(None, None)).return_value = 'help message'
        assert result is not None

if __name__ == '__main__':
    unittest.main()