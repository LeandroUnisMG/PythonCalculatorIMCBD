import pyodbc
import tkinter as tk
from tkinter import messagebox


def conectar_banco():
    try:
        conexao = pyodbc.connect(
            "Driver={SQL Server};"
            "Server=DESKTOP-EM29UCK\PROJECTS;"  
            "Database=IMC;"  
            "Trusted_Connection=yes;"
        )
        return conexao
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")
        return None


def calcular_imc():
    try:
        nome = nome_entry.get()
        endereco = endereco_entry.get()
        altura = float(altura_entry.get()) / 100  
        peso = float(peso_entry.get())

        if altura <= 0 or peso <= 0:
            raise ValueError("Altura e peso devem ser maiores que zero.")

        imc = peso / (altura ** 2)
        resultado_text.set(f"IMC: {imc:.2f}")

       
        conexao = conectar_banco()
        if conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "INSERT INTO Pacientes (Nome, Endereco, Altura, Peso, IMC) VALUES (?, ?, ?, ?, ?)",
                (nome, endereco, altura, peso, imc)
            )
            conexao.commit()
            conexao.close()
            messagebox.showinfo("Sucesso", "Dados salvos no banco de dados com sucesso!")
    except ValueError as ve:
        messagebox.showerror("Erro", f"Erro nos dados fornecidos: {ve}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao calcular ou salvar os dados: {e}")


def reiniciar():
    nome_entry.delete(0, tk.END)
    endereco_entry.delete(0, tk.END)
    altura_entry.delete(0, tk.END)
    peso_entry.delete(0, tk.END)
    resultado_text.set("")


def sair():
    janela.destroy()


janela = tk.Tk()
janela.title("Cálculo do IMC - Índice de Massa Corporal")


tk.Label(janela, text="Nome do Paciente:").grid(row=0, column=0, sticky="w")
nome_entry = tk.Entry(janela, width=50)
nome_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(janela, text="Endereço Completo:").grid(row=1, column=0, sticky="w")
endereco_entry = tk.Entry(janela, width=50)
endereco_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(janela, text="Altura (cm):").grid(row=2, column=0, sticky="w")
altura_entry = tk.Entry(janela)
altura_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

tk.Label(janela, text="Peso (Kg):").grid(row=3, column=0, sticky="w")
peso_entry = tk.Entry(janela)
peso_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

resultado_text = tk.StringVar()
resultado_label = tk.Label(janela, textvariable=resultado_text, width=30, height=5, relief="sunken")
resultado_label.grid(row=2, column=2, rowspan=2, padx=10, pady=5)

# Botões
tk.Button(janela, text="Calcular", command=calcular_imc).grid(row=4, column=0, pady=10)
tk.Button(janela, text="Reiniciar", command=reiniciar).grid(row=4, column=1, pady=10)
tk.Button(janela, text="Sair", command=sair).grid(row=4, column=2, pady=10)

janela.mainloop()
