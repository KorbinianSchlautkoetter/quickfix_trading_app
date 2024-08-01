import quickfix as fix

class MessageProcessor:
    def process_message(self, message, sessionID):
        msgType = fix.MsgType()
        message.getHeader().getField(msgType)
        if msgType.getValue() == fix.MsgType_NewOrderSingle:
            self.process_order(message, sessionID)
        else:
            print(f"Message type {msgType.getValue()} not supported")

    def process_order(self, message, sessionID):
        clOrdID = fix.ClOrdID()
        message.getField(clOrdID)

        symbol = fix.Symbol()
        message.getField(symbol)

        side = fix.Side()
        message.getField(side)

        orderQty = fix.OrderQty()
        message.getField(orderQty)

        price = fix.Price()
        message.getField(price)

        print(f"Processing order: {clOrdID}, {symbol}, {side}, {orderQty}, {price}")

        self.send_execution_report(message, sessionID)

    def send_execution_report(self, message, sessionID):
        executionReport = fix.Message()
        executionReport.getHeader().setField(fix.BeginString(fix.BeginString_FIX44))
        executionReport.getHeader().setField(fix.MsgType(fix.MsgType_ExecutionReport))
        
        executionReport.setField(fix.OrderID("12345"))
        executionReport.setField(fix.ExecID("12345"))
        executionReport.setField(fix.ExecType(fix.ExecType_TRADE))
        executionReport.setField(fix.OrdStatus(fix.OrdStatus_FILLED))
        executionReport.setField(fix.LeavesQty(0))

        # Extract and set the fields from the incoming message
        clOrdID = fix.ClOrdID()
        message.getField(clOrdID)
        executionReport.setField(clOrdID)  # Use the populated FieldBase object
        
        symbol = fix.Symbol()
        message.getField(symbol)
        executionReport.setField(symbol)  # Use the populated FieldBase object
        
        side = fix.Side()
        message.getField(side)
        executionReport.setField(side)  # Use the populated FieldBase object

        # Retrieve and set field values
        price_field = fix.Price()
        message.getField(price_field)
        avg_price = price_field.getValue()  # Retrieve value as double
        executionReport.setField(fix.AvgPx(avg_price))  # Correctly use the retrieved double value

        orderqty_field = fix.OrderQty()
        message.getField(orderqty_field)
        cumqty = orderqty_field.getValue()  # Retrieve value as double
        executionReport.setField(fix.CumQty(cumqty))  # Correctly use the retrieved double value
        

        fix.Session.sendToTarget(executionReport, sessionID)
        print(f"Sent execution report: {executionReport}")
