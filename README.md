# RTSP-RTP-Programming-Assignment
RTSP/RTP Programming Assignment Recap
# Task Overview
You need to build a system with two main components:

# RTP Server:

Takes stored video frames

Encapsulates them into RTP packets (adding headers)

Creates UDP segments

Sends them to a UDP socket

Must include sequence numbers and timestamps

![image](https://github.com/user-attachments/assets/f0cdb547-dec2-4ba9-a4ee-1803096e917e)




# RTSP Client:

Issues play/pause commands to control video streaming

Technical Requirements
The system involves real-time streaming protocol (RTSP) for control and real-time transport protocol (RTP) for actual media delivery

UDP will be used as the transport protocol for RTP packets

Sequence numbers and timestamps are required in RTP headers for proper media synchronization

![image](https://github.com/user-attachments/assets/bb0faa83-3645-4644-9887-1556c16259cd)
