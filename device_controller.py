from pyfirmata2 import Arduino, util # type: ignore

board = Arduino('/dev/ttyACM0')  # or COM3 on Windows

led_pins = [2, 3, 4, 5, 6]
leds = [board.digital[pin] for pin in led_pins]

for led in leds:
    led.write(0)

it = util.Iterator(board)
it.start()

def control_leds(finger_status: list):
    # assert type(finger_status) == list and len(finger_status) == 5, "finger_status must be a list of 5 elements"
    print(f"Finger status: {finger_status}, len: {len(finger_status)}")
    try:
        for i in range(0, 5):
            leds[i].write(finger_status[i])
    except IndexError as e:
        print(f"Error: {e}. finger_status must be a list of 5 elements.")
        for led in leds:
            led.write(0)
