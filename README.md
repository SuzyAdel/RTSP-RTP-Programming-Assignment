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

Note: The client-side RTP implementation is provided for you

# RTSP Client:

Issues play/pause commands to control video streaming

Note: The server-side RTSP implementation is provided for you

Technical Requirements
The system involves real-time streaming protocol (RTSP) for control and real-time transport protocol (RTP) for actual media delivery

UDP will be used as the transport protocol for RTP packets

Sequence numbers and timestamps are required in RTP headers for proper media synchronization
