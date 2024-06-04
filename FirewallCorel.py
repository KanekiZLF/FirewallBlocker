# Desenvolvido por Luiz F. R. Pimentel
# https://github.com/KanekiZLF

import tkinter as tk
from tkinter import messagebox, filedialog
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
lanel = ""
folderPath = ""
errorMsg = False
folderFound = False

def centerWindow(window):
    window.update_idletasks()
    x_offset = (window.winfo_screenwidth() - window.winfo_reqwidth()) // 2
    y_offset = (window.winfo_screenheight() - window.winfo_reqheight()) // 2
    window.geometry('+{}+{}'.format(x_offset, y_offset))

def ruleExists(ruleName):
    # Comando para verificar a existência da regra
    comando = [
        "netsh",
        "advfirewall",
        "firewall",
        "show",
        "rule",
        "name=" + ruleName
    ]

    # Executa o comando e captura a saída
    try:
        output = subprocess.check_output(comando, universal_newlines=True)
        # Verifica se a regra existe na saída
        if ruleName in output:
            return True
        else:
            return False
    except subprocess.CalledProcessError:
        # Se ocorrer um erro ao executar o comando, a regra não existe
        return False

def programExist(program_name):
    global folderPath
    
    # Verifica se a pasta existe
    if not os.path.isdir(folderPath):
        print("O caminho especificado não é uma pasta válida.")
        messagebox.showerror("Erro", f"O caminho especificado não é uma pasta válida.")
        return False

    # Lista todos os arquivos na pasta
    files = os.listdir(folderPath)

    # Verifica se o programa está na lista de arquivos
    if program_name in files:
        return True
    else:
        return False

def blockProgram():
    global folderFound

    if folderFound:
        # Verifica se a regra existe antes de bloquear os programas
        if ruleExists("BlockFontManager") and ruleExists("BlockCorelDRW") and ruleExists("BlockCorelPP") \
                and ruleExists("BlockCapture") and ruleExists("BlockCdrConv") and ruleExists("BlockCap"):
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
    else:
        messagebox.showerror("Pasta invalida", f"Selecione a pasta onde fica os executaveis do corel !")

# Criar a janela principal
root = tk.Tk()
root.title("FirewallCorel")

# Criação do campo de entrada para exibir o caminho do arquivo
corelPath = tk.Entry(root, width=19)
corelPath.place(x= 10, y= 105)

# Criação do botão para abrir o diálogo de seleção de arquivos
corelFiles = tk.Button(root, text="...", command=lambda: browseFiles())
corelFiles.place(x= 132, y= 102)


# Definir o tamanho da janela
withWindow = 160
hightWindow = 160
root.geometry(f"{withWindow}x{hightWindow}")
root.title("CorelBlock by Kaneki")

root.resizable(False,False)

# Criar e posicionar os widgets
tk.Label(root, text="FontManager:").place(x=10, y=0)
tk.Label(root, text="CorelDRW:").place(x=10, y=15)
tk.Label(root, text="CorelPP:").place(x=10, y=30)
tk.Label(root, text="Capture:").place(x=10, y=45)
tk.Label(root, text="CdrConv:").place(x=10, y=62)
tk.Label(root, text="Cap:").place(x=10, y=77)

# Função para abrir o diálogo de seleção de arquivos
def browseFiles():
    global folderPath
    global errorMsg
    errorMsg = False
    filename = filedialog.askdirectory(initialdir="C:/", title="Selecione pasta do corel")
    if filename:
        corelPath.delete(0, tk.END)
        corelPath.insert(0, filename)
        folderPath = filename
        if folderPath:
                for program, x, y in programsPositions:
                    checkProgram(program, x, y)
        return filename
    return None

def checkProgram(programName, x, y):
    global errorMsg
    global folderFound
    if programExist(programName):
        tk.Label(root, text="✔️").place(x=x, y=y)
        folderFound = True
    else:
        tk.Label(root, text="❌").place(x=x, y=y)
        if not errorMsg:
            messagebox.showerror("Erro", f"O caminho especificado não é uma pasta válida.")
            errorMsg = True
            folderFound = False

# Definindo a lista de programas e suas posições
programsPositions = [
    ("FontManager.exe", 90, 0),
    ("CorelDRW.exe", 72, 15),
    ("CorelPP.exe", 60, 30),
    ("Capture.exe", 60, 45),
    ("CdrConv.exe", 65, 62),
    ("Cap.exe", 40, 77)
]

def aboutKaneki ():
    messagebox.showinfo("Desenvolvido por Kaneki", f"Este programa tem como função lhe ajudar a bloquear conexão de rede do programa Corel Draw !!.")
    return
blockButton = tk.Button(root, text="Block", command=blockProgram)
blockButton.place(x=55, y=128)

aboutButton = tk.Button(root, text="?", font=("Arial", 7), command=aboutKaneki)
aboutButton.place(x=134, y=132)

# Rodar o loop principal

def main():
     # Coloca a janela no topo
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)  # Voltar ao estado normal depois de ser mostrada
    centerWindow(root)
    root.mainloop()

if __name__ == "__main__":
    # Solicitar privilégios de administrador
    if not pyuac.isUserAdmin():
        pyuac.runAsAdmin()
    else:
        centerWindow(root)
        main()