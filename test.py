from pyfirmata2 import Arduino, util
import time

board = Arduino('/dev/ttyACM0')
it = util.Iterator(board)
it.start()

# Optional: explicitly set output mode
board.digital[2].mode = 1
board.digital[3].mode = 1
board.digital[13].mode = 1


while True:
    time.sleep(1)  # give time to initialize
    board.digital[2].write(1)
    board.digital[3].write(1)
    board.digital[13].write(1)
    print("LEDs ON")
    time.sleep(1)
    board.digital[2].write(0)
    board.digital[3].write(0)
    board.digital[13].write(0)
    print("LEDs OFF")
    time.sleep(1)
