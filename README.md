# Live-Glucose-Meter-E-Ink
### Description
This is just a little script I wrote that allows me to see my blood sugar on an E-ink display attached to a raspberry pi.

##Instructions
1) Image Raspberry Pi
2) Enable SPI in Raspi-config
3) git clone this reposity
4) Put in Dexcom credentials into the "credentials.json" file
5) Install python3 using "sudo apt install python3" if it isn't installed already
6) Add pydexcom into your python3 installation by typing "pip3 install pydexcom"
7) Run the app by typing "python3 main.py"
  7a) If you want to run the app in the background, type "nohup python3 main.py &"
  7b) If you want it to start getting the data upon bootup, you can add the commands into your init.rc file. More can be found here: 
