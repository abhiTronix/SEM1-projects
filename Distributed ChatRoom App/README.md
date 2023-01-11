# Distributed ChatRoom App with Image Sharing and Chatbot Support

## Demo Videos:

## Server + Client-1 on Machine-A:
<video src="Demo Videos\Server + Client-1.mp4"></video>

## Client-2 on Machine-B:
<video src="Demo Videos\Client-2.mp4"></video>

## Team Members
- Abhishek Singh Thakur
- Kandanlly Rohan Reddy

## Features Implemented:
- Employed gRPC library APIs to implement group chat with a centralized server.
- Intuitive and User friendly GUI with PysimpleGUI python library.
- Image sharing with Pillow and Numpy Python libraries.
- Register-Login workflow with SQLite database support.
- Trained and Implement rule-based ChatBOT using Tensorflow, TFLearn, NLTK libraries.

## Technologies Used
- Tensorflow
- PysimpleGUI
- TFLearn Python module
- NLTK Python module
- Pillow
- SQLite3

## Installation
- **Program requires following dependencies:**
  - Python >= 3.7
  - Pip 
- **Installing pip dependencies:**
  - The `requirements.txt` file contains all Python libraries that this app depend on, and they can be installed using:
    ```sh
    pip install -r requirements.txt
    ```
- **Training ChatBot:**
  - You need to follow these steps in order to train the Chatbot.
    - You can find data model from `/Bot/content.json` and change the content as you wish.
    -  Execute `train.py` file which is inside `/Bot/` directory to train the model that you have prepared.
    -  Then, You are done!

## Usage:
### LOCAL Machine usage:
```sh
# 1. Start your server app
python3 boot_server.py 

# 2. Starts your client app without login/Registration GUI
python3 boot_client_manual.py --user "Abhishek"

# OR

# Starts your client app with login/Registration GUI
python3 boot_client_login.py
```

### Remote Machine usage:
> Make sure both Server and Client machine are on same network.
```sh
# 1. Start your server app will run on `50052` PORT
# Note down IP address and Port of this machine
python3 boot_server.py --port 50052

# 2. Starts your client app without login/Registration GUI
# Write down IP address(for e.g. 172.168.1.14) and Port(for e.g. 50052) of Server machine here
python3 boot_client_manual.py --user "Abhishek" --ip 172.168.1.14 --port 50052

# OR

# Starts your client app with login/Registration GUI
# Write down IP address(for e.g. 172.168.1.14) and Port(for e.g. 50052) of Server machine here
python3 boot_client_login.py --user "Abhishek" --ip 172.168.1.14 --port 50052
```

## References
- Image Sharing: https://github.com/ArnoldYSYeung/grpc-image-service
- Chat Bot: https://github.com/nimeshabuddhika/Tensorflow-Chatbot