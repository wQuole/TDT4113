import arduino_connect  # This is the key import so that you can access the serial port.

# M O R S E C O D E _ C L A S S / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /
class mocoder():

    #0 = dot, 1 = dash
    _morse_codes = {'01':'a','1000':'b','1010':'c','100':'d','0':'e','0010':'f','110':'g','0000':'h','00':'i','0111':'j',
                    '101':'k','0100':'l','11':'m','10':'n','111':'o','0110':'p','1101':'q','010':'r','000':'s','1':'t',
                    '001':'u','0001':'v','011':'w','1001':'x','1011':'y','1100':'z','01111':'1','00111':'2','00011':'3',
                    '00001':'4','00000':'5','10000':'6','11000':'7','11100':'8','11110':'9','11111':'0'}

    # Setup for connection with Arduino serial port
    def __init__(self):
        self.serial_port = arduino_connect.pc_connect()
        self.reset()

    # Resets the message, word and symbol
    def reset(self):
        self.current_message = ''
        self.current_word = ''
        self.current_symbol = ''

    # Reads a number between 1-4 from the Arduino serial port
    def read_one_signal(self,port=None):
        connection = port if port else self.serial_port
        while True:
            # Reads the input from the arduino serial connection
            data = connection.readline()
            if data:
                return data

    # Examine the recently-read signal and call one of several methods, depending
    # upon the signal type. If it is a dot or dash, then call update current symbol; if it is a pause, then call
    # handle_symbol_end() or handle_word_end() depending upon the type of pause
    def process_signal(self,signal):
        print("Process signal: "+str(signal))
        if (signal == 0 or signal == 1):
            self.update_current_symbol(signal)
        elif (signal == 2):
            self.handle_symbol_end()
        elif (signal == 3):
            self.handle_word_end()

    # Append the current dot or dash onto the end of current symbol
    def update_current_symbol(self,signal):
        self.current_symbol += str(signal)

    # When the code for a symbol ends, use that code as a key into morse codes
    # to find the appropriate symbol, which is then used as the argument in a call to update current word.
    # Finally, reset current symbol to the empty string
    def handle_symbol_end(self):
            try:
                code = self._morse_codes[self.current_symbol]
                print("Code:"+str(code))
                self.update_current_word(code)
                self.current_symbol = ''
            except KeyError:
                print("Feil1")

    # Add the most recently completed symbol onto current_word.
    def update_current_word(self,symbol):
        self.current_word += symbol

    # This should begin by calling handle_symbol_end;  it should then print current_word
    # to the screen and, finally, reset current word to the empty string.
    def handle_word_end(self):
        self.handle_symbol_end()
        print(self.current_word)
        self.reset()

    # Loop
    def loop(self):
        while True:
            s = self.read_one_signal(self.serial_port)
            print(s)
            for byte in s:
                self.process_signal(int(chr(byte)))

def run():
    m = mocoder()
    m.loop()

run()