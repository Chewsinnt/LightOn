from microbit import *
import math

# Define a function for sending MIDI note messages
def midiNoteSend(chan, n, vel):
    MIDI_NOTE_ON = 0x90
    if chan > 15:
        return
    if n > 127:
        return
    if vel > 127:
        return
    msg = bytes([MIDI_NOTE_ON | chan, n, vel])
    uart.write(msg)

# Define a function for sending MIDI control change messages
def midiControlChange(chan, n, value):
    MIDI_CC = 0xB0
    if chan > 15:
        return
    if n > 127:
        return
    if value > 127:
        return
    msg = bytes([MIDI_CC | chan, n, value])
    uart.write(msg)

# Define a function for setting the uart in to MIDI setting
def Start():
    uart.init(baudrate=31250, bits=8, parity=None, stop=1, tx=pin0)

# Call the Start function
Start()

# Set the pull-up resistors on the input pins
pin13.set_pull(pin13.PULL_UP)
pin14.set_pull(pin14.PULL_UP)
pin15.set_pull(pin15.PULL_UP)
pin16.set_pull(pin16.PULL_UP)

# Define the MIDI note values for the buttons
Button_1_Value = 1
Button_2_Value = 3
Button_3_Value = 5
Button_4_Value = 7
Button_5_Value = 9
Button_6_Value = 11
Button_7_Value = 13
Button_8_Value = 15

# Main loop
while True:

    # Read the state of the buttons
    a = pin1.is_touched()
    b = pin2.is_touched()
    c = pin13.read_digital()
    d = pin14.read_digital()
    e = pin15.read_digital()
    f = pin16.read_digital()
    g = button_a.is_pressed()
    h = button_b.is_pressed()

    last_level = 0
    last_tilt = 0

    # Check if button ... is touched, if so, send a MIDI note message
    if a is True:
        if Button_1_Value == 1: # if pressed, send MIDI note 2
            Button_1_Value = 2
            midiNoteSend(0, Button_1_Value, 127)
        elif Button_1_Value == 2: # if pressed again, send MIDI note 1
            Button_1_Value = 1
            midiNoteSend(0, Button_1_Value, 127)
    while pin1.is_touched(): # sleep while button is on hold to avoid button spamming
        sleep(1)
    if b is True:
        if Button_2_Value == 3:
            Button_2_Value = 4
            midiNoteSend(0, Button_2_Value, 127)
        elif Button_2_Value == 4:
            Button_2_Value = 3
            midiNoteSend(0, Button_2_Value, 127)
    while pin2.is_touched():
        sleep(1)
    if c == False:
        if Button_3_Value == 5:
            Button_3_Value = 6
            midiNoteSend(0, Button_3_Value, 127)
        elif Button_3_Value == 6:
            Button_3_Value = 5
            midiNoteSend(0, Button_3_Value, 127)
    while pin13.read_digital() == False:
        sleep(1)
    if d == False:
        if Button_4_Value == 7:
            Button_4_Value = 8
            midiNoteSend(0, Button_4_Value, 127)
        elif Button_4_Value == 8:
            Button_4_Value = 7
            midiNoteSend(0, Button_4_Value, 127)
    while pin14.read_digital() == False:
        sleep(1)
    if e == False:
        if Button_5_Value == 9:
            Button_5_Value = 10
            midiNoteSend(0, Button_5_Value, 127)
        elif Button_5_Value == 10:
            Button_5_Value = 9
            midiNoteSend(0, Button_5_Value, 127)
    while pin15.read_digital() == False:
        sleep(1)
    if f == False:
        if Button_6_Value == 11:
            Button_6_Value = 12
            midiNoteSend(0, Button_6_Value, 127)
        elif Button_6_Value == 12:
            Button_6_Value = 11
            midiNoteSend(0, Button_6_Value, 127)
    while pin16.read_digital() == False:
        sleep(1)
    if g is True:
        if Button_7_Value == 13:
            Button_7_Value = 14
            midiNoteSend(0, Button_7_Value, 127)
        elif Button_7_Value == 14:
            Button_7_Value = 13
            midiNoteSend(0, Button_7_Value, 127)
    while button_a.is_pressed():
        sleep(1)
    if h is True:
        if Button_8_Value == 15:
            Button_8_Value = 16
            midiNoteSend(0, Button_8_Value, 127)
        elif Button_8_Value == 16:
            Button_8_Value = 15
            midiNoteSend(0, Button_8_Value, 127)
    while button_b.is_pressed():
        sleep(1)
    # Read the light level from the LED display and send a MIDI control change message
    current_level = display.read_light_level()
    if current_level != last_level: 
        midiControlChange(0, 22, current_level)
        last_level = current_level
    # Read the tilt value from the accelerometer and send a MIDI control change message
    current_tilt = accelerometer.get_y()
    if current_tilt != last_tilt:
        # Map the tilt value to a MIDI controller value in the range of 0-127 test
        mod_y = math.floor(math.fabs((((current_tilt + 1024) / 2048) * 127)))
        midiControlChange(0, 23, mod_y)
        last_tilt = current_tilt
    sleep(10)
