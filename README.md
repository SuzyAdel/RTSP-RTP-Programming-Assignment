

# RTSP-RTP Programming Assignment

## Project Overview

This repository presents a comprehensive implementation of a real-time video streaming system based on **RTSP (Real-Time Streaming Protocol)** for control signaling and **RTP (Real-Time Transport Protocol)** for media delivery over UDP. The project focuses on building two core components:

---

## Components

### 1. RTP Server

* **Function:** Reads stored video frames, encapsulates them into RTP packets by adding appropriate headers, and sends them via UDP.
* **Key Features:**

  * RTP header includes sequence numbers and timestamps for synchronization.
  * Constructs UDP segments to ensure real-time delivery.
  * Sends RTP packets continuously to client socket.

### 2. RTSP Client

* **Function:** Acts as a control interface to send commands (e.g., play, pause) to the RTP server for managing video streaming.
* **Key Features:**

  * Implements RTSP protocol for session control.
  * Handles play/pause commands to start or stop the media stream effectively.

---

## Technical Highlights

* **Protocols Used:**

  * RTSP for control commands.
  * RTP for streaming media encapsulation and delivery.
  * UDP for transport layer, chosen for its low latency and suitability for real-time streaming.

* **RTP Packet Details:**

  * Includes **sequence numbers** to detect lost packets and maintain order.
  * Uses **timestamps** for synchronization of video frames.

---

## Architecture Diagram

![RTSP/RTP System Diagram](https://github.com/user-attachments/assets/f0cdb547-dec2-4ba9-a4ee-1803096e917e)

---

## Workflow Summary

| Step | Component   | Action                                                 |
| ---- | ----------- | ------------------------------------------------------ |
| 1    | RTSP Client | Issues **play** or **pause** commands                  |
| 2    | RTP Server  | Processes stored frames, encapsulates into RTP packets |
| 3    | RTP Server  | Sends UDP segments to client                           |
| 4    | RTSP Client | Receives media stream and handles control              |

---

## Future Enhancements

* Implement adaptive bitrate streaming for network variability.
* Add RTCP (RTP Control Protocol) support for better quality feedback.
* Integrate GUI client for enhanced user experience.

---

## How to Run

1. Start the RTP server:

   ```bash
   python rtp_server.py
   ```

2. Launch the RTSP client and control the streaming:

   ```bash
   python rtsp_client.py
   ```

---

## Contact & Contribution

Feel free to open issues or submit pull requests to improve functionality or documentation.

