import serial

# Connects to the arduino via a COM port (USB).
# Does not work if the serial monitor in arduino is open.
def pc_connect():
    for i in range(100):
        try:
            arduino = serial.Serial('COM' + str(i), 9600, timeout=.1)
            print("Connected to arduino")
            return arduino
        except serial.SerialException:
            pass
    exit("Arduino was not found")


