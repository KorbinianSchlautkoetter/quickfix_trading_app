class MessageProcessor:
    def process_order(self, message):
        print(f"Processing order: {message}")

    def process_execution_report(self, message):
        print(f"Processing execution report: {message}")

    # Add more message processing methods as needed
