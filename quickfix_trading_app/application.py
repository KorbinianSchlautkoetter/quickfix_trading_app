import quickfix as fix
from message_processor import MessageProcessor
from fix_utils import format_fix_message

class FixApplication(fix.Application):
    def __init__(self, processor):
        super().__init__()
        self.processor = processor

    def onCreate(self, sessionID):
        print(f"{sessionID.getSenderCompID()} - Session created: {sessionID}")

    def onLogon(self, sessionID):
        print(f"{sessionID.getSenderCompID()} - Logon: {sessionID}")

    def onLogout(self, sessionID):
        print(f"{sessionID.getSenderCompID()} - Logout: {sessionID}")

    def toAdmin(self, message, sessionID):
        print(f"{sessionID.getSenderCompID()} - Outbound admin message:")
        # print("Outbound admin message:")
        print(format_fix_message(message))

    def fromAdmin(self, message, sessionID):
        print(f"{sessionID.getSenderCompID()} - Inbound admin message:")
        # print("Inbound admin message:")
        print(format_fix_message(message))

    def toApp(self, message, sessionID):
        print(f"{sessionID.getSenderCompID()} - Outbound application message:")
        # print("Outbound application message:")
        print(format_fix_message(message))

    def fromApp(self, message, sessionID):
        print(f"{sessionID.getSenderCompID()} - Inbound application message:")
        # print("Inbound application message:")
        print(format_fix_message(message))
        self.onMessage(message, sessionID)

    def onMessage(self, message, sessionID):
        self.processor.process_message(message, sessionID)
        # added below to print each message in terminal
        print(f"Processed message: {message}")