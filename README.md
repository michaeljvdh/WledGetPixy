* # WLED GetPixy File Processing System User Guide

  

  ```
   _    _  _      _____ ______             
  | |  | || |    |  ___||  _  \            
  | |  | || |    | |__  | | | |            
  | |/\| || |    |  __| | | | |            
  \  /\  /| |____| |___ | |/ /             
   \/  \/ \_____/\____/ |___/              
                                           
                                           
   _____        _   ______  _              
  |  __ \      | |  | ___ \(_)             
  | |  \/  ___ | |_ | |_/ / _ __  __ _   _ 
  | | __  / _ \| __||  __/ | |\ \/ /| | | |
  | |_\ \|  __/| |_ | |    | | >  < | |_| |
   \____/ \___| \__|\_|    |_|/_/\_\ \__, |
                                      __/ |
                                     |___/ 
  - Convert images to WLED 2D Matrixes with ease.
  - Script your own events for an icon change and more.
  
  - By Michael van den Heever
  
  ```


  Buy me a beer, for the love of LED's

  https://www.paypal.com/donate/?business=LWK64EZBGDCRS&no_recurring=0&item_name=Greetings%2C+your+patronage+keeps+me+building+more+for+you.&currency_code=CAD

  
![getpixy](getpixy.jpg)

  ### GetPixy Configuration and Usage Guide

#### Extremely Simple Overview

  - To send images to WLED, they need to be converted to colors per pixel, monitor.py is a script that will run in the background, when you drop an image in the monitor folder it watches it will convert them and send them to WLED 2D Matrix, which should already be configured.  Make sure your on version 14+ with a  2D Matrix - if it's not done ... this ain't gonna work.

  - Questions and Answers

    - Yes you can manually convert single images, and then script your own conditions, timers and so on using your own scheduling methods with push.py to send the frame files to WLED

    - If you have any questions, send them to me at wledgetpixy@outlook.com

  #### Getting Started - For the Python folks
  1. (Optional) dump into your python virtual environment
  2. Install requirements
    `pip install -r requirements.txt`
  3. run python monitor.py
  4. Edit the monitor.cfg and convert.cfg files
  5. Drop your gif into the monitor folder

  #### Getting Started - For the windows users - executable mode
  1. Download the "GetPixy" artifact from github
  2. Extract it
  3. Run  getpixy.exe
  4. Edit the monitor.cfg and convert.cfg files
  5. Drop your gif into the monitor folder

  #### Running `monitor.py`
  1. Executes required folder generation based on `monitor.cfg`.
  2. Default folders created: (these will change if you modify the config file - be warned!)
     - `send_data_archive`
     - `send`
     - `archive`
     - `monitor`
  3. drop an jpg,img or gif in the `mointor` folder and watch the magic.

  #### Process Flow
  1. With `monitor.py` running, drop image files (PNG, JPG, GIF) into the `monitor` folder.
  2. Images are converted to WLED format and sent to your device:
     - Frames generated to `send` folder.
     - Data pushed to WLED Device using `push.py`.
     - For GIFs, frames are additionally copied to `gifdata` from the send location each time a gif is dropped into the `monitor` folder.
     - `send` folder is cleared after processing, except if `delete_after_send` is disabled in `monitor.cfg`.  (Why? - you might want to copy the processed frames from `gifdata` and use them separately with push.py for your own custom animation reasons.)
     - png,jpg frame files are never kept, if you want to build a collection for some reasons, and then push them based on your own scripts use, use convert.py to create the frame files and use push.py to send them.

  > **Note:** To retain frame files, consider disabling `delete_after_send` in `monitor.cfg`, or manually convert and save important frames.

  

  

  ## Configuration Files

  ### `monitor.cfg`  
  - `move_to_archive`: Saves processed images in `archive_folder_path` (yes/no).
  - `archive_folder_path`: Storage path for archived images.
  - `monitor_location`: Directory monitored for new images.
  - `send_location`: Location where `.send` files are created.
  - `send_data_archive_location`: Temporary storage for send frames data (gets wiped out on each run).

  ### `convert.cfg`
  - `ipaddress`: IP address of WLED device.
  - `brightness`: Brightness setting for LED display. (Don't set too low or some colours will not appear)
  - `resolution`: Resolution of LED matrix. Format (16x16 or 32x32 and so on)

  ## Scripts Usage
  ### convert.py (generates frame files for WLED)
  Converts an image file to `.send` frame files for WLED.
  - **Syntax**: `python convert.py [path_to_image] [output_folder]`
    - image can be png, jpg or gif
  - **Example**: `python convert.py C:\path\to\image.jpg C:\path\to\customfolder`

  ### push.py (solely sends frame files to WLED)
  Sends `.send` file data to WLED device.
  - **Syntax**:

    - For a folder: `python push.py -folder [path_to_folder]` 
      - this process ALL frame files in a folder, this is useful for gifs, as they have a bunch of frames, this will send them all to WLED, but I suggest using the time delay between frames. 
    - For a specific file: `python push.py -file [path_to_file]` 
      - this is used for sending a single frame file from a jpg or a png
    - With delay: `python push.py -folder [path_to_folder] -time [milliseconds]` 
      - creates a delay between frames.

    - With looping: `python push.py -folder [path_to_folder] -loop [count]`
      (***PS: when using this you must specify a folder and a file***)

  - **Examples**:
    - Sending all `.send` files in a folder: 
      - `python push.py -folder C:\path\`
    - Sending a specific file: 
    - `python push.py -folder C:\path\ -file C:\path\file.send`
    - With a delay (for gifs, frame sets): `python push.py -folder C:\path\ -time 1000`
    - Looping the send process: `python push.py -folder C:\path\to\send_location -loop 3`

  ### monitor.py (is the fully automated script that uses convert and push)
  Automatically monitors a directory for new files to process and send to WLED.

  - **Operation**: Runs continuously, monitoring the specified directory.

  

  ### Building for docker
  docker build -t getpixy .

  ### Running this in docker
  docker run -v "$(pwd)/monitor:/app/monitor" -v "$(pwd)/convert.cfg:/app/convert.cfg" -v "$(pwd)/monitor.cfg:/app/monitor.cfg" getpixy:latest

  if your using docker for windows:

  docker run -v "%cd%\monitor:/app/incoming" -v "%cd%\convert.cfg:/app/convert.cfg" -v "%cd%\monitor.cfg:/app/monitor.cfg" getpixy:latest



