import RPi.GPIO as GPIO
import socket
import time
    
# This Code should be run after running "TrafficLight_secondary_pi"

out_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

local_IP = "192.168.0.127"
send_ip="192.168.0.171"
UDP_port = 2550
Secondary_port = 2551

in_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
in_socket.bind((local_IP, UDP_port))

# GPIO variables
green = 11
yellow = 13
red = 15

GPIO.setmode(GPIO.BOARD)
GPIO.setup(red, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(yellow, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(green, GPIO.OUT, initial = GPIO.HIGH)

drequest = "No Motion on Secondary"  # Assume No motion on second_pi for initial State

while True:
    if drequest == "No Motion on Secondary":
        # Send order to keep second pi Red
        data = "Change Red"
        edata = data.encode("ascii")
        out_socket.sendto( edata , (send_ip, Secondary_port))
            
        # Change to Green 
        time.sleep(1)   # Wait until the Secondary Pi is Red
        GPIO.output(red,0)
        GPIO.output(yellow,0)
        GPIO.output(green,1)         
        print("Im Green")
        
    elif drequest == "Motion on Secondary":
            # Let 2 pi to change to Green
        data = "Change Green"
        edata = data.encode("ascii")
        out_socket.sendto( edata , (send_ip, Secondary_port))
         
        if GPIO.input(red) == 0:  # If Red LED is Off, turn it ON
        # Change to Red
            GPIO.output(red,0)
            GPIO.output(yellow,1)
            GPIO.output(green,0)
            time.sleep(0.5)
            GPIO.output(red,1)
            GPIO.output(yellow,0)
            GPIO.output(green,0)      
            print("Im Red")
        
        else:     # Otherwise Keep Red LED ON
            # Keep Red LED ON
            GPIO.output(red,1)
            GPIO.output(yellow,0)
            GPIO.output(green,0)      
            print("Im Red")
        
    print("Waiting for second_pi status")
        #receive data from secondary 
    req_data, addr = in_socket.recvfrom(1024)
    drequest = req_data.decode("utf-8")
    
GPIO.cleanup()
    
    
    
    
        
        
    
