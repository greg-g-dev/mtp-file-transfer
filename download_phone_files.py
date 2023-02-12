# Using HomeBrew, install libmtp . The mtpy module relies on this library.
# Changes made to original mtpy module to get it to run on MacOS:
# line 29 mtp = ct.cdll.LoadLibrary("libmtp.so.9") changed to:
# mtp = ct.cdll.LoadLibrary("libmtp.9.dylib")
# line 54 libc = ct.cdll.LoadLibrary("libc.so.6") changed to:
# libc = ct.cdll.LoadLibrary("libc.dylib")

import os.path
import inspect
from datetime import datetime
from importlib import reload
try:
    import mtpy
except:
    # try re-loading in case wrong file is cached
    reload(mtpy)
print('-'*len(inspect.getfile(mtpy)))
print('Located mtpy module needed for MTP file transfers:')
print(inspect.getfile(mtpy))
print('-'*len(inspect.getfile(mtpy)))

# Get User Downloads folder
LOCAL_DOWNLOAD_FOLDER = os.path.expanduser('~/Downloads')
LOCAL_CAMERA_SUBDIR = '/camera'
LOCAL_RECORDINGS_SUBDIR = '/recordings'
PHONE_CAMERA_FOLDER = '/DCIM/Camera'
PHONE_RECORDING_FOLDER = '/Recordings'

#mtpy provides access to (some of) the functions of libmtp from Python
#3.x. It tries to do this in a high-level, convenient fashion. Examples:
print("Checking if phone is connected and accessible...")
while True:
    
    try:
        devices_connected = mtpy.get_raw_devices()
        print("Device(s) found")
        print('Device(s) connected:', devices_connected)
        break

    except Exception as e:
        print('Oops. Something went wrong:')
        print(e)
        print('Check that: 1) phone is turned on AND 2) connected to computer and 3) MTP enabled')
        try_again = input('<Enter> to try again or (e) to exit: ')

        if try_again == 'e':
            exit()

try:
    #returns a list of all the recognizable MTP-speaking devices connected
    #to your host machine, as a list of RawDevice objects.
    device = mtpy.get_raw_devices()[0]
    dev = mtpy.get_raw_devices()[0].open()
    print('Open connection to device:')
    print('Vendor: ', dev.vendor)
    print('Product: ', dev.product)
    #print('Manufacturer: ', dev.get_manufacturer_name())
    print('Model Name:', dev.get_model_name())
    #print('Friendly Name: ', dev.get_friendly_name())
    #print('Battery Level: ', dev.get_battery_level())
    #print('Supported file types: ', dev.get_supported_filetypes())


    LOCAL_PHONE_SUBDIR = '/' + dev.get_model_name().replace(' ', '_')
    
    #returns a Device object for communicating with the first (or only) MTP
    #device connected to your system, and saves it in the variable dev.
    
    while True:
        print()
        print('---------------------------------')
        print('-- What Would You Like To Do?  --')
        print('---------------------------------')
        print('(1) List Camera Files')
        print('(2) Download Camera Files')
        print('(3) List Audio Recordings')
        print('(4) Download Audio Recordings')
        print('(5) List Phone File Folders')
        print('(Enter) Enter no option to Exit')
        print('---------------------------------')
        folder_choice = input('Enter selection: ')
        print()

        #returns a list of the files and folders at the root directory level
        #on the Device. (The first such call is liable to take a few seconds,
        #accompanied by some diagnostic messages from libmtp.)

        if folder_choice == '1':
            picture_folder = dev.get_descendant_by_path(PHONE_CAMERA_FOLDER)
            print('Camera Folder: ', picture_folder)
            pictures = picture_folder.get_children()
            for picture in pictures:
                print('Pictures in folder: ', picture)


        elif folder_choice == '2':
            picture_folder = dev.get_descendant_by_path(PHONE_CAMERA_FOLDER)
            print('Camera Folder: ', picture_folder)

                # Download camera files to local folder.
            if not os.path.exists(LOCAL_DOWNLOAD_FOLDER + LOCAL_PHONE_SUBDIR):
                os.mkdir(LOCAL_DOWNLOAD_FOLDER + LOCAL_PHONE_SUBDIR)
            if not os.path.exists(LOCAL_DOWNLOAD_FOLDER + LOCAL_PHONE_SUBDIR + LOCAL_CAMERA_SUBDIR):
                os.mkdir(LOCAL_DOWNLOAD_FOLDER + LOCAL_PHONE_SUBDIR + LOCAL_CAMERA_SUBDIR)
            print('Downloading camera files to: ', LOCAL_DOWNLOAD_FOLDER + LOCAL_PHONE_SUBDIR + LOCAL_CAMERA_SUBDIR)
            picture_folder.retrieve_to_folder(LOCAL_DOWNLOAD_FOLDER + LOCAL_PHONE_SUBDIR + LOCAL_CAMERA_SUBDIR)
            print('Downloading complete.')            
            
        elif folder_choice == '3':
            recording_folder = dev.get_descendant_by_path(PHONE_RECORDING_FOLDER)
            print('Recordings Folder: ', recording_folder)
            recordings = recording_folder.get_children()
            for recording in recordings:
                print('Recordings in folder: ', recording)


        elif folder_choice == '4':
            recording_folder = dev.get_descendant_by_path(PHONE_RECORDING_FOLDER)
            print('Recordings Folder: ', recording_folder)

                # Download audio recordings to local folder.
            if not os.path.exists(LOCAL_DOWNLOAD_FOLDER + LOCAL_PHONE_SUBDIR):
                os.mkdir(LOCAL_DOWNLOAD_FOLDER + LOCAL_PHONE_SUBDIR)
            if not os.path.exists(LOCAL_DOWNLOAD_FOLDER + LOCAL_PHONE_SUBDIR + LOCAL_RECORDINGS_SUBDIR):
                os.mkdir(LOCAL_DOWNLOAD_FOLDER + LOCAL_PHONE_SUBDIR + LOCAL_RECORDINGS_SUBDIR)
            print('Downloading recording files to: ', LOCAL_DOWNLOAD_FOLDER + LOCAL_PHONE_SUBDIR + LOCAL_RECORDINGS_SUBDIR)
            recording_folder.retrieve_to_folder(LOCAL_DOWNLOAD_FOLDER + LOCAL_PHONE_SUBDIR + LOCAL_RECORDINGS_SUBDIR)
            print('Downloading complete.')

        elif folder_choice == '5':
            all_folders = dev.get_children()
            for folder in all_folders:
                print('Folders available on device: ', folder)

        else:
            print('Exiting. B-bye')
            break

        

        #on my Samsung Galaxy Nexus, returns a Folder object for the location
        #where the Camera app puts its photos, and saves it in the variable p.
        #pictures = picture_folder.get_children()
        #for picture in pictures:
        #    print('Pictures in folder: ', picture)

        #returns a list of the photos currently in the /DCIM/Camera folder.

        #picture_folder.retrieve_to_folder("/Users/greggauthier/Downloads/linkii_photos")

        #will download the entire contents of the photos folder into the local
        #directory “all_photos”, which will be created if it doesn’t exist.

            #d1 = dev.create_folder("test")

        #creates a folder named “test” at the root directory level on the
        #Device, and saves the returned Folder object describing it in the
        #variable d1.

            #d2 = d1.create_folder("also_test")

        #creates a folder named “also_test” within the previously-created
        #“test” folder, and saves the returned Folder object describing it in
        #the variable d2.

            #f3 = d2.send_file("photo.jpeg", "photo.jpg")

        #sends the file named “photo.jpeg” to the previously-created
        #“also_test” folder on the device, giving it the full uploaded pathname
        #of “/test/also_test/photo.jpg”.

          #  f3.retrieve_to_file("photo-too.jpeg")

        #downloads the uploaded file under the name “photo-too.jpeg” to the host
        #system.

         #   f3.delete()

        #deletes the uploaded copy of the file. The object in f3 should not
        #be referenced after this point.

         #   d1.delete()

        #will fail, because the folder “test” is not empty (contains the
        #subfolder “also_test”).

        #    d1.delete(delete_descendants = True)

        #will delete the folder “test” and all its descendants (i.e. the Folder
        #described by d2). The objects in d1 and d2 should not be referenced
        #after this point.

    dev.close()

    

    #Licence: LGPL2+, same as libmtp.
    #Credit original test script to:  
    #Lawrence D’Oliveiro

except Exception as e:
    print('Oops. Something went wrong:')
    print(e)

