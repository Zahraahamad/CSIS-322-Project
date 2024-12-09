import socket
import os
import hashlib

def calculate_checksum(file_path):
    """Calculate the checksum of a file using SHA-256."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            sha256.update(chunk)
    return sha256.hexdigest()

def send_file(client, server_address, file_path):
    """Send a single text file to the server."""
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)

    # Send metadata: (file_name, file_size)
    metadata = f"{file_name}|{file_size}"
    client.sendto(metadata.encode(), server_address)

    # Send file data
    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            client.sendto(chunk, server_address)

    print(f"[INFO] File '{file_name}' sent successfully.")

    # Send checksum
    checksum = calculate_checksum(file_path)
    client.sendto(checksum.encode(), server_address)

    # Wait for confirmation
    status, _ = client.recvfrom(1024)
    if status.decode() == "SUCCESS":
        print(f"[INFO] Checksum verified by server. File '{file_name}' is intact.")
    else:
        print(f"[ERROR] Checksum mismatch reported by server for '{file_name}'.")

def receive_file(client, server_address):
    """Receive a single text file from the server."""
    # Receive file metadata: (file_name, file_size)
    metadata, server_address = client.recvfrom(4096)
    file_name, file_size = metadata.decode().split('|')
    file_size = int(file_size)

    print(f"[INFO] Receiving file '{file_name}' of size {file_size} bytes from {server_address}")

    # Receive the file data
    received_size = 0
    with open(file_name, "wb") as f:
        while received_size < file_size:
            data, server_address = client.recvfrom(4096)
            f.write(data)
            received_size += len(data)

    print(f"[INFO] File '{file_name}' received successfully.")

    # Receive checksum from server
    server_checksum, server_address = client.recvfrom(1024)

    # Verify file integrity
    client_checksum = calculate_checksum(file_name)
    if server_checksum.decode() == client_checksum:
        print(f"[INFO] Checksum verified for '{file_name}'. File is intact.")
        client.sendto("SUCCESS".encode(), server_address)
    else:
        print(f"[ERROR] Checksum mismatch for '{file_name}'!")
        client.sendto("FAILURE".encode(), server_address)

def start_client(server_host, server_port, files_to_send=[]):
    """Start the UDP client."""
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Indicate readiness to the server
        client.sendto("READY".encode(), (server_host, server_port))

        # Send files to server
        client.sendto(str(len(files_to_send)).encode(), (server_host, server_port))
        print(f"[INFO] Sending {len(files_to_send)} file(s) to server.")
        for file_path in files_to_send:
            send_file(client, (server_host, server_port), file_path)

        # Receive files back from server
        num_files, _ = client.recvfrom(1024)
        num_files = int(num_files.decode())
        print(f"[INFO] Receiving back {num_files} file(s) from server.")
        for _ in range(num_files):
            receive_file(client, (server_host, server_port))

    except Exception as e:
        print(f"[ERROR] {e}")

    finally:
        client.close()

if __name__ == "__main__":
    # Replace with paths to text files the client should send
    files_to_send = ["client_file1.txt", "client_file2.txt", "client_file3.txt"]
    start_client("127.0.0.1", 5000, files_to_send=files_to_send)
