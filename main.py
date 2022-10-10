from pydexcom import Dexcom
import time
from rpi_epd2in7.rpi_epd2in7.epd import EPD
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import json
import os

USERNAME = ""
PASSWORD = ""

def get_credentials_json():
    global USERNAME, PASSWORD
    
    # get current directory for file
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    filename = os.path.join(file_dir, "credentials.json")

    # Open and dump file
    file = open(filename)
    file_contents = file.read()
    print(file_contents)
    file.close()

    # Decode JSON and save credentials in memory
    decoded_json = json.loads(file_contents)
    USERNAME = str(decoded_json["username"])
    PASSWORD = str(decoded_json["password"])

def main():
    global USERNAME, PASSWORD 

    # Get latest credentials from the json "credentials.json"
    get_credentials_json()
    
    # Initialize Waveshare Python Library
    display = EPD()
    display.init()
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 110)
    image = Image.new('1', (display.height, display.width), 255)
    draw = ImageDraw.Draw(image)
    
    # Initialize Dexcom Glucose Measurement REST API
    dexcom = Dexcom(USERNAME, PASSWORD)
    
    while True:
        # Get current glucose data and post it!
        current_glucose_data = dexcom.get_current_glucose_reading()
        draw.text((15, 5), str(current_glucose_data.value), font=font, fill=0)


        display.smart_update(image.transpose(Image.ROTATE_270))
        # Readings are only every 15 minutes anyway
        time.sleep(140)

main()