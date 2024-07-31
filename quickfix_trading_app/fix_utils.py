import quickfix as fix

def create_new_order(symbol, qty, price, side):
    message = fix.Message()
    message.getHeader().setField(fix.BeginString(fix.BeginString_FIX42))
    message.getHeader().setField(fix.MsgType(fix.MsgType_NewOrderSingle))
    message.setField(fix.ClOrdID("12345"))
    message.setField(fix.Symbol(symbol))
    message.setField(fix.Side(side))
    message.setField(fix.TransactTime())
    message.setField(fix.OrderQty(qty))
    message.setField(fix.Price(price))
    return message
