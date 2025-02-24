import tkinter as tk
from tkinter import messagebox
import requests
import pandas as pd
from datetime import datetime
import os

# Função para obter dados climáticos de São Paulo
def obter_temperatura():
    api_key = "e81b43e6cdf8edc65c86e001ce64df24"  
    url = "https://api.openweathermap.org/data/2.5/weather?q=Sao%20Paulo,BR&appid=" + api_key + "&units=metric&lang=pt"
    
    try:
        resposta = requests.get(url)
        dados = resposta.json()
        
        if "main" in dados:
            temperatura = dados['main']['temp']
            umidade = dados['main']['humidity']
            descricao_umidade = "Alta" if umidade > 70 else "Média" if umidade > 40 else "Baixa"
            
            salvar_dados(temperatura, descricao_umidade)
            
            messagebox.showinfo("Sucesso", f"Temperatura: {temperatura}°C\nUmidade: {descricao_umidade}")
        else:
            messagebox.showerror("Erro", f"Resposta inesperada da API: {dados}")
    except Exception as e:
        messagebox.showerror("Erro", "Não foi possível obter os dados. Verifique sua conexão.")
        print(e)

# Função para salvar dados em uma planilha
def salvar_dados(temperatura, umidade):
    arquivo = "historico_temperatura.xlsx"
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    novo_dado = pd.DataFrame([[data_hora, temperatura, umidade]], columns=["Data/Hora", "Temperatura", "Umidade"])
    
    if os.path.exists(arquivo):
        df = pd.read_excel(arquivo)
        df = pd.concat([df, novo_dado], ignore_index=True)
    else:
        df = novo_dado
    
    df.to_excel(arquivo, index=False)

# Criando a interface gráfica
janela = tk.Tk()
janela.title("Captador de Temperatura - São Paulo")
janela.geometry("350x200")

label_titulo = tk.Label(janela, text="Captador de Temperatura", font=("Arial", 14))
label_titulo.pack(pady=10)

botao_capturar = tk.Button(janela, text="Capturar Dados", font=("Arial", 12), command=obter_temperatura)
botao_capturar.pack(pady=10)

janela.mainloop()
