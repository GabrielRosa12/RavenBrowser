import subprocess
import os
import platform 

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)

def buscar_firefox():
    sistema = platform.system()
    
    if sistema == "Windows":
        prog_files = os.environ.get("ProgramFiles", "C:/Program Files")
        return os.path.join(prog_files, "Mozilla Firefox", "firefox.exe")
    
    elif sistema == "Linux":
        return "firefox" 
    
    return "firefox"

FIREFOX_PATH = buscar_firefox()

def abrir_perfil(nome):
    path = os.path.join(BASE_DIR, "profiles", nome)
    
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

    print(f"Sistema: {platform.system()} | Perfil: {nome}")

    subprocess.Popen([
        FIREFOX_PATH,
        "--no-remote",
        "--profile",
        path
    ])

print("1-Normal")
print("2-VPN")
print("3-TOR")

opcao = input("Escolha: ")

if opcao == "1":
    abrir_perfil("normal")
elif opcao == "2":
    abrir_perfil("vpn")
elif opcao == "3":
    abrir_perfil("tor")
else:
    print("Opção inválida")