# CS158A Assignment 1

Python Version - 3.13.3

---

# How to Run

## Replace the IP address with your IP address.

![image](https://github.com/user-attachments/assets/abd532a7-5421-4bf6-bb1e-334db9a319a4)

## Start the Server

In **Terminal 1**, run:

python3 myvlserver.py

In **Terminal 2**, run:

python3 myvlclient.py

## Input Format

- The input sentence must start with a **2-digit length prefix**, followed by a message.
- The prefix indicates how many characters follow it.
- Example:  
  `10helloworld` → 10-character message `"helloworld"`

- Valid inputs: `01a`, `10helloworld`, `99<99-characters-message>`
- Total length must be between 3 and 101 characters.

## Example

### Input
![Screenshot 2025-06-16 232101](https://github.com/user-attachments/assets/6e46f29a-117d-4ac5-8c93-3f7ba087e909)

### Output
![Screenshot 2025-06-16 232049](https://github.com/user-attachments/assets/004fff84-215d-4c8b-8b52-c1e32a05f62d)

