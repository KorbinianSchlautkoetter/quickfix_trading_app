import quickfix as fix
from application import FixApplication
from message_processor import MessageProcessor
from settings import CLIENT_CFG, SERVER_CFG
from fix_utils import send_new_order
import threading
import time

stop_event = threading.Event() # Added to implement a flag to signal the worker threads to stop
shared_state = {}  # Shared dictionary to hold initiator and acceptor references

def start_initiator():
    processor = MessageProcessor()
    application = FixApplication(processor)
    settings = fix.SessionSettings(CLIENT_CFG)
    storeFactory = fix.FileStoreFactory(settings)
    logFactory = fix.FileLogFactory(settings)
    initiator = fix.SocketInitiator(application, storeFactory, settings, logFactory)

    try:
        initiator.start()
        print("Client started.")
        shared_state['initiator'] = initiator  # Store the initiator in the shared dictionary
        # while True:
        while not stop_event.is_set():
            time.sleep(1)
    except (fix.ConfigError, fix.RuntimeError) as e:
        print(e, flush=True)
    finally:
        initiator.stop()

    # initiator.start()
    # print("Client started.")
    # return initiator

def start_acceptor():
    processor = MessageProcessor()
    application = FixApplication(processor)
    settings = fix.SessionSettings(SERVER_CFG)
    storeFactory = fix.FileStoreFactory(settings)
    logFactory = fix.FileLogFactory(settings)
    acceptor = fix.SocketAcceptor(application, storeFactory, settings, logFactory)

    try:
        acceptor.start()
        print("Server started.")
        shared_state['acceptor'] = acceptor  # Store the acceptor in the shared dictionary
        # while True:
        while not stop_event.is_set():
            time.sleep(1)
    except (fix.ConfigError, fix.RuntimeError) as e:
        print(e, flush=True)
    finally:
        acceptor.stop()

    # acceptor.start()
    # print("Server started.")
    # return acceptor


def send_orders():
    try:
        while not stop_event.is_set():
            # Wait for a short time to ensure the session is established
            time.sleep(45)

            # Construct the session ID directly
            sessionID = fix.SessionID("FIX.4.4", "CLIENT1", "SERVER1")

            # Send a new order
            send_new_order(sessionID)
            stop_event.set()  # Signal to stop after sending one order
    except Exception as e:
        print(f"An error occurred in the send_orders thread: {e}", flush=True)


def main():
    acceptor_thread = None
    initiator_thread = None
    order_thread = None
    
    try:
    
        initiator_thread = threading.Thread(target=start_initiator, name="InitiatorThread")
        acceptor_thread = threading.Thread(target=start_acceptor, name="AcceptorThread")

        # initiator_thread.daemon = True # make the order-sending thread a daemon thread so that it automatically terminates when the main program exits
        # acceptor_thread.daemon = True # make the order-sending thread a daemon thread so that it automatically terminates when the main program exits

        initiator_thread.start()
        acceptor_thread.start()

        # acceptor = start_acceptor()
        # initiator = start_initiator()

        # Start a thread to send orders
        # order_thread = threading.Thread(target=send_orders, args=(initiator_thread,))
        order_thread = threading.Thread(target=send_orders, name="OrderThread")
        # order_thread.daemon = True # make the order-sending thread a daemon thread so that it automatically terminates when the main program exits
        order_thread.start()

        initiator_thread.join()
        acceptor_thread.join()
        order_thread.join()

        # while not stop_event.is_set():
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        stop_event.set()
        print("Keyboard interrupt received. FIX application stopped.", flush=True)
    except Exception as e:
        print(f"An error occurred: {e}", flush=True)
    finally:
        # if initiator_thread is not None:
        #     initiator_thread.stop()
        #     print("Client stopped.", flush=True)
        # if acceptor_thread is not None:
        #     acceptor_thread.stop()
        #     print("Server stopped.", flush=True)
        # # Ensure the thread has finished before exiting
        # if order_thread is not None:
        #     order_thread.join()
        stop_event.set()
        print("FIX application stopped.", flush=True)

if __name__ == "__main__":
    main()
