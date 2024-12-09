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

def receive_file(server, client_address):
    """Receive a single text file from the client."""
    # Receive file metadata: (file_name, file_size)
    metadata, client_address = server.recvfrom(4096)
    file_name, file_size = metadata.decode().split('|')
    file_size = int(file_size)

    print(f"[INFO] Receiving file '{file_name}' of size {file_size} bytes from {client_address}")

    # Receive the file data
    received_size = 0
    with open(file_name, "wb") as f:
        while received_size < file_size:
            data, client_address = server.recvfrom(4096)
            f.write(data)
            received_size += len(data)

    print(f"[INFO] File '{file_name}' received successfully.")

    # Receive checksum from client
    client_checksum, client_address = server.recvfrom(1024)

    # Verify file integrity
    server_checksum = calculate_checksum(file_name)
    if client_checksum.decode() == server_checksum:
        print(f"[INFO] Checksum verified for '{file_name}'. File is intact.")
        server.sendto("SUCCESS".encode(), client_address)
    else:
        print(f"[ERROR] Checksum mismatch for '{file_name}'!")
        server.sendto("FAILURE".encode(), client_address)

    return file_name

def send_file(server, client_address, file_path):
    """Send a single text file to the client."""
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)

    # Send metadata: (file_name, file_size)
    metadata = f"{file_name}|{file_size}"
    server.sendto(metadata.encode(), client_address)

    # Send file data
    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            server.sendto(chunk, client_address)

    print(f"[INFO] File '{file_name}' sent successfully.")

    # Send checksum
    checksum = calculate_checksum(file_path)
    server.sendto(checksum.encode(), client_address)

    # Wait for confirmation
    status, _ = server.recvfrom(1024)
    if status.decode() == "SUCCESS":
        print(f"[INFO] Checksum verified by client. File '{file_name}' is intact.")
    else:
        print(f"[ERROR] Checksum mismatch reported by client for '{file_name}'.")

def start_server(host="0.0.0.0", port=5000):
    """Start the UDP server."""
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((host, port))
    print(f"[INFO] UDP server listening on {host}:{port}")

    while True:
        try:
            print("[INFO] Waiting for a client to connect...")
            message, client_address = server.recvfrom(1024)
            if message.decode() == "READY":
                print(f"[INFO] Client {client_address} is ready.")

                # Receive files from client
                num_files, client_address = server.recvfrom(1024)
                num_files = int(num_files.decode())
                print(f"[INFO] Receiving {num_files} file(s) from client.")
                received_files = []
                for _ in range(num_files):
                    file_name = receive_file(server, client_address)
                    received_files.append(file_name)

                # Send files back to the client
                print(f"[INFO] Sending back {len(received_files)} file(s) to client.")
                server.sendto(str(len(received_files)).encode(), client_address)
                for file_path in received_files:
                    send_file(server, client_address, file_path)

        except Exception as e:
            print(f"[ERROR] {e}")

if __name__ == "__main__":
    start_server(port=5000)
