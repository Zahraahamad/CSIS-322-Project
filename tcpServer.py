import socket
import threading
import hashlib

def handle_client(client_socket, client_address):
    print(f"[INFO] Connected to {client_address}")

    # Receive the number of files
    num_files = int(client_socket.recv(1024).decode())
    client_socket.send(b"ACK")  # Acknowledge receipt
    print(f"[INFO] Client will send {num_files} files.")

    for file_index in range(num_files):
        # Receive file name
        file_name = client_socket.recv(1024).decode()
        client_socket.send(b"ACK")  # Acknowledge receipt
        print(f"[INFO] Receiving file {file_index + 1}/{num_files}: {file_name}")

        # Receive file size
        file_size = int(client_socket.recv(1024).decode())
        client_socket.send(b"ACK")  # Acknowledge receipt
        print(f"[INFO] File size: {file_size} bytes")

        # Receive file data
        received_data = b''
        while len(received_data) < file_size:
            data = client_socket.recv(1024)
            if not data:
                break
            received_data += data
        client_socket.send(b"ACK")  # Acknowledge receipt of file data

        # Receive file checksum
        received_checksum = client_socket.recv(1024).decode()
        print(f"[INFO] Received checksum for {file_name}: {received_checksum}")

        # Save the file
        with open(file_name, 'wb') as f:
            f.write(received_data)

        # Verify file integrity
        calculated_checksum = hashlib.md5(received_data).hexdigest()
        if calculated_checksum == received_checksum:
            print(f"[INFO] File {file_name} received successfully with integrity.")
        else:
            print(f"[ERROR] File {file_name} integrity check failed.")

        # Send the file back to the client
        print(f"[INFO] Sending back file: {file_name}")
        client_socket.send(file_name.encode())  # Send back file name
        client_socket.recv(1024)  # Wait for acknowledgment
        client_socket.send(str(file_size).encode())  # Send back file size
        client_socket.recv(1024)  # Wait for acknowledgment
        client_socket.sendall(received_data)  # Send back file data
        client_socket.recv(1024)  # Wait for acknowledgment
        client_socket.send(calculated_checksum.encode())  # Send back checksum

    print(f"[INFO] All {num_files} files processed and sent back. Connection with {client_address} closed.")
    client_socket.close()

def start_server(server_ip, server_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_ip, server_port))
    server.listen(5)
    print(f"[INFO] Server listening on {server_ip}:{server_port}")

    while True:
        client_socket, client_address = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    start_server("0.0.0.0", 9999)
