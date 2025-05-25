# rtp_server.py

import socket, threading, struct, cv2, os, time

# ─── Settings ────────────────────────────────────────────────
VIDEO_PATH = r"C:\Users\PC\Documents\ADVANCED\Advanced Proj\RTPServer\Running_Video.mp4"
CONTROL_PORT = 8554   # TCP for RTSP commands
VIDEO_PORT   = 5004   # UDP for video packets
FRAME_SIZE   = (320, 240)
JPEG_QUALITY = 50
FPS          = 25

# ─── Check file exists ───────────────────────────────────────
if not os.path.exists(VIDEO_PATH):
    raise FileNotFoundError(f"Video not found → {VIDEO_PATH}")

# ─── Global control state ────────────────────────────────────
state = {
    "play": False,
    "exit": False,
    "client_addr": None
}

# ─── UDP Sender Thread ───────────────────────────────────────
def udp_streamer():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cap = cv2.VideoCapture(VIDEO_PATH)
    seq = 0
    ssrc = 12345678

    print("📡 RTP Server ready — waiting for client to press PLAY...")

    while not state["exit"]:
        if not state["play"]:
            time.sleep(0.1)
            continue

        ret, frame = cap.read()
        if not ret:
            print("✅ End of video. Exiting.")
            break

        frame = cv2.resize(frame, FRAME_SIZE)
        ok, enc = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY])
        if not ok:
            print("⚠️ JPEG encode failed.")
            continue

        payload = enc.tobytes()
        timestamp = int(time.time() * 1000) & 0xFFFFFFFF
        rtp_hdr = struct.pack("!BBHII", 0x80, 26, seq & 0xFFFF, timestamp, ssrc)
        packet = rtp_hdr + payload

        if state["client_addr"]:
            sock.sendto(packet, state["client_addr"])
            print(f"📤 Sent frame {seq:05} → {len(packet):>5} bytes")
        seq += 1
        time.sleep(1 / FPS)

    cap.release()
    sock.close()

# ─── TCP RTSP-like Command Listener ──────────────────────────
def tcp_command_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", CONTROL_PORT))
    server.listen(1)
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

            elif data.startswith("PLAY"):
                state["play"] = True
                conn.sendall(b"RTSP/1.0 200 OK\nStreaming started\n")

            elif data.startswith("PAUSE"):
                state["play"] = False
                conn.sendall(b"RTSP/1.0 200 OK\nStreaming paused\n")

            elif data.startswith("TEARDOWN"):
                state["exit"] = True
                conn.sendall(b"RTSP/1.0 200 OK\nTeardown\n")
                break

            else:
                conn.sendall(b"RTSP/1.0 400 BAD REQUEST\nUnknown command\n")

        except Exception as e:
            print(f"❌ Client connection error: {e}")
            break

    conn.close()
    server.close()
    print("🛑 Server shutting down.")

# ─── Main ────────────────────────────────────────────────────
if __name__ == "__main__":
    t1 = threading.Thread(target=tcp_command_server)
    t2 = threading.Thread(target=udp_streamer)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
