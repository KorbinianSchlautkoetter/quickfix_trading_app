import unittest
from quickfix_trading_app.fix_utils import create_new_order
import quickfix as fix

class TestFixUtils(unittest.TestCase):
    def test_create_new_order(self):
        symbol = "AAPL"
        qty = 100
        price = 150.0
        side = fix.Side_BUY
        message = create_new_order(symbol, qty, price, side)
        self.assertEqual(message.getHeader().getField(fix.BeginString()).getValue(), fix.BeginString_FIX44)
        self.assertEqual(message.getHeader().getField(fix.MsgType()).getValue(), fix.Msg)
