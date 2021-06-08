Robopet Backend

Two main components:
1. HTTP server that triggers actions / behaviors (friendly, hostile, follow object, sleep). This server works by getting the appropriate request, and calling a function that implements it via a child process. When a new request arrives, the server terminates the running process, by sending SIGTERM.
2. Movement control - a script to be executed via SSH shell. This script reads angles from the standard input and directs the robot through serial connection.
