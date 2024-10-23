import socket

SERVER_ADDRESS = 'localhost'
SERVER_PORT = 1977

class DSlaser():
    def create_client(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to the server
        self.client_socket.connect((SERVER_ADDRESS, SERVER_PORT))
        print("Connection established!")
        return self.client_socket

    def start_countdown(self):
        """
        For COUNTDOWN_INCREMENT
        """
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

        if response_code == '00': 
            countdown_bytes = response_bytes[4:8].decode('utf-8')
            countdown = int(countdown_bytes, 16)
            print(f"Countdown initiated successfully. Countdown value: {countdown}")
            return countdown
        else:
            print("Error in initiating countdown!")
            return None
        
    def decrement_countdown(self, countdown_number):
        """
        For COUNTDOWN_DECREMENT
        """
        
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
            print(f"Got the response! {response_bytes}")

            #Ensuring the response is at least 8 bytes
            if len(response_bytes) < 8 :
                print("Malformed response buddy, must be 8 bytes.")
                break
            
            #Parsing the response now
            response_message_code = response_bytes[0:2].decode('utf-8')
            response_code = response_bytes[2:4].decode('utf-8')
            countdown = response_bytes[4:8].decode('utf-8')
            countdown_value = int(countdown, 16)

            print(f"Response message code: {response_message_code}, Response code: {response_code}")
            print(f"Countdown value sent by server: {countdown_value}")

            if response_code == '00':
                print("Sucess, countdown decremented!")
            else:
                print("Erorr in decrementing the value")
                break
            
            # Updating the countdown_number for the next iteration
            countdown_number = countdown_value

            # Check if countdown has reached zero
            if countdown_number == 0:
                print("Countdown has reached zero!")
                break
        


                     
            



if __name__ == '__main__':
    dslaser_client = DSlaser()
    dslaser_client.create_client()
    starting_count = dslaser_client.start_countdown()
    decremnting_count = dslaser_client.decrement_countdown(starting_count)
  
