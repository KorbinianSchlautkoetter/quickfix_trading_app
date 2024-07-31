import quickfix as fix

class FixApplication(fix.Application):
    def onCreate(self, sessionID):
        print(f"Session created: {sessionID}")

    def onLogon(self, sessionID):
        print(f"Logon: {sessionID}")

    def onLogout(self, sessionID):
        print(f"Logout: {sessionID}")

    def toAdmin(self, message, sessionID):
        print(f"To Admin: {message}")

    def fromAdmin(self, message, sessionID):
        print(f"From Admin: {message}")

    def toApp(self, message, sessionID):
        print(f"To App: {message}")

    def fromApp(self, message, sessionID):
        print(f"From App: {message}")
        self.onMessage(message, sessionID)

    def onMessage(self, message, sessionID):
        # Custom message processing
        print(f"Received message: {message}")
