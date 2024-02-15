# Desenvolvido por Luiz F. R. Pimentel
# https://github.com/KanekiZLF

import subprocess
import sys
import pyuac
import tkinter as tk
import os
from tkinter import messagebox, filedialog

def about_me():
    messagebox.showinfo("By KanekiZLF", "Desenvolvido por Luiz F. R. Pimentel.")

def center_window(window):
    window.update_idletasks()
    x_offset = (window.winfo_screenwidth() - window.winfo_reqwidth()) // 2
    y_offset = (window.winfo_screenheight() - window.winfo_reqheight()) // 2
    window.geometry('+{}+{}'.format(x_offset, y_offset))

def adicionar_regra_firewall(programa, nome_regra):
    tipo = "out"  # 'in' para tráfego de entrada, 'out' para tráfego de saída
    acao = "block"  # 'allow' para permitir, 'block' para bloquear
    perfil = "any"  # 'domain', 'public', 'private', 'any'

    # Compondo o comando netsh para adicionar a regra de saída
    comando = ['netsh', 'advfirewall', 'firewall', 'add', 'rule',
               'name="{}"'.format(nome_regra),
               'dir={}'.format(tipo),
               'action={}'.format(acao),
               'program="{}"'.format(programa),
               'profile={}'.format(perfil)]

    # Executando o comando com privilégios de administrador
    try:
        subprocess.run(comando, shell=True, check=True)
        messagebox.showinfo("Sucesso", "Regra de firewall adicionada com sucesso.")
    except subprocess.CalledProcessError as e:
        print("Erro ao adicionar regra de firewall:", e)
        messagebox.showerror("Erro", "Erro ao adicionar regra de firewall.")

    # Perguntar ao usuário se deseja adicionar mais regras
    resposta = messagebox.askyesno("Nova Regra", "Deseja adicionar outra regra de firewall?")
    if resposta:
        obter_dados()
    else:
        sys.exit(0)

def obter_dados():
    # Criar uma nova janela
    janela = tk.Toplevel()
    janela.title("Configuração de Regra de Firewall")
    janela.resizable(False, False)
    center_window(janela)  # Centralizar a janela

    # Ajustar o tamanho das colunas
    janela.grid_columnconfigure(1, minsize=20)
    janela.grid_columnconfigure(2, minsize=20)

    # Função para selecionar o arquivo
    def selecionar_arquivo():
        arquivo = filedialog.askopenfilename()
        if arquivo:
            entrada_formatada = os.path.normpath(arquivo)
            entrada_programa.delete(0, tk.END)
            entrada_programa.insert(0, entrada_formatada)

    # Criar campo de entrada para o caminho do programa
    label_programa = tk.Label(janela, text="Caminho do Programa:")
    label_programa.grid(row=0, column=0, padx=10, pady=5)
    entrada_programa = tk.Entry(janela, width=20)
    entrada_programa.grid(row=0, column=1, padx=10, pady=5)
    botao_selecionar = tk.Button(janela, text="...", command=selecionar_arquivo)
    botao_selecionar.grid(row=0, column=2, padx=5, pady=5)

    # Criar campo de entrada para o nome da regra
    label_nome_regra = tk.Label(janela, text="Nome da Regra de Firewall:")
    label_nome_regra.grid(row=1, column=0, padx=10, pady=5)
    entrada_nome_regra = tk.Entry(janela, width=20)
    entrada_nome_regra.grid(row=1, column=1, padx=10, pady=5)

    # Função para adicionar a regra de firewall
    def adicionar_regra():
        programa = entrada_programa.get()
        nome_regra = entrada_nome_regra.get()
        adicionar_regra_firewall(programa, nome_regra)
        janela.destroy()

    # Função para cancelar e fechar a janela
    def cancelar():
        janela.destroy()
        sys.exit(1)

    # Configurar tratador de evento para fechar a janela
    janela.protocol("WM_DELETE_WINDOW", cancelar)

    # Botão para adicionar a regra de firewall
    botao_adicionar = tk.Button(janela, text="Adicionar Regra", command=adicionar_regra)
    botao_adicionar.grid(row=2, column=0, columnspan=1, pady=10, padx=0)

    # Botão para cancelar
    botao_cancelar = tk.Button(janela, text="Cancelar", command=cancelar)
    botao_cancelar.grid(row=2, column=1, columnspan=2, pady=0, padx=0)

    # Botão para sobre
    botao_sobre = tk.Button(janela, text="Sobre", command=about_me)
    botao_sobre.grid(row=2, column=2, columnspan=1, pady=0, padx=10)

    

def main():
    window = tk.Tk()
    window.withdraw()  # Esconder a janela principal do Tkinter
    obter_dados()
    window.mainloop()

if __name__ == "__main__":
    # Solicitar privilégios de administrador
    if not pyuac.isUserAdmin():
        pyuac.runAsAdmin()
    else:
        main()
