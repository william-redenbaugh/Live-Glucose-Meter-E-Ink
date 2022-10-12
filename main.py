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
    print("Credentials Entered")
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
    font2 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 30)
    image = Image.new('1', (display.height, display.width), 255)
    draw = ImageDraw.Draw(image)

    # Initialize Dexcom Glucose Measurement REST API
    dexcom = Dexcom(USERNAME, PASSWORD)

    glucose_text_draw = ImageDraw.Draw(image)
    glucose_text_draw.text((15, 120), "Current Glucose", font=font2, fill=0)
    while True:
        try:
            # Get current glucose data and post it!
            current_glucose_data = dexcom.get_current_glucose_reading()
            out = ""
            if current_glucose_data == None:
                out = "N/A"
            else:
                out = str(current_glucose_data.value)

            image = Image.new('1', (display.height, display.width), 255)
            glucose_text_draw = ImageDraw.Draw(image)
            glucose_text_draw.text((15, 120), "Current Glucose", font=font2, fill=0)
            draw = ImageDraw.Draw(image)
            draw.text((15, 5), out, font=font, fill=0)
            display.display_frame(image.transpose(Image.ROTATE_270))
            # Readings are only every 15 minutes anyway
            time.sleep(60)

        # Any error we just recover!
        except Exception as e:
            # Initialize Waveshare Python Library
            display = EPD()
            display.init()
            font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 110)
            font2 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 30)
            image = Image.new('1', (display.height, display.width), 255)
            draw = ImageDraw.Draw(image)

            # Initialize Dexcom Glucose Measurement REST API
            dexcom = Dexcom(USERNAME, PASSWORD)

            glucose_text_draw = ImageDraw.Draw(image)
            glucose_text_draw.text((15, 120), "Current Glucose", font=font2, fill=0)

main()
