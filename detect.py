import RPi.GPIO as IO
import time
import sys
import logging
from subprocess import call
from os import remove

IO.setmode(IO.BOARD);
IO.setup(12,IO.OUT);    # LED GPIO 18
IO.setup(16,IO.OUT);    # LED GPIO 23 
IO.setup(18,IO.OUT);    # LED GPIO 24 
IO.setup(7,IO.IN);      # Detecteur GPIO 4

outDir = "/home/pi/detectOut/"
dropboxSync = "/home/pi/Dropbox-Uploader/dropbox_uploader.sh -f /home/pi/.dropbox_uploader upload " + outDir + " /"
photoDayligth = "raspistill -n -t 1000 -ISO 200 -ex auto -ev 0 -o "
photoNigthligth = "raspistill -n -ex nigth -o "

def main():
	logging.basicConfig(filename=outDir+"detect.log",level=logging.INFO)
	Detect_Start();

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
				#build filename
				filename = outDir + time.strftime("%m-%d_%H-%M-%S");
				filename += ".jpg";

				#take picture
                                Detect_Smile(filename);

                                #upload file in the cloud
                                IO.output(12,False);
                                IO.output(18,True);
                                Detect_SaveInCloud();
				
				#delete file
				remove(filename);
                                IO.output(18,False);

        except:
                logging.error("Main loop unexpected error: %s", format(sys.exc_info()[0]));

def Detect_Smile(filename):

	#take picture 
	try:
		retcode = call(photoDayligth + filename, shell=True);
		logging.info(photoDayligth + filename + "=" + format(retcode));
		if retcode < 0:
			logging.error("Detect_Smile Child was terminated by signal %x", -retcode);
	except OSError as e:
		logging.error("Call take photo execution failed:" + e);

def Detect_SaveInCloud():
	try:
		retcode = call(dropboxSync, shell=True);
		logging.info(dropboxSync + "=" + format(retcode));
		if retcode < 0:
			logging.error("Call dropbox was terminated by signal %x", retcode);
	except OSError as e:
		logging.error("Execution failed:" + e);	

# MAIN
if __name__ == '__main__':
    main()

