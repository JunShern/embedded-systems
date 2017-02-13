# embedded-systems
Group coursework for EE3-24 Embedded Systems at Imperial College London

### Getting started

1. Enter REPL using [screen](https://micropython.org/resources/docs/en/latest/wipy/wipy/tutorial/repl.html) (need to use sudo if “screen is terminating”) or follow [these instructions](https://learn.adafruit.com/micropython-basics-how-to-load-micropython-on-a-board/serial-terminal?view=all#serial-terminal)
`sudo screen /dev/ttyUSB0 115200`

2. Try out some basic commands on the [micropython docs](https://docs.micropython.org/en/latest/esp8266/esp8266/quickref.html)

3. Install ampy using `pip install adafruit-ampy` and go through the [docs](https://learn.adafruit.com/micropython-basics-load-files-and-run-code/overview)

### Running the program

1. Create a Python file to run on the device (e.g. main.py - this special name will boot everytime the board is reset)

2. Use ampy to load the file in:
`sudo ampy -p /dev/ttyUSB0 -b 115200 put main.py`
*The `put` command loads the program onto the board but doesn't run it; the correct command for running files is actually `run` but `run` was found to cause errors so use `put` for best results. To view debug and print output, need to use `screen` to talk to the board after the program has been loaded.*

### MQTT Communication Resources
[MQTT overview](http://www.hivemq.com/blog/mqtt-essentials-part-3-client-broker-connection-establishment)
[Installation and setup](http://www.switchdoc.com/2016/02/tutorial-installing-and-testing-mosquitto-mqtt-on-raspberry-pi/)

### Other resources

(Can skip this step since MicroPython is already on the Huzzah’s ESP) 

Flash MicroPython firmware onto ESP8266 - [link](https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/intro.html) (need to determine USB dev path using [this](http://unix.stackexchange.com/questions/144029/command-to-determine-ports-of-a-device-like-dev-ttyusb0))

(Can skip this step too)

Install MicroPython on laptop and run executable to connect - [instructions](http://unix.stackexchange.com/questions/144029/command-to-determine-ports-of-a-device-like-dev-ttyusb0)
