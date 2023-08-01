from machine import *
import time
import math


oneInc = Pin(16, Pin.IN, Pin.PULL_DOWN)
tenInc = Pin(17, Pin.IN, Pin.PULL_DOWN)
hundredInc = Pin(18, Pin.IN, Pin.PULL_DOWN)
oneDec = Pin(19, Pin.IN, Pin.PULL_DOWN)
tenDec = Pin(20, Pin.IN, Pin.PULL_DOWN)
hundredDec = Pin(21, Pin.IN, Pin.PULL_DOWN)
flush = Pin(22, Pin.IN, Pin.PULL_DOWN)
modeSwtich = Pin(11, Pin.IN, Pin.PULL_DOWN)
confirmPin = Pin(10, Pin.IN, Pin.PULL_DOWN)
mode_pins = [{ "mode" : "add", "pin" : 15, "state" : False},{ "mode" : "subtract", "pin" : 14, "state" : False},{ "mode" : "multiply", "pin" : 13, "state" : False},{ "mode" : "divide", "pin" : 12, "state" : False}]
led_pins = [8, 7, 6, 5, 4, 3, 2, 1,0]
leds = [machine.Pin(pin, machine.Pin.OUT) for pin in led_pins]
modeLeds = [machine.Pin(led["pin"], machine.Pin.OUT) for led in mode_pins]

curNum = 0
# Define a global variable to keep track of the number of times the function is called
call_count = 0

def modeSwitch():
    global call_count

    for i, led in enumerate(mode_pins, start=1):
        if led["state"]:
            led["state"] = False
            modeLeds[i - 1].toggle()
            try:
                mode_pins[i]["state"] = True
                modeLeds[i].toggle()
                break
            except IndexError:
                break


    # Increment the call_count
    call_count += 1

    # Check if the function has been called four times and reset the states
    if call_count == 5:
        for led in mode_pins:
            led["state"] = False
            for led in modeLeds : led.value(0)
        call_count = 0
        return
        
    
    if not any(led["state"] for led in mode_pins):
        mode_pins[0]["state"] = True
        modeLeds[0].toggle()


    
def activateLeds(num):
    for led in leds:
        led.value(0)
    i = 0
    if num == 0:
        return
    while num != 0:
        binaryBool = num % 2
        num //= 2
        leds[i].value(binaryBool)
        i += 1

def clear():
    global curNum
    curNum = 0
    activateLeds(curNum)

def incrementFunc(increment):
    global curNum
    if (curNum + increment) > math.pow(2,len(leds)):
        curNum == math.pow(2,len(leds))
        return
    curNum += increment
    print(curNum)
    activateLeds(curNum)
    
def decrementFunc(decrement):
    global curNum
    if (curNum - decrement) < 0:
        curNum == 0
        return 
    curNum -= decrement
    print(curNum)
    activateLeds(curNum)
    
while True:
    if oneInc.value():
        print("Incrementing by 1")
        incrementFunc(1)
        time.sleep(0.3)
    if tenInc.value():
        print("Incrementing by 10")
        incrementFunc(10)
        time.sleep(0.3)
    if hundredInc.value():
        print("Incrementing by 100")
        incrementFunc(100) 
        time.sleep(0.3)
    if oneDec.value():
        print("Decrementing by 1")
        decrementFunc(1)
        time.sleep(0.3)
    if tenDec.value():
        print("Decrementing by 10")
        decrementFunc(10)
        time.sleep(0.3)
    if hundredDec.value():
        print("Decrementing by 100")
        decrementFunc(100) 
        time.sleep(0.3)
    if flush.value():
        clear()
    if modeSwtich.value():
        modeSwitch()
        for pin in mode_pins:
            print(f"{pin['mode']} : {pin['state']}")
        print("______________")
        time.sleep(0.3)
    if confirmPin.value():
        print("confirmed")
        time.sleep(0.3)