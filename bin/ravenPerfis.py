import subprocess
import os
import platform
import tkinter as tk

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)

HTML_PATH = os.path.join(BASE_DIR, "desktop", "raven.html")

def buscar_firefox():
    sistema = platform.system()
    if sistema == "Windows":
        prog_files = os.environ.get("ProgramFiles", "C:/Program Files")
        return os.path.join(prog_files, "Mozilla Firefox", "firefox.exe")
    return "firefox"

FIREFOX_PATH = buscar_firefox()

def formatar_path_html(path):
    path = os.path.abspath(path)
    if platform.system() == "Windows":
        path = path.replace("\\", "/")
        return f"file:///{path}"
    return f"file://{path}"

def configurar_perfil(path_perfil, html_uri):
    user_js = os.path.join(path_perfil, "user.js")
    prefs = {
        "browser.startup.homepage": html_uri,
        "browser.startup.page": 1,
        "browser.newtabpage.enabled": False,
        "browser.newtab.url": html_uri,
        "toolkit.legacyUserProfileCustomizations.stylesheets": True,
        "dom.allow_scripts_to_close_windows": True,
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
        f.write("\n// === Raven Browser ===\n")
        for chave, valor in prefs.items():
            if isinstance(valor, bool):
                v = "true" if valor else "false"
            elif isinstance(valor, int):
                v = str(valor)
            else:
                v = f'"{valor}"'
            f.write(f'user_pref("{chave}", {v});\n')
    print(f"[+] user.js criado em: {user_js}")

   
    chrome_dir = os.path.join(path_perfil, "chrome")
    os.makedirs(chrome_dir, exist_ok=True)

    user_chrome = os.path.join(chrome_dir, "userChrome.css")
    with open(user_chrome, "w", encoding="utf-8") as f:
        f.write("/* Raven Browser — oculta interface nativa do Firefox */\n")
        f.write("#nav-bar          { display: none !important; }\n")
        f.write("#TabsToolbar      { display: none !important; }\n")
        f.write("#toolbar-menubar  { display: none !important; }\n")
        f.write("#PersonalToolbar  { display: none !important; }\n")
    print(f"[+] userChrome.css criado em: {user_chrome}")

def abrir_perfil(nome):
    path = os.path.join(BASE_DIR, "profiles", nome)
    os.makedirs(path, exist_ok=True)

    html_uri = formatar_path_html(HTML_PATH)
    configurar_perfil(path, html_uri)

    print(f"[*] Sistema : {platform.system()}")
    print(f"[*] Perfil  : {nome}")
    print(f"[*] URL     : {html_uri}")

    subprocess.Popen([FIREFOX_PATH, "--no-remote", "--profile", path, html_uri])

def escolher_perfil():
    escolha = {"perfil": None}

    root = tk.Tk()
    root.title("Raven Browser")
    root.geometry("280x360")
    root.resizable(False, False)
    root.configure(bg="#0f0f1a")

    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - 140
    y = (root.winfo_screenheight() // 2) - 180
    root.geometry(f"560x560+{x}+{y}")

    try:
        root.iconphoto(True, tk.PhotoImage(file=os.path.join(BASE_DIR, "branding", "icon.png")))
    except:
        pass

    try:
        img = tk.PhotoImage(file=os.path.join(BASE_DIR, "branding", "icon.png"))
        img = img.subsample(2, 2)
        icon_label = tk.Label(root, image=img, bg="#0f0f1a")
        icon_label.image = img
        icon_label.pack(pady=(28, 8))
    except:
        tk.Label(root, text="◈", font=("Segoe UI", 28), bg="#0f0f1a", fg="#7B2FBE").pack(pady=(28, 8))

    tk.Label(root, text="Raven Browser", font=("Segoe UI", 14, "bold"),
             bg="#0f0f1a", fg="#e8e0f0").pack()
    tk.Label(root, text="Escolha o perfil", font=("Segoe UI", 10),
             bg="#0f0f1a", fg="#5a4a72").pack(pady=(2, 20))

    for nome, label in [("normal", "Normal"), ("vpn", "VPN"), ("tor", "TOR")]:
        def abrir(n=nome):
            escolha["perfil"] = n
            root.destroy()

        btn = tk.Button(
            root, text=f"  ●  {label}",
            font=("Segoe UI", 11),
            bg="#1a1028", fg="#c8b8e8",
            activebackground="#2a1a3a", activeforeground="#e8e0f0",
            relief="flat", bd=0, cursor="hand2",
            width=22, height=2,
            anchor="w", padx=16,
            command=abrir
        )
        btn.pack(pady=4)
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#2a1a3a"))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#1a1028"))

    tk.Label(root, text="raven • v1.0", font=("Segoe UI", 9),
             bg="#0f0f1a", fg="#2a1a3a").pack(side="bottom", pady=16)

    root.mainloop()
    return escolha["perfil"]

perfil = escolher_perfil()
if perfil:
    abrir_perfil(perfil)