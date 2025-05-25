# rtp_server.py

import socket, threading, struct, cv2, os, time

# ─── Settings ────────────────────────────────────────────────
VIDEO_PATH = r"C:\Users\PC\Documents\ADVANCED\Advanced Proj\RTPServer\Running_Video.mp4"
CONTROL_PORT = 8554   # TCP for RTSP commands, used in SETUP, PLAY, PAUSE, TEARDOWN
VIDEO_PORT   = 5004   # UDP for video packets, used in RTP streaming
FRAME_SIZE   = (320, 240) # Resize frames to this size because of bandwidth constraints
JPEG_QUALITY = 50 # JPEG compression quality (0-100), lower means more compression
FPS          = 25 # Frames per second for the video stream

# ─── Check file exists ───────────────────────────────────────
if not os.path.exists(VIDEO_PATH):
    raise FileNotFoundError(f"Video not found → {VIDEO_PATH}")

# ─── Global control state ────────────────────────────────────
# intially set to false because we don't want to stream until the client sends PLAY command

state = {
    "play": False,
    "exit": False,
    "client_addr": None
} 

# ─── UDP Sender Thread ───────────────────────────────────────
# This thread will handle sending RTP packets over UDP
def udp_streamer():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Create a UDP socket
    cap = cv2.VideoCapture(VIDEO_PATH) # Open the video file
    seq = 0 # Sequence number for RTP packets
    ssrc = 12345678 # Random SSRC value, can be any unique identifier

    print("📡 RTP Server ready — waiting for client to press PLAY...")

    while not state["exit"]:
        if not state["play"]:
            time.sleep(0.1) # Wait until PLAY command is received, enter
            continue

        ret, frame = cap.read()
        if not ret:
            print("✅ End of video. Exiting.") # If video ends, exit the loop
            break

        frame = cv2.resize(frame, FRAME_SIZE)
        ok, enc = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY])
        if not ok:
            print("⚠️ JPEG encode failed.") # If encoding fails, skip this frame
            continue

        payload = enc.tobytes() # Convert encoded frame to bytes
        timestamp = int(time.time() * 1000) & 0xFFFFFFFF # Use current time as timestamp, wrap to 32 bits
        # RTP header: version 2, payload type 26 (JPEG), sequence number, timestamp, SSRC
        rtp_hdr = struct.pack("!BBHII", 0x80, 26, seq & 0xFFFF, timestamp, ssrc)
       
        packet = rtp_hdr + payload # Combine RTP header and payload

        if state["client_addr"]:
            sock.sendto(packet, state["client_addr"])
            print(f"📤 Sent frame {seq:05} → {len(packet):>5} bytes")
        seq += 1
        time.sleep(1 / FPS)

    cap.release() # Release the video capture object
    sock.close() # Close the UDP socketS

# ─── TCP RTSP-like Command Listener ──────────────────────────
def tcp_command_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", CONTROL_PORT)) 
    server.listen(1) # Listen for incoming connections
    print(f"📞 Listening for RTSP commands on TCP {CONTROL_PORT}...")

    conn, addr = server.accept()
    print(f"✅ Client connected from {addr}")
    conn.sendall(b"RTSP/1.0 200 OK\nWelcome\n")

    while not state["exit"]:
        try:
            data = conn.recv(1024).decode().strip()
            if not data:
                continue
            print(f"🧾 Received command: {data}")

            if data.startswith("SETUP"):
                state["client_addr"] = (addr[0], VIDEO_PORT)
                conn.sendall(b"RTSP/1.0 200 OK\nSETUP Done\n")
                # Send back the client address for RTP streaming
            elif data.startswith("PLAY"):
                state["play"] = True
                conn.sendall(b"RTSP/1.0 200 OK\nStreaming started\n")
                # Notify the UDP streamer to start sending packets
            elif data.startswith("PAUSE"):
                state["play"] = False
                conn.sendall(b"RTSP/1.0 200 OK\nStreaming paused\n")
                # Notify the UDP streamer to pause sending packets
            elif data.startswith("TEARDOWN"):
                state["exit"] = True
                conn.sendall(b"RTSP/1.0 200 OK\nTeardown\n")
                break
            
            else:
                conn.sendall(b"RTSP/1.0 400 BAD REQUEST\nUnknown command\n")
                # Handle unknown commands gracefully
        except Exception as e:
            print(f"❌ Client connection error: {e}")
            break

    conn.close()
    server.close()
    print("🛑 Server shutting down.") # Close the server socket and exit

# ─── Main ────────────────────────────────────────────────────
if __name__ == "__main__":
    t1 = threading.Thread(target=tcp_command_server)
    t2 = threading.Thread(target=udp_streamer)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
