import socket
import struct
import time

MCAST_ADDR = "224.0.0.1"
MCAST_PORT = 8888

def send_multicast(message):
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # Set the time-to-live for messages to reach the multicast group
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, struct.pack('b', 1))

    # Set the destination address
    addr = (MCAST_ADDR, MCAST_PORT)

    try:
        # Send the message to the multicast group
        sock.sendto(message.encode(), addr)
        print(f"Sent: {message}")

    except Exception as e:
        print(f"Error sending message: {e}")

    finally:
        # Close the socket
        sock.close()

if __name__ == "__main__":
    count = 0
    while True:
        message = f"Hello from Python {count}"
        send_multicast(message)
        count += 1
        time.sleep(1)
