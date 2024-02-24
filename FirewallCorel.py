# Desenvolvido por Luiz F. R. Pimentel
# https://github.com/KanekiZLF

import tkinter as tk
from tkinter import messagebox
import subprocess
import pyuac
import os
import sys

# Caminhos dos programas fixos
FontManager = r"C:\Program Files\Corel\CorelDRAW Graphics Suite 2022\Programs64\FontManager.exe"
CorelDRW = r"C:\Program Files\Corel\CorelDRAW Graphics Suite 2022\Programs64\CorelDWR.exe"
CorelPP = r"C:\Program Files\Corel\CorelDRAW Graphics Suite 2022\Programs64\CorelPP.exe"
Capture = r"C:\Program Files\Corel\CorelDRAW Graphics Suite 2022\Programs64\Capture.exe"
CdrConv = r"C:\Program Files\Corel\CorelDRAW Graphics Suite 2022\Programs64\CdrConv.exe"
Cap = r"C:\Program Files\Corel\CorelDRAW Graphics Suite 2022\Programs64\Cap.exe"

def center_window(window):
    window.update_idletasks()
    x_offset = (window.winfo_screenwidth() - window.winfo_reqwidth()) // 2
    y_offset = (window.winfo_screenheight() - window.winfo_reqheight()) // 2
    window.geometry('+{}+{}'.format(x_offset, y_offset))

def rule_exists(rule_name):
    # Comando para verificar a existência da regra
    comando = [
        "netsh",
        "advfirewall",
        "firewall",
        "show",
        "rule",
        "name=" + rule_name
    ]

    # Executa o comando e captura a saída
    try:
        output = subprocess.check_output(comando, universal_newlines=True)
        # Verifica se a regra existe na saída
        if rule_name in output:
            return True
        else:
            return False
    except subprocess.CalledProcessError:
        # Se ocorrer um erro ao executar o comando, a regra não existe
        return False

def program_exist(program_name):
    folder_path = r"C:\Program Files\Corel\CorelDRAW Graphics Suite 2022\Programs64"
    
    # Verifica se a pasta existe
    if not os.path.isdir(folder_path):
        print("O caminho especificado não é uma pasta válida.")
        messagebox.showerror("Erro", f"O caminho especificado não é uma pasta válida.")
        return False

    # Lista todos os arquivos na pasta
    files = os.listdir(folder_path)

    # Verifica se o programa está na lista de arquivos
    if program_name in files:
        return True
    else:
        return False

def bloquear_programas():

    # Verifica se a regra existe antes de bloquear os programas
    if rule_exists("BlockFontManager") and rule_exists("BlockCorelDRW") and rule_exists("BlockCorelPP") \
            and rule_exists("BlockCapture") and rule_exists("BlockCdrConv") and rule_exists("BlockCap"):
        messagebox.showinfo("Info", "As regras já existem no firewall.")
    else:
        comando_corelfnt = [
        "netsh",
        "advfirewall",
        "firewall",
        "add",
        "rule",
        "name=BlockFontManager",
        "dir=out",
        "action=block",
        f"program={FontManager}",
        "enable=yes"
    ]

        comando_coreldrw = [
            "netsh",
            "advfirewall",
            "firewall",
            "add",
            "rule",
            "name=BlockCorelDRW",
            "dir=out",
            "action=block",
            f"program={CorelDRW}",
            "enable=yes"
        ]

        comando_corelpp = [
            "netsh",
            "advfirewall",
            "firewall",
            "add",
            "rule",
            "name=BlockCorelPP",
            "dir=out",
            "action=block",
            f"program={CorelPP}",
            "enable=yes"
        ]

        comando_corelcapture = [
            "netsh",
            "advfirewall",
            "firewall",
            "add",
            "rule",
            "name=BlockCapture",
            "dir=out",
            "action=block",
            f"program={Capture}",
            "enable=yes"
        ]

        comando_corelcdrconv = [
            "netsh",
            "advfirewall",
            "firewall",
            "add",
            "rule",
            "name=BlockCdrConv",
            "dir=out",
            "action=block",
            f"program={CdrConv}",
            "enable=yes"
        ]

        comando_corelcap = [
            "netsh",
            "advfirewall",
            "firewall",
            "add",
            "rule",
            "name=BlockCap",
            "dir=out",
            "action=block",
            f"program={Cap}",
            "enable=yes"
        ]
        try:
            subprocess.run(comando_corelfnt, check=True)
            subprocess.run(comando_coreldrw, check=True)
            subprocess.run(comando_corelpp, check=True)
            subprocess.run(comando_corelcapture, check=True)
            subprocess.run(comando_corelcdrconv, check=True)
            subprocess.run(comando_corelcap, check=True)
            messagebox.showinfo("Sucesso", "Acesso à rede para os programas CorelDRAW foi bloqueado com sucesso!")
            sys.exit()
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Erro", f"Erro ao bloquear acesso à rede para os programas CorelDRAW: {e}")

# Criar a janela principal
root = tk.Tk()
root.title("FirewallCorel")

# Definir o tamanho da janela
largura_janela = 160
altura_janela = 132
root.geometry(f"{largura_janela}x{altura_janela}")


root.resizable(False,False)

# Criar e posicionar os widgets
tk.Label(root, text="FontManager:").place(x=10, y=0)
tk.Label(root, text="CorelDRW:").place(x=10, y=15)
tk.Label(root, text="CorelPP:").place(x=10, y=30)
tk.Label(root, text="Capture:").place(x=10, y=45)
tk.Label(root, text="CdrConv:").place(x=10, y=62)
tk.Label(root, text="Cap:").place(x=10, y=77)


if program_exist("FontManager.exe"):
    tk.Label(root, text="✔️").place(x=90, y=0)
else:
    tk.Label(root, text="❌").place(x=90, y=0)

if program_exist("CorelDRW.exe"):
    tk.Label(root, text="✔️").place(x=72, y=15)
else:
    tk.Label(root, text="❌").place(x=72, y=15)

if program_exist("CorelPP.exe"):
    tk.Label(root, text="✔️").place(x=60, y=30)
else:
    tk.Label(root, text="❌").place(x=60, y=30)

if program_exist("Capture.exe"):
    tk.Label(root, text="✔️").place(x=60, y=45)
else:
    tk.Label(root, text="❌").place(x=60, y=45)


if program_exist("CdrConv.exe"):
    tk.Label(root, text="✔️").place(x=65, y=62)
else:
    tk.Label(root, text="❌").place(x=65, y=62)


if program_exist("Cap.exe"):
    tk.Label(root, text="✔️").place(x=40, y=77)
else:
    tk.Label(root, text="❌").place(x=40, y=77)




bloquear_button = tk.Button(root, text="Block", command=bloquear_programas)
bloquear_button.place(x=55, y=100)

# Rodar o loop principal


def main():
    root.mainloop()

if __name__ == "__main__":
    # Solicitar privilégios de administrador
    if not pyuac.isUserAdmin():
        pyuac.runAsAdmin()
    else:
        center_window(root)
        main()