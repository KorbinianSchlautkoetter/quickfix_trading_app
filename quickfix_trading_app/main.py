import quickfix as fix
from quickfix_trading_app.application import FixApplication
from quickfix_trading_app.settings import CLIENT_CFG

def main():
    application = FixApplication()
    settings = fix.SessionSettings(CLIENT_CFG)
    storeFactory = fix.FileStoreFactory(settings)
    logFactory = fix.FileLogFactory(settings)
    initiator = fix.SocketInitiator(application, storeFactory, settings, logFactory)

    initiator.start()
    print("QuickFIX application started.")
    
    try:
        while True:
            pass
    except KeyboardInterrupt:
        initiator.stop()
        print("QuickFIX application stopped.")

if __name__ == "__main__":
    main()
