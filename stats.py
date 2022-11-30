# Needed Libraries
import time
import board
import busio
import subprocess
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

# Display Configuration
i2c = busio.I2C(board.SCL, board.SDA)
width = 128
height = 64
disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

# Clear display.
disp.fill(0)
disp.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Constants that allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same d>
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('Minecraftia.ttf', 8)

while True:

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Shell scripts for system monitoring from here : https://unix.stackexchang>
    cmd = "hostname -i | cut -f 2 -d ' '"
    IP = subprocess.check_output(cmd, shell = True )
    cmd = "vcgencmd measure_temp | cut -f 2 -d '='"
    temp = subprocess.check_output(cmd, shell = True )
    cmd = "top -bn1 | grep load | awk '{printf \"CPU: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell = True )
    cmd = "free -m | awk 'NR==2{printf \"RAM: %s/%sMB %.2f%%\", $3,$2,$3*100/$2>
    MemUsage = subprocess.check_output(cmd, shell = True )
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell = True )

    # Write lines of text.
    draw.text((x, top),       "FurrOS" , font=font, fill=255)
    draw.text((x, top+8),     "Beta 0.1.6", font=font, fill=255)
    draw.text((x, top+16),    "IP: " + str(IP, 'utf-8'),  font=font, fill=255)
    draw.text((x, top+24),    str(CPU, 'utf-8'), font=font, fill=255)
    draw.text((x, top+32),    "Temp:" + str(temp, 'utf-8'), font=font, fill=255)
    draw.text((x, top+40),    str(MemUsage, 'utf-8'),  font=font, fill=255)
    draw.text((x, top+48),    str(Disk, 'utf-8'),  font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.show()
    time.sleep(.1)
