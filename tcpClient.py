import socket
import hashlib
import os

def send_files(server_ip, server_port, file_paths):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))

    # Send the number of files
    client.send(str(len(file_paths)).encode())
    client.recv(1024)  # Wait for acknowledgment

    for file_path in file_paths:
        # File name and size
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)

        # Read file data and calculate checksum
        with open(file_path, 'rb') as f:
            file_data = f.read()
        file_checksum = hashlib.md5(file_data).hexdigest()

        # Send file name
        client.send(file_name.encode())
        client.recv(1024)  # Wait for acknowledgment

        # Send file size
        client.send(str(file_size).encode())
        client.recv(1024)  # Wait for acknowledgment

        # Send file data
        client.sendall(file_data)
        client.recv(1024)  # Wait for acknowledgment

        # Send checksum
        client.send(file_checksum.encode())

        # Receive the file back from the server
        returned_file_name = client.recv(1024).decode()
        client.send(b"ACK")  # Acknowledge file name
        returned_file_size = int(client.recv(1024).decode())
        client.send(b"ACK")  # Acknowledge file size
        returned_data = b''
        while len(returned_data) < returned_file_size:
            data = client.recv(1024)
            if not data:
                break
            returned_data += data
        client.send(b"ACK")  # Acknowledge file data
        returned_checksum = client.recv(1024).decode()

        # Save the returned file
        returned_file_path = f"returned_{returned_file_name}"
        with open(returned_file_path, 'wb') as f:
            f.write(returned_data)

        # Verify the returned file integrity
        if hashlib.md5(returned_data).hexdigest() == returned_checksum:
            print(f"[INFO] File {returned_file_name} successfully returned with integrity.")
        else:
            print(f"[ERROR] Integrity check failed for file {returned_file_name}.")

    client.close()

if __name__ == "__main__":
    files_to_send = [
        "client_file1.txt",
        "client_file2.txt",
        "client_file3.txt"
    ]
    send_files("127.0.0.1", 9999, files_to_send)
