# rtsp_client.py

import socket

SERVER_IP   = "127.0.0.1" # Change to your RTSP server IP
CONTROL_PORT = 8554 # Change to your RTSP server control port

def send(cmd, conn):
    conn.sendall(f"{cmd}\n".encode()) # Send command to server
    response = conn.recv(4096).decode() # Receive response from server
    print(f"🧾 Server Response:\n{response}")

if __name__ == "__main__":
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((SERVER_IP, CONTROL_PORT))
        print("✅ Connected to server.")
        print(sock.recv(1024).decode())

        send("SETUP", sock)
        playing = False

        print("\n🎮 Controls:")
        print("  ↵  Press Enter to toggle PLAY/PAUSE")
        print("  E  Press E then Enter to TEARDOWN and exit\n")

        while True:
            user_input = input().strip().lower()

            if user_input == "e":
                send("TEARDOWN", sock)
                break
            elif user_input == "":
                if not playing:
                    send("PLAY", sock)
                else:
                    send("PAUSE", sock)
                playing = not playing
            else:
                print("❓ Unknown input. Use Enter to toggle, 'E' to exit.") # Handle unknown input

        sock.close()

    except Exception as e:
        print(f"❌ Connection failed: {e}")
