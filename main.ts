input.onGesture(Gesture.EightG, function () {
    if (sound_mode == false && tolerance == "8g") {
        hit_recieved()
    }
})
bluetooth.onBluetoothConnected(function () {
    basic.showString("O")
    basic.showLeds(`
        # . . . .
        # . . . .
        # # # . .
        # . . . .
        # . . . .
        `)
    serial.writeLine("Connected to phone via bluetooth")
    is_bt_connected = true
})
bluetooth.onBluetoothDisconnected(function () {
    basic.showLeds(`
        . . . . #
        . . . . #
        . . # # #
        . . . . #
        . . . . #
        `)
    serial.writeLine("Disconnected Bluetooth")
    is_bt_connected = false
})
input.onGesture(Gesture.SixG, function () {
    if (sound_mode == false && tolerance == "6g") {
        hit_recieved()
    }
})
input.onSound(DetectedSound.Loud, function () {
    if (sound_mode == true) {
        hit_recieved()
    }
})
bluetooth.onUartDataReceived(serial.delimiters(Delimiters.Hash), function () {
    command = bluetooth.uartReadUntil(serial.delimiters(Delimiters.Hash))
    serial.writeLine("" + (command))
    basic.showLeds(`
        . . . . .
        . . . . .
        . . . . .
        # . . . .
        . . . . .
        `)
    basic.pause(100)
    basic.showLeds(`
        . . . . .
        . . . . .
        . . . . .
        # . # . .
        . . . . .
        `)
    basic.pause(100)
    basic.showLeds(`
        . . . . .
        . . . . .
        . . . . .
        # . # . #
        . . . . .
        `)
    basic.pause(100)
    if (command.includes("TOLE")) {
        tolerance = command.split(":")[1]
        basic.showString("T=" + tolerance)
    } else if (command.includes("RATE")) {
        rate = parseFloat(command.split(":")[1])
        basic.showString("R=" + rate)
    } else if (command.includes("SNDM")) {
        sound_mode = 1 == parseFloat(command.split(":")[1])
        basic.showString("S=" + sound_mode)
    }
    basic.pause(500)
    basic.clearScreen()
})
function hit_recieved () {
    if (is_bt_connected) {
        if (input.runningTime() > last_punch_time + rate) {
            bluetooth.uartWriteString("HIT")
            last_punch_time = input.runningTime()
            basic.showLeds(`
                # . . . #
                . # . # .
                . . # . .
                . # . # .
                # . . . #
                `)
            serial.writeLine("HIT")
        }
        basic.pause(3)
        basic.clearScreen()
    } else {
        serial.writeLine("Not BT connected/on sound mode")
    }
}
input.onGesture(Gesture.ThreeG, function () {
    if (sound_mode == false && tolerance == "3g") {
        hit_recieved()
    }
})
let last_punch_time = 0
let command = ""
let is_bt_connected = false
let sound_mode = false
let rate = 0
let tolerance = ""
basic.showString("Sens.ai")
bluetooth.startUartService()
tolerance = "3g"
let average_g = 1024
rate = 20
sound_mode = false
let all_in_1000ms: number[] = []
let game_mode = "gameHRP"
