# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
# SPDX-FileCopyrightText: 2017 James DeVito for Adafruit Industries
# SPDX-License-Identifier: MIT

## REF https://pillow.readthedocs.io/

# This example is for use on (Linux) computers that are using CPython with
# Adafruit Blinka to support CircuitPython libraries. CircuitPython does
# not support PIL/pillow (python imaging library)!
import math
from os import stat
import os
import time
import sys, getopt
import subprocess
import json
import smbus

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont, ImageOps
import adafruit_ssd1306

## Global Variables
# Default set, but can be overridden by config in addon setup.
TEMP_UNIT = "C"
SHOW_SPLASH = True
SHOW_CPU = True
SHOW_NETWORK = False
SHOW_MEMORY = True
SHOW_STORAGE = True
DURATION = 5
FAN_ENABLED = True
FAN_TEMP_FULL = 60
FAN_TEMP_HIGH = 55
FAN_TEMP_MEDHIGH = 50
FAN_TEMP_MEDLOW = 45
FAN_TEMP_LOW = 40

bus = smbus.SMBus(1)

addr = 0x0d
fan_reg = 0x08
fan_state = 0
temp = 0
level_temp = 0
rgb_off_reg = 0x07
Max_LED = 3

# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these to the right size for your display!
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Clear display.
disp.fill(0)
disp.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.

width = disp.width
height = disp.height

image = Image.new("1", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)


# Load default font.
# font = ImageFont.load_default()
p = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 9)
p_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 9)
small = ImageFont.truetype("usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 8)
smaller = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 7)


img_network = Image.open(r"./img/ip-network.png") 
img_mem = Image.open(r"./img/ram.png") 
img_disk = Image.open(r"./img/sd_card.png") 
img_ha_logo = m = Image.open(r"./img/home-assistant-logo.png") 
img_cpu_64 = Image.open(r"./img/cpu_arm.png") 


def start():
    while True:        
        if (SHOW_SPLASH) : show_splash()
        if (FAN_ENABLED) : fan_rgb_operation()
        if (SHOW_CPU) : show_cpu_temp()
        if (FAN_ENABLED) : fan_rgb_operation()
        if (SHOW_MEMORY) : show_memory()
        if (FAN_ENABLED) : fan_rgb_operation()
        if (SHOW_NETWORK) : show_network()
        if (FAN_ENABLED) : fan_rgb_operation()
        if (SHOW_STORAGE) : show_storage()
        if (FAN_ENABLED) : fan_rgb_operation()

def setRGB(num, r, g, b):
    if num >= Max_LED:
        bus.write_byte_data(addr, 0x00, 0xff)
        bus.write_byte_data(addr, 0x01, r&0xff)
        bus.write_byte_data(addr, 0x02, g&0xff)
        bus.write_byte_data(addr, 0x03, b&0xff)
    elif num >= 0:
        bus.write_byte_data(addr, 0x00, num&0xff)
        bus.write_byte_data(addr, 0x01, r&0xff)
        bus.write_byte_data(addr, 0x02, g&0xff)
        bus.write_byte_data(addr, 0x03, b&0xff)

def fan_rgb_operation():

    temp = float(shell_cmd("cat /sys/class/thermal/thermal_zone0/temp")) / 1000.00
    global level_temp
    if abs(temp - level_temp) >= 1:
        if temp <= FAN_TEMP_LOW:
            level_temp = FAN_TEMP_LOW
            setRGB(Max_LED, 0x1e, 0xb6, 0xee)
            bus.write_byte_data(addr, fan_reg, 0x00)

        elif temp <= FAN_TEMP_MEDLOW:
            level_temp = FAN_TEMP_MEDLOW
            setRGB(Max_LED, 0x97, 0x32, 0xc1)
            bus.write_byte_data(addr, fan_reg, 0x05)

        elif temp <= FAN_TEMP_MEDHIGH:
            level_temp = FAN_TEMP_MEDHIGH
            setRGB(Max_LED, 0xf9, 0x63, 0x14)
            bus.write_byte_data(addr, fan_reg, 0x07)

        elif temp <= FAN_TEMP_HIGH:
            level_temp = FAN_TEMP_HIGH
            setRGB(Max_LED, 0xff, 0x8c, 0x00)
            bus.write_byte_data(addr, fan_reg, 0x09)

        elif temp >= FAN_TEMP_FULL:
            level_temp = FAN_TEMP_FULL
            setRGB(Max_LED, 0xff, 0xff, 0xff)
            bus.write_byte_data(addr, fan_reg, 0x01)



def show_storage():
    storage =  shell_cmd('df -h | awk \'$NF=="/"{printf "%d,%d,%s", $3,$2,$5}\'')
    storage = storage.split(',')

    # Clear Canvas
    draw.rectangle((0,0,128,32), outline=0, fill=0)

    # Resize and merge icon to Canvas
    icon = img_disk
    image.paste(icon,(0,0))

    draw.text((33, 0), "USED: " + storage[0] + ' GB \n', font=small, fill=255)
    draw.text((33, 11), "TOTAL: " + storage[1] + ' GB \n', font=small, fill=255)
    draw.text((33, 21), "UTILISED: " + storage[2] + ' \n', font=small, fill=255) 

    #image.save(r"./img/examples/storage.png")    

    disp.image(image)
    disp.show()
    time.sleep(DURATION)  

def show_memory():

    mem = shell_cmd("free -m | awk 'NR==2{printf \"%.1f,%.1f,%.0f%%\", $3/1000,$2/1000,$3*100/$2 }'")
    mem = mem.split(',')

    # Clear Canvas
    draw.rectangle((0,0,128,32), outline=0, fill=0)

    # Resize and merge icon to Canvas
    icon = img_mem
    image.paste(icon,(0,0))

    draw.text((33, 0), "USED: " + mem[0] + ' GB \n', font=small, fill=255)
    draw.text((33, 11), "TOTAL: " + mem[1] + ' GB \n', font=small, fill=255)
    draw.text((33, 21), "UTILISED: " + mem[2] + ' \n', font=small, fill=255)  

    #image.save(r"./img/examples/memory.png")   

    disp.image(image)
    disp.show()
    time.sleep(DURATION) 


def show_cpu_temp():

    #host_info = hassos_get_info('host/info')

    cpu = shell_cmd("top -bn1 | grep load | awk '{printf \"%.2f\", $(NF-2)}'")
    temp = float(shell_cmd("cat /sys/class/thermal/thermal_zone0/temp")) / 1000.00
    uptime = shell_cmd("uptime | grep -ohe 'up .*' | sed 's/,//g' | awk '{ print $2" "$3 }'")

    # Check temapture unit and convert if required.
    if (TEMP_UNIT == 'C'): 
        temp = "%0.2f °C " % (temp)
    else:
        temp = "%0.2f °F " % (temp * 9.0 / 5.0 + 32)


    # Clear Canvas
    draw.rectangle((0,0,128,32), outline=0, fill=0)

    # Resize and merge icon to Canvas
    icon = img_cpu_64#.resize([32,32])  
    image.paste(icon,(0,0))

    draw.text((33, 0), 'TEMP: ' + temp, font=small, fill=255)
    draw.text((33, 11), 'LOAD: '+ cpu + "% ", font=small, fill=255)  
    draw.text((33, 21), uptime.upper(), font=small, fill=255)

    #image.save(r"./img/examples/cpu.png")
    
    disp.image(image)
    disp.show()
    time.sleep(DURATION)


def show_network():
    host_info = hassos_get_info('host/info')
    hostname = host_info['data']['hostname'].upper()

    network_info = hassos_get_info('network/info')
    ipv4 = network_info['data']['interfaces'][0]['ipv4']['address'][0].split("/")[0]

    mac = shell_cmd("cat /sys/class/net/wlan0/address")

    # Clear Canvas
    draw.rectangle((0,0,128,32), outline=0, fill=0)

    # Resize and merge icon to Canvas
    icon = img_network.resize([32,32])  
    image.paste(icon,(0,0))

    draw.text((33, 0), "HOST " + hostname, font=small, fill=255)
    draw.text((33, 11), "IP4 " + ipv4, font=small, fill=226)    
    draw.text((33, 21), "MAC " + mac.upper(), font=small, fill=255)    

    #image.save(r"./img/examples/network.png")

    disp.image(image)
    disp.show()
    time.sleep(DURATION)

def get_text_center(text, font, center_point):
    w, h = draw.textsize(text, font=font)

    return (center_point -(w/2))


def show_splash():

    os_info = hassos_get_info('os/info')    
    os_version = os_info['data']['version']
    os_upgrade = os_info['data']['update_available']  
    if (os_upgrade == True):
        os_version = os_version + "*"

    core_info = hassos_get_info('core/info')
    core_version = core_info['data']['version']  
    core_upgrade = os_info['data']['update_available']
    if (core_upgrade == True):
        core_version =  core_version + "*"


    # Draw a padded black filled box with style.border width.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Get HA Logo and Resize
    logo = img_ha_logo#.resize([32,32])
    # logo = ImageOps.invert(logo)  
    
    # Merge HA Logo with Canvas.
    image.paste(logo,(0,0))

    draw.line([(34, 16),(123,16)], fill=255, width=1)

    ln1 = "Home Assistant"
    ln1_x = get_text_center(ln1, p_bold, 78)
    draw.text((ln1_x, 4), ln1, font=p_bold, fill=255)

    # Write Test, Eventually will get from HA API.
    ln2 = 'OS '+ os_version + ' - ' + core_version
    ln2_x = get_text_center(ln2, small, 78)
    draw.text((ln2_x, 20), ln2, font=small, fill=255)


    # Display Image to OLED
    #image.save(r"./img/examples/splash.png")
    disp.image(image)
    disp.show() 
    time.sleep(DURATION)


def hassos_get_info(type):
    info = shell_cmd('curl -sSL -H "Authorization: Bearer $SUPERVISOR_TOKEN" http://supervisor/' + type)
    return json.loads(info)


def shell_cmd(cmd):
    return subprocess.check_output(cmd, shell=True).decode("utf-8")


def get_options():
    f = open("/data/options.json", "r")
    options = json.loads(f.read())
    global TEMP_UNIT, SHOW_SPLASH, SHOW_CPU, SHOW_MEMORY, SHOW_STORAGE, SHOW_NETWORK, DURATION, FAN_ENABLED, FAN_TEMP_FULL, FAN_TEMP_HIGH, FAN_TEMP_MEDHIGH, FAN_TEMP_MEDLOW, FAN_TEMP_LOW
    TEMP_UNIT = options['Temperature_Unit']
    SHOW_SPLASH = options['Show_Splash_Screen']
    SHOW_CPU = options['Show_CPU_Info']
    SHOW_MEMORY =options['Show_Memory_Info']
    SHOW_STORAGE = options['Show_Storage_Info']
    SHOW_NETWORK = options['Show_Network_Info']
    DURATION =  options['Slide_Duration']
    FAN_ENABLED = options['Enable_Fan']
    FAN_TEMP_HIGH = options['Temperature_High']
    FAN_TEMP_MEDHIGH = options['Temperature_Medium_High']
    FAN_TEMP_MEDLOW = options['Temperature_Medium_Low']
    FAN_TEMP_LOW = options['Temperature_Low']


def clear_display():
    disp.fill(0)
    disp.show()

if __name__ == "__main__":
    get_options()
    start()

