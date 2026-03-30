from gpiozero import LED

import time

if __name__ == "__main__":
    ch1 = LED(26, initial_value=True)
    ch2 = LED(20, initial_value=True)
    ch3 = LED(21, initial_value=True)
    """
    # testing all three relais on the board
    print("start test")
    time.sleep(5)
    print("channel 1")
    ch1.off()
    time.sleep(5)
    ch1.on()
    time.sleep(5)
    print("channel 2")
    ch2.off()
    time.sleep(5)
    ch2.on()
    time.sleep(5)
    print("channel 3")
    ch3.off()
    time.sleep(5)
    ch3.on()
    time.sleep(5)
    print("end test")
    """
    # look at the delay of the relais
    print("test starts in 2 seconds")
    time.sleep(2)
    print("about to turn on")
    ch1.off()
    print("turned on")
    time.sleep(5)
    ch1.on()
    print("turned off again")
