import RPi.GPIO as IO
import time
import os

IO.setmode(IO.BOARD);
IO.setup(12,IO.OUT);    # LED GPIO 18
IO.setup(7,IO.IN);      # Detecteur GPIO 4
TakePhoto = False;

dropboxSync = "/home/pi/Dropbox-Uploader/dropbox_uploader.sh -s upload /home/pi/Detect /Detect"

photoDayligth = "raspistill -n -ISO 200 -ex auto -ev 0 -o /home/pi/Detect/"
#photoNigthligth = "raspistill -n -ex nigth /home/pi/Detect/"


def Smile():
        #build filename
        filename = time.strftime("%m-%d_%H-%M-%S");
        filename += ".jpg";

        #take photo
        os.system(photoDayligth + filename);
        time.sleep(5);

        #upload file in the cloud
        os.system(dropboxSync);

while (1):
        time.sleep(1);

        if (IO.input(7) == True and TakePhoto == False ):
                TakePhoto = True;
                IO.output(12,True);
        else:
                TakePhoto = False;
                IO.output(12,False);

        if (TakePhoto == True):
                Smile();
