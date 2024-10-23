import socket

SERVER_ADDRESS = 'localhost'
SERVER_PORT = 1977

class DSlaser():
    def create_client(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to the server
        self.client_socket.connect((SERVER_ADDRESS, SERVER_PORT))
        return self.client_socket

    def start_countdown(self):
        
        message = '0100'
        print("Sending countdown increment!")
        
        # Send the COUNTDOWN_INITIATE request as UTF-8 encoded string
        message_bytes = message.encode('utf-8')
        self.client_socket.send(message_bytes)

        # Receive the response
        response_bytes = self.client_socket.recv(1024)
        print(f"Received response: {response_bytes}")

        # Ensure the response is at least 8 bytes 
        if len(response_bytes) < 8:
            print("Malformed response! Less than expected 8 bytes.")
            return None

        # First 4 bytes are message code and response code as UTF-8 strings
        response_message_code = response_bytes[0:2].decode('utf-8')
        response_code = response_bytes[2:4].decode('utf-8')
        print(f"Response message code: {response_message_code}, Response code: {response_code}")

        if response_code == '00':  # Expected success code
            # Next 4 bytes are the countdown value as a big-endian integer
            countdown_bytes = response_bytes[4:8].decode('utf-8')
            countdown = int(countdown_bytes, 16)
            print(f"Countdown initiated successfully. Countdown value: {countdown}")
            return countdown
        else:
            print("Error in initiating countdown!")
            return None
        
    def decrement_countdown(self, countdown_number):
        while countdown_number>0:
            next_countdown_number = countdown_number -1
            message_code = '0200'
            number_hex = f"{next_countdown_number:04x}"
            message = message_code + number_hex
            print(f"Sending Countdown Decrement: {message}")

            #Sending the message
            message_bytes = message.encode('utf-8')
            self.client_socket.send(message_bytes)

            #Receiving the response
            response_bytes = self.client_socket.recv(1024)
            


            
            



if __name__ == '__main__':
    dslaser_client = DSlaser()
    dslaser_client.create_client()
    starting_count = dslaser_client.start_countdown()
  
