import os

class Netstat:
    def __init__(self, pipe_name):
        self.buffer = []
        self.pipe_name = pipe_name
        # Créer un tube nommé s'il n'existe pas déjà
        if not os.path.exists(pipe_name):
            os.mkfifo(pipe_name)

    def add_to_buffer(self, data):
        self.buffer.append(data)

    def write_to_pipe(self):
        with open(self.pipe_name, 'w') as pipe:
            for item in self.buffer:
                pipe.write(f"{item}\n")

# Utilisation
netstat = Netstat("/tmp/netstat_pipe")
netstat.add_to_buffer("data1")
netstat.add_to_buffer("data2")
netstat.write_to_pipe()

