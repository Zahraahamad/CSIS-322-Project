# File Transfer System Using TCP and UDP

## Description
This project implements a file transfer system to send and receive files between a client and a server using both **TCP** and **UDP** protocols. The system ensures data integrity through checksum verification, making it an excellent demonstration of network communication concepts.

---

## Features
- **TCP Protocol**: Reliable, connection-oriented file transfer.
- **UDP Protocol**: Faster, connectionless file transfer.
- **Checksum Verification**: Ensures file integrity during transfer.
- **Bidirectional Transfer**: Files are sent from the client to the server and returned to the client.

---

## Prerequisites
- Python 3.8 or later.
- Basic understanding of terminal/command-line operations.
- Text files to transfer.
---
## Installation

1. **Download the Project Files**
   - Ensure you have downloaded the project files.
   - Extract the files into a directory on your computer if they are in a compressed format.

2. **Ensure Python is Installed**
   - This project requires **Python 3.8 or later**. Verify your Python installation by running the following command in your terminal or command prompt:
     ```bash
     python --version
     ```
   - If Python is not installed, download and install it from [https://www.python.org/](https://www.python.org/).

3. **Navigate to the Project Directory**
   - Open a terminal or command prompt.
   - Navigate to the folder where the project files are located. For example:
     ```bash
     cd path/to/project-folder
     ```

4. **No Additional Dependencies**
   - This project uses Python's standard library and does not require any additional installations.

5. **Run the Project**
   - Proceed to the **How to Use** section for instructions on running the TCP or UDP versions of the file transfer system.
---
## How to Use
### Using the TCP Version

#### Step 1: Start the TCP Server
1. Open a terminal or command prompt.
2. Navigate to the project directory:
   ```bash
   cd path/to/project-folder
3. Start the tcp server
    ```bash
    python tcp_server.py
4. The server will begin listening on 0.0.0.0:9999 and wait for client connections.
#### Step 2: Start the TCP Client
1. Open the terminal
2. Navigate the project directory:
    ```bash
   cd path/to/project-folder
3. Start the tcp client
    ```bash
    python tcp_client.py

### Using the UDP Version
#### Repeat the same steps for the UDP version.
