import hashlib
files = ["Board.py", "Colours.py", "Connection.py", "Controller.py", "Particle.py", "Player.py", "Point.py", "Rules.py", "Settings.py",
         "Server/Client.py", "Server/BaseServer.py", "Server/GameServer.py", "Server/ServerManager.py", "Server/Tester.py",
         "View/CreditsUI.py", "View/GameUI.py", "View/LobbyUI.py", "View/MenuUI.py","View/RulesUI.py", "View/SettingsUI.py"]
# Location of the file (can be set a different way)
BLOCK_SIZE = 65536  # The size of each read from the file

hash_obj = hashlib.md5(open(files[0], 'rb').read(BLOCK_SIZE))
for filename in files[1:]:
    hash_obj.update(open(filename, 'rb').read(BLOCK_SIZE))
checksum = hash_obj.digest()
print(checksum)
