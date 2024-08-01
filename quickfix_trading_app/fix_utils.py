import quickfix as fix
from fix_config import FIELD_NAMES

def format_fields(fields):
    formatted_message = []
    # Iterate over known field tags
    for tag in FIELD_NAMES.keys():
        tag_num = int(tag)
        if fields.isSetField(tag_num):
            try:
                field_value = fields.getField(tag_num)
                field_name = FIELD_NAMES.get(tag, f"Unknown({tag})")
                formatted_message.append(f"{field_name}: {field_value}")
            except fix.FieldNotFound:
                formatted_message.append(f"Field with tag {tag} not found")
    return ";".join(formatted_message)

def format_fix_message(message):
    formatted_message = []
    
    # Extract and format header fields
    header = message.getHeader()
    # formatted_message.append("Header:")
    formatted_message.append(format_fields(header))
    
    # Extract and format body fields
    # formatted_message.append("Body:")
    formatted_message.append(format_fields(message))
    
    return "\n".join(formatted_message)



def create_new_order(symbol, qty, price, side):
    message = fix.Message()
    message.getHeader().setField(fix.BeginString(fix.BeginString_FIX44))
    message.getHeader().setField(fix.MsgType(fix.MsgType_NewOrderSingle))
    message.setField(fix.ClOrdID("12345"))
    message.setField(fix.Symbol(symbol))
    message.setField(fix.Side(side))
    message.setField(fix.TransactTime())
    message.setField(fix.OrderQty(qty))
    message.setField(fix.Price(price))
    message.setField(fix.OrdType(fix.OrdType_LIMIT))  # Set as limit order
    return message

def send_new_order(sessionID):
    message = create_new_order("AAPL", 100, 150.00, fix.Side_BUY)
    fix.Session.sendToTarget(message, sessionID)
    print("Sent new order:", message)


