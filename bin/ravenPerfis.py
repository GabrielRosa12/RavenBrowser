import subprocess
import os
import platform 


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)


HTML_PATH = os.path.join(BASE_DIR, "desktop", "teste.html")  

def buscar_firefox():
    sistema = platform.system()
    if sistema == "Windows":
        prog_files = os.environ.get("ProgramFiles", "C:/Program Files")
        return os.path.join(prog_files, "Mozilla Firefox", "firefox.exe")
    elif sistema == "Linux":
        return "firefox" 
    
    return "firefox"

FIREFOX_PATH = buscar_firefox()

def formatar_path_html(path):
    
    path = os.path.abspath(path)
    if platform.system() == "Windows":
        path = path.replace("\\", "/")
        return f"file:///{path}"
    return f"file://{path}"

def configurar_user_js(path_perfil, html_uri):

    user_js = os.path.join(path_perfil, "user.js")

    prefs = {
        "browser.startup.homepage": html_uri,
        "browser.startup.page": 1,
        "browser.newtabpage.enabled": False,
        "browser.newtab.url": html_uri,
    }

    linhas_existentes = []
    if os.path.exists(user_js):
        with open(user_js, "r", encoding="utf-8") as f:
            linhas_existentes = f.readlines()

    
    chaves = list(prefs.keys())
    linhas_filtradas = [
        l for l in linhas_existentes
        if not any(chave in l for chave in chaves)
    ]

    
    with open(user_js, "w", encoding="utf-8") as f:
        f.writelines(linhas_filtradas)
        f.write("\n// === Página inicial personalizada ===\n")
        for chave, valor in prefs.items():
            if isinstance(valor, bool):
                v = "true" if valor else "false"
            elif isinstance(valor, int):
                v = str(valor)
            else:
                v = f'"{valor}"'
            f.write(f'user_pref("{chave}", {v});\n')

def abrir_perfil(nome):
    path = os.path.join(BASE_DIR, "profiles", nome)
    
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

    print(f"Sistema: {platform.system()} | Perfil: {nome}")
    html_uri = formatar_path_html(HTML_PATH)
    subprocess.Popen([
        FIREFOX_PATH,
        "--no-remote",
        "--profile",
        path,
        html_uri
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