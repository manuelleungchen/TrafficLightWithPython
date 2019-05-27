import RPi.GPIO as GPIO
import time
import socket

# This CODE should be run first
 
out_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

local_IP = "192.168.0.171"
Primary_IP = "192.168.0.127"
UDP_port = 2551
Primary_port = 2550

in_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
in_socket.bind((local_IP, UDP_port))

# GPIO variables
sensor = 8
green = 11
yellow = 13
red = 15

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensor, GPIO.IN)
GPIO.setup(green, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(yellow, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(red, GPIO.OUT, initial = GPIO.LOW)

while True:
    # Waiting for command for primary_pi
    incomingdata, addr = in_socket.recvfrom(1024)
    de_data = incomingdata.decode("utf-8")
    print("Waiting for action")

    if de_data == "Change Red":   # Keep All LEDs OFF 
        # Turn ON the LED red
        greenLedState = GPIO.input(green)  # Chenque if Green LED is ON
        
        if greenLedState:  # If Green LED is ON, change light from Green to Red 
            GPIO.output(green, GPIO.LOW)
            GPIO.output(yellow, GPIO.HIGH)
            GPIO.output(red, GPIO.LOW)
            time.sleep(0.5)
            GPIO.output(green, GPIO.LOW)  
            GPIO.output(yellow, GPIO.LOW)
            GPIO.output(red, GPIO.HIGH)
            print("I am Red")
            
            if GPIO.input(sensor) == False:   # Request to be Green
                time.sleep(0.5)
                data = "Motion on Secondary"
                sdata = data.encode("ascii")
                out_socket.sendto(sdata, (Primary_IP, Primary_port))
        
            else:
                time.sleep(0.5)
                data = "No Motion on Secondary"
                sdata = data.encode("ascii")
                out_socket.sendto(sdata, (Primary_IP, Primary_port))
        
            
        else:  # If Red LED is ON, keep it ON   
            GPIO.output(green, GPIO.LOW)  
            GPIO.output(yellow, GPIO.LOW)
            GPIO.output(red, GPIO.HIGH)

            if GPIO.input(sensor) == False:   # Request to be Green
                time.sleep(1)
                data = "Motion on Secondary"
                sdata = data.encode("ascii")
                out_socket.sendto(sdata, (Primary_IP, Primary_port))
        
            else:
                time.sleep(1)
                data = "No Motion on Secondary"
                sdata = data.encode("ascii")
                out_socket.sendto(sdata, (Primary_IP, Primary_port))
        
    elif de_data == "Change Green":
        # Turn ON Green LED
        time.sleep(1)   # Wait until the Primary Pi is Red
        GPIO.output(green, GPIO.HIGH)
        GPIO.output(yellow, GPIO.LOW)
        GPIO.output(red, GPIO.LOW)
        print("I am Green")
        
        if GPIO.input(sensor) == False:   # Request to be Green
            time.sleep(1)
            data = "Motion on Secondary"
            sdata = data.encode("ascii")
            out_socket.sendto(sdata, (Primary_IP, Primary_port))
        
        else:
            time.sleep(1)
            data = "No Motion on Secondary"
            sdata = data.encode("ascii")
            out_socket.sendto(sdata, (Primary_IP, Primary_port)) 
               
GPIO.cleanup() # Set pins back to Input.

