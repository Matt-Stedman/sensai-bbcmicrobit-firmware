def on_gesture_eight_g():
    if sound_mode == False and tolerance == "8g":
        hit_recieved()
input.on_gesture(Gesture.EIGHT_G, on_gesture_eight_g)

def on_bluetooth_connected():
    global is_bt_connected
    basic.show_string("O")
    basic.show_leds("""
        # . . . .
                # . . . .
                # # # . .
                # . . . .
                # . . . .
    """)
    serial.write_line("Connected to phone via bluetooth")
    is_bt_connected = True
bluetooth.on_bluetooth_connected(on_bluetooth_connected)

def on_bluetooth_disconnected():
    global is_bt_connected
    basic.show_leds("""
        . . . . #
                . . . . #
                . . # # #
                . . . . #
                . . . . #
    """)
    serial.write_line("Disconnected Bluetooth")
    is_bt_connected = False
bluetooth.on_bluetooth_disconnected(on_bluetooth_disconnected)

def on_gesture_six_g():
    if sound_mode == False and tolerance == "6g":
        hit_recieved()
input.on_gesture(Gesture.SIX_G, on_gesture_six_g)

def on_sound_loud():
    if sound_mode == True:
        hit_recieved()
input.on_sound(DetectedSound.LOUD, on_sound_loud)

def on_uart_data_received():
    global command, tolerance, rate, sound_mode
    command = bluetooth.uart_read_until(serial.delimiters(Delimiters.HASH))
    serial.write_line("" + (command))
    basic.show_leds("""
        . . . . .
                . . . . .
                . . . . .
                # . . . .
                . . . . .
    """)
    basic.pause(100)
    basic.show_leds("""
        . . . . .
                . . . . .
                . . . . .
                # . # . .
                . . . . .
    """)
    basic.pause(100)
    basic.show_leds("""
        . . . . .
                . . . . .
                . . . . .
                # . # . #
                . . . . .
    """)
    basic.pause(100)
    if command.includes("TOLE"):
        tolerance = command.split(":")[1]
        basic.show_string("T=" + tolerance)
    elif command.includes("RATE"):
        rate = parse_float(command.split(":")[1])
        basic.show_string("R=" + str(rate))
    elif command.includes("SNDM"):
        sound_mode = 1 == parse_float(command.split(":")[1])
        basic.show_string("S=" + str(sound_mode))
    basic.pause(500)
    basic.clear_screen()
bluetooth.on_uart_data_received(serial.delimiters(Delimiters.HASH), on_uart_data_received)

def hit_recieved():
    global last_punch_time
    if is_bt_connected:
        if input.running_time() > last_punch_time + rate:
            bluetooth.uart_write_string("HIT")
            last_punch_time = input.running_time()
            basic.show_leds("""
                # . . . #
                                . # . # .
                                . . # . .
                                . # . # .
                                # . . . #
            """)
            serial.write_line("HIT")
        basic.pause(3)
        basic.clear_screen()
    else:
        serial.write_line("Not BT connected/on sound mode")

def on_gesture_three_g():
    if sound_mode == False and tolerance == "3g":
        hit_recieved()
input.on_gesture(Gesture.THREE_G, on_gesture_three_g)

last_punch_time = 0
command = ""
is_bt_connected = False
sound_mode = False
rate = 0
tolerance = ""
basic.show_string("Sens.ai")
bluetooth.start_uart_service()
tolerance = "3g"
average_g = 1024
rate = 20
sound_mode = False
all_in_1000ms: List[number] = []
game_mode = "gameHRP"