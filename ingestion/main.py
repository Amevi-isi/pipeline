import subprocess

# Définir les fichiers Bash à exécuter
copie = 'copie.sh'
consumers = 'conso.sh'
producters = 'prod.sh'

# Lancer les deux scripts en parallèle
process1 = subprocess.Popen(['bash', consumers])
process2 = subprocess.Popen(['bash', producters])
process3 = subprocess.Popen(['bash', copie])

print("Les deux scripts sont en cours d'execution.")
# Attendre que les deux processus se terminent
process3.wait()
process1.wait()
process2.wait()

print("Les deux scripts ont été exécutés.")


