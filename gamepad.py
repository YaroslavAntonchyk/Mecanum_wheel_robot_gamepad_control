import pygame
import serial
import time
def init_serial(port="COM16", baud=115200):
    ser = serial.Serial(port, baud, timeout=1)
    # open the serial port
    if ser.isOpen():
        print(ser.name + ' is open...')
    return ser

def send_message(ser, message):
    message = str(message)
    print(message)
    for char in message:
        ser.write(bytes(char, 'ascii'))
    # if ser.readable():
    #     out = ser.read_until()
    #     print('Receiving... ' + str(out, 'ascii'))

def constraint(val, up_lim, bot_lim):
    if val > up_lim:
        return up_lim
    elif val < bot_lim:
        return bot_lim
    else:
        return val

def main():
    prev_axis = []
    # init gamepad
    pygame.init()
    j = pygame.joystick.Joystick(0)
    j.init()
    message = ""
    sp = init_serial()
    axes = j.get_numaxes()
    for i in range(axes):
        prev_axis.append(0)

    while True:
        pygame.event.pump()
        for i in range(axes):
            axis = constraint(int((j.get_axis(i) + 1) * 100), 200, 0)
            if 105 >= axis >= 95:
                axis = 100
            if prev_axis[i] != axis:
                if i == 3:
                    message += str(axis) + "y"
                elif i == 2:
                    message += str(axis) + "x"
                elif i == 1:
                    message += str(axis) + "f"
            prev_axis[i] = axis
        time.sleep(0.05)
        # print(message)
        if len(message) > 0:
            send_message(sp, message)
        message = ""
        if sp.readable():
            out = sp.read_until()
            print('Receiving... ' + str(out, 'ascii'))

main()
