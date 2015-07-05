import RPi.GPIO as IO
import time
import sys
from sys import stderr
from subprocess import call

IO.setmode(IO.BOARD);
IO.setup(12,IO.OUT);    # LED GPIO 18
IO.setup(16,IO.OUT);    # LED GPIO 23 
IO.setup(18,IO.OUT);    # LED GPIO 24 
IO.setup(7,IO.IN);      # Detecteur GPIO 4


logFileName = "/home/pi/detectOut/detect.log"
removeFiles = "rm /home/pi/detectOut/*"
dropboxSync = "/home/pi/Dropbox-Uploader/dropbox_uploader.sh -f /home/pi/.dropbox_uploader -s upload /home/pi/detectOut /"
photoDayligth = "raspistill -n -t 1000 -ISO 200 -ex auto -ev 0 -o /home/pi/detectOut/"
#photoNigthligth = "raspistill -n -ex nigth /home/pi/detectOut/"

lastCurrentDay = time.strftime("%d");

def Detect_RemoveFiles():
	global lastCurrentDay;
	currentDay = time.strftime("%d");
	if (currentDay != lastCurrentDay):
		logfile.write(removeFiles + "\n");
		call(removeFiles, shell=True);
		lastCurrentDay = currentDay;
	
def Detect_Smile():
	#build filename
	filename = time.strftime("%m-%d_%H-%M-%S");
	filename += ".jpg";

	#take photo
	try:
		retcode = call(photoDayligth + filename, shell=True);
		logfile.write(photoDayligth + filename + "=" + format(retcode) + "\n");
		if retcode < 0:
			print >> stderr, "Child was terminated by signal", -retcode
	except OSError as e:
		print >> stderr, "Call take photo execution failed:", e	

def Detect_SaveInCloud():
	try:
		retcode = call(dropboxSync, shell=True);
		logfile.write(dropboxSync + format(retcode) + "\n");
		if retcode < 0:
			print >> stderr, "Child was terminated by signal", -retcode
	except OSError as e:
		print >> stderr, "Execution failed:", e	

def Detect_Start():
	TakePhoto = False;

	try:
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
				Detect_RemoveFiles();
                		Detect_Smile();

	        		#upload file in the cloud
                		IO.output(12,False);
        			IO.output(18,True);
				Detect_SaveInCloud();
		        	IO.output(18,False);
	
	except:
		logfile.write("Main loop unexpected error:" + format(sys.exc_info()[0]) + "\n");

logfile = open(logFileName, 'w');
Detect_Start();
logfile.close();
