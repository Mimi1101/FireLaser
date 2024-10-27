import socket

SERVER_ADDRESS = 'localhost'
SERVER_PORT = 1977

class DSlaser():
    def create_client(self):
        """
        Creating a client to send to the server
        """
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        self.client_socket.connect((SERVER_ADDRESS, SERVER_PORT))
        print("Connection established!")
        return self.client_socket

    def start_countdown(self):
        """
        Incrementing the countdown
        """
        message = '0100'
        
        message_bytes = message.encode('utf-8')
        print("Sending for countdown increment")
        self.client_socket.send(message_bytes)

        # Receiving the response
        response_bytes = self.client_socket.recv(1024)

        # Ensure the response is at least 8 bytes complying with the instructions
        if len(response_bytes) < 8:
            print("This is a malinformed response.")
            return None

        response_message_code = response_bytes[0:2].decode('utf-8')
        response_code = response_bytes[2:4].decode('utf-8')
        print(f"Response message code: {response_message_code}, Response code: {response_code}")

        if response_code == '00': 
            countdown_bytes = response_bytes[4:8].decode('utf-8')
            countdown = int(countdown_bytes, 16)
            print(f"Countdown initiated successfully. Countdown value: {countdown}")
            return countdown
        else:
            print("Couldn't initiate countdown")
            return None
        
    def decrement_countdown(self, countdown_number):
        """
        Decremting the countdown number to 0 we got from countdown increment.
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
                print("countdown is decremented")
            else:
                print("Erorr in decrementing the value")
                break
            
            # Updating the countdown_number for the next iteration
            countdown_number = countdown_value

            # Check if countdown has reached zero
            if countdown_number == 0:
                print("Countdown has reached zero!")
                return countdown_number

    def fire_laser(self, countdown_value):
        """
        Firing the laser after the countdown decrement has reached 0
        """
        if(countdown_value == 0):
            message = '0300'

            message_bytes = message.encode('utf-8')
            self.client_socket.send(message_bytes)

            # Receive the response
            response_bytes = self.client_socket.recv(1024)


            #Ensuring the response is at least 9 bytes complying with the instructions
            if len(response_bytes) < 9 :
                print("Malformed response")
                return None

            response_message_code = response_bytes[0:2].decode('utf-8')
            response_code = response_bytes[2:4].decode('utf-8')
            firiring_string = response_bytes[4:9].decode('utf-8')

            if response_code == '00':
                print("Sent a firing ")
            else:
                print("Erorr firing")
                return None


            print(f"Response message code: {response_message_code}, Response code: {response_code}")
            print(f"Firing message sent by the server: {firiring_string}")
            return firiring_string

            
    def fire_laser_confirmation(self, firing_string):

        """
        Checking if the laser is actually fired.
        """
        
        if firing_string == 'Fired':
            message = '0400'
            message_bytes = message.encode('utf-8')
            self.client_socket.send(message_bytes)

            # Receive the response
            response_bytes = self.client_socket.recv(1024)

            # Ensure the response is at least 44 bytes  complying with the instructions
            if len(response_bytes) < 44:
                print("This is a malformed response")
                return None

            response_message_code = response_bytes[0:2].decode('utf-8')
            response_code = response_bytes[2:4].decode('utf-8')
            print(f"Response message code: {response_message_code}, Response code: {response_code}")

        if response_code == '00': 
            fire_laser_confirmation = response_bytes[4:44].decode('utf-8')
            print(f"Geeting the conformation for firing the laser: {fire_laser_confirmation}")
            return fire_laser_confirmation
        else:
            print("Error in initiating countdown!")
            return None

    def communication_shutdown (self):
        """
        Shutting down the communication with the server
        """
        message = '0500'
        message_bytes = message.encode('utf-8')
        self.client_socket.send(message_bytes)

        # Receive the response
        response_bytes = self.client_socket.recv(1024)

        # Ensure the response is at least 4 bytes 
        if len(response_bytes) < 4:
            print("Malformed response.")
            return None

        response_message_code = response_bytes[0:2].decode('utf-8')
        response_code = response_bytes[2:4].decode('utf-8')
        print(f"Response message code: {response_message_code}, Response code: {response_code}")

        if response_code == '00': 
            print("Communication is shutdown succesfully.")

        self.client_socket.close()




if __name__ == '__main__':
    dslaser_client = DSlaser()
    dslaser_client.create_client()
    print("-----------------------------------------------")
    starting_count = dslaser_client.start_countdown()
    print("-----------------------------------------------")
    decremnting_count = dslaser_client.decrement_countdown(starting_count)
    print("-----------------------------------------------")
    fire_laser = dslaser_client.fire_laser(decremnting_count)
    print("-----------------------------------------------")
    dslaser_client.fire_laser_confirmation(fire_laser)
    print("-----------------------------------------------")
    dslaser_client.communication_shutdown()
  
