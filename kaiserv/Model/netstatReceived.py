import os

class Netstat:
    def __init__(self, pipe_name):
        self.pipe_name = pipe_name

    def read_from_pipe(self):
        print(f"Listening for data on {self.pipe_name}...")
        with open(self.pipe_name, 'r') as pipe:
            while True:
                data = pipe.readline().strip()
                if data:
                    print(f"Data received: {data}")
                    # Here you can add the data to the buffer or process it as needed

# Utilisation
if not os.path.exists("/tmp/netstat_pipe_received"):
    os.mkfifo("/tmp/netstat_pipe_received")

netstat = Netstat("/tmp/netstat_pipe_received")
netstat.read_from_pipe()
