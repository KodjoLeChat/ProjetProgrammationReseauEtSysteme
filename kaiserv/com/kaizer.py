import subprocess
import time

# Commande pour exécuter le programme en C (intermitter)
c_program_command = ["./transmitter"]
c_process = subprocess.Popen(c_program_command)

time.sleep(2)

# Commande pour exécuter le script Python (prog.py)
python_program_command = ["python3", "../controleur.py"]
subprocess.run(python_program_command, check=True)

# Afficher un message à la fin
print("Les programmes ont été exécutés avec succès.")
