import evdev
gamepads = []
devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
count = False

controllers = {"Logitech Gamepad F310","Logitech Gamepad F710","Microsoft X-Box 360 pad","Logitech Logitech Cordless RumblePad 2", "Logitech Logitech Dual Action"}
n = len(controllers)
for i in devices:
    if i.name in controllers:
        gamepad = i

#assert device.name in controllers

print("your gamepad is:",gamepad)

for event in gamepad.read_loop():
    try:
        code = event.code
        value = event.value
        if code != 0:
           print('Code: ',code,'Value: ', value)
    except:
        print('break')
