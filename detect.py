import RPi.GPIO as IO
import time
import os

IO.setmode(IO.BOARD);
IO.setup(12,IO.OUT);    # LED GPIO 18
IO.setup(16,IO.OUT);    # LED GPIO 23 
IO.setup(18,IO.OUT);    # LED GPIO 24 
IO.setup(7,IO.IN);      # Detecteur GPIO 4


logFile = "/home/pi/detectOut/detect.log"
removeFiles = "rm /home/pi/detectOut/*"
dropboxSync = "/home/pi/Dropbox-Uploader/dropbox_uploader.sh -s upload /home/pi/detectOut /"
photoDayligth = "raspistill -n -t 1000 -ISO 200 -ex auto -ev 0 -o /home/pi/detectOut/"
#photoNigthligth = "raspistill -n -ex nigth /home/pi/detectOut/"

lastCurrentDay = time.strftime("%d");

def FlushDirectory():
	global lastCurrentDay;
	currentDay = time.strftime("%d");
	if (currentDay != lastCurrentDay):
		print (removeFiles);
		os.system(removeFiles);
		lastCurrentDay = currentDay;
	
def Smile():
        #build filename
        filename = time.strftime("%m-%d_%H-%M-%S");
        filename += ".jpg";

        #take photo
        os.system(photoDayligth + filename);
        time.sleep(2); #PiCam takes 1000ms seconds to take a picture
	log.write("Photo "+ filename);

def Start():
	TakePhoto = False;

	while (1):
        	time.sleep(0.7);
               	IO.output(16,True);   # HEARTBEAT LED
        	time.sleep(0.3);
               	IO.output(16,False);

        	if (IO.input(7) == True and TakePhoto == False ):
                	TakePhoto = True;
                	IO.output(12,True);   # NOTIFY DETECTION 
        	else:
                	TakePhoto = False;

        	if (TakePhoto == True):
			FlushDirectory();
                	Smile();

	        	#upload file in the cloud
                	IO.output(12,False);
        		IO.output(18,True);
        		os.system(dropboxSync);
		        IO.output(18,False);

log = open(logFile, 'w');
Start();
