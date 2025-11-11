# Calculadora Bonita com CustomTkinter
# Autor: Leonardo de Moura Fuseti


import customtkinter as ctk
from tkinter import END
import math

class Calculadora:
    def __init__(self):
        # Configurar modo de aparência e tema de cores
        ctk.set_appearance_mode("dark")  # "light" ou "dark"
        ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"
        
        # Criar janela principal
        self.janela = ctk.CTk()
        self.janela.title("Calculadora Fuseti")
        self.janela.geometry("400x600")
        self.janela.resizable(False, False)
        
        # Cores personalizadas
        self.cor_fundo = "#1a1a1a"
        self.cor_display = "#2d2d2d"
        self.cor_numero = "#404040"
        self.cor_operador = "#ff6b35"
        self.cor_igual = "#4CAF50"
        self.cor_limpar = "#f44336"
        
        # Variáveis de controle
        self.expressao_atual = ""
        self.total = 0
        
        self.criar_interface()
        
    def criar_interface(self):
        # Frame principal
        frame_principal = ctk.CTkFrame(self.janela, fg_color=self.cor_fundo)
        frame_principal.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Frame do display
        frame_display = ctk.CTkFrame(frame_principal, height=120, fg_color=self.cor_display)
        frame_display.pack(fill="x", padx=10, pady=(10, 20))
        frame_display.pack_propagate(False)
        
        # Campo de entrada do display
        self.display = ctk.CTkEntry(
            frame_display,
            font=ctk.CTkFont(size=32, weight="bold"),
            height=60,
            justify="right",
            border_width=0,
            fg_color="transparent",
            text_color="#ffffff"
        )
        self.display.pack(fill="both", expand=True, padx=20, pady=20)
        self.display.insert(0, "0")
        
        # Frame dos botões
        frame_botoes = ctk.CTkFrame(frame_principal, fg_color="transparent")
        frame_botoes.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Configuração padrão dos botões
        config_botao = {
            "font": ctk.CTkFont(size=20, weight="bold"),
            "height": 70,
            "corner_radius": 15,
            "border_width": 0
        }
        
        # Linha 1: Limpar, ±, %, ÷
        self.criar_botao(frame_botoes, "C", 0, 0, self.cor_limpar, self.limpar_tudo, config_botao)
        self.criar_botao(frame_botoes, "±", 0, 1, self.cor_numero, self.inverter_sinal, config_botao)
        self.criar_botao(frame_botoes, "%", 0, 2, self.cor_numero, lambda: self.adicionar_expressao("%"), config_botao)
        self.criar_botao(frame_botoes, "÷", 0, 3, self.cor_operador, lambda: self.adicionar_operador("/"), config_botao)
        
        # Linha 2: 7, 8, 9, ×
        self.criar_botao(frame_botoes, "7", 1, 0, self.cor_numero, lambda: self.adicionar_expressao("7"), config_botao)
        self.criar_botao(frame_botoes, "8", 1, 1, self.cor_numero, lambda: self.adicionar_expressao("8"), config_botao)
        self.criar_botao(frame_botoes, "9", 1, 2, self.cor_numero, lambda: self.adicionar_expressao("9"), config_botao)
        self.criar_botao(frame_botoes, "×", 1, 3, self.cor_operador, lambda: self.adicionar_operador("*"), config_botao)
        
        # Linha 3: 4, 5, 6, -
        self.criar_botao(frame_botoes, "4", 2, 0, self.cor_numero, lambda: self.adicionar_expressao("4"), config_botao)
        self.criar_botao(frame_botoes, "5", 2, 1, self.cor_numero, lambda: self.adicionar_expressao("5"), config_botao)
        self.criar_botao(frame_botoes, "6", 2, 2, self.cor_numero, lambda: self.adicionar_expressao("6"), config_botao)
        self.criar_botao(frame_botoes, "-", 2, 3, self.cor_operador, lambda: self.adicionar_operador("-"), config_botao)
        
        # Linha 4: 1, 2, 3, +
        self.criar_botao(frame_botoes, "1", 3, 0, self.cor_numero, lambda: self.adicionar_expressao("1"), config_botao)
        self.criar_botao(frame_botoes, "2", 3, 1, self.cor_numero, lambda: self.adicionar_expressao("2"), config_botao)
        self.criar_botao(frame_botoes, "3", 3, 2, self.cor_numero, lambda: self.adicionar_expressao("3"), config_botao)
        self.criar_botao(frame_botoes, "+", 3, 3, self.cor_operador, lambda: self.adicionar_operador("+"), config_botao)
        
        # Linha 5: 0 (ocupa 2 colunas), ., =
        config_zero = config_botao.copy()
        self.criar_botao(frame_botoes, "0", 4, 0, self.cor_numero, lambda: self.adicionar_expressao("0"), config_zero, columnspan=2)
        self.criar_botao(frame_botoes, ".", 4, 2, self.cor_numero, lambda: self.adicionar_expressao("."), config_botao)
        self.criar_botao(frame_botoes, "=", 4, 3, self.cor_igual, self.calcular, config_botao)
        
        # Configurar pesos da grade para design responsivo
        for i in range(5):
            frame_botoes.grid_rowconfigure(i, weight=1)
        for i in range(4):
            frame_botoes.grid_columnconfigure(i, weight=1)
    
    def criar_botao(self, pai, texto, linha, coluna, cor, comando, config, columnspan=1):
        """Método auxiliar para criar botões estilizados"""
        cor_hover = self.ajustar_brilho_cor(cor, 1.2)
        
        botao = ctk.CTkButton(
            pai,
            text=texto,
            command=comando,
            fg_color=cor,
            hover_color=cor_hover,
            text_color="#ffffff",
            **config
        )
        botao.grid(row=linha, column=coluna, columnspan=columnspan, padx=3, pady=3, sticky="nsew")
        return botao
    
    def ajustar_brilho_cor(self, cor_hex, fator):
        """Ajustar o brilho de uma cor em formato hexadecimal"""
        cor_hex = cor_hex.lstrip('#')
        rgb = tuple(int(cor_hex[i:i+2], 16) for i in (0, 2, 4))
        rgb = tuple(min(255, int(c * fator)) for c in rgb)
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
    
    def adicionar_expressao(self, valor):
        """Adicionar número ou ponto decimal à expressão atual"""
        atual = self.display.get()
        if atual == "0" or atual == "Erro":
            self.display.delete(0, END)
            self.display.insert(0, valor)
        else:
            self.display.delete(0, END)
            self.display.insert(0, atual + valor)
        self.expressao_atual += valor
    
    def adicionar_operador(self, operador):
        """Adicionar operador à expressão atual"""
        atual = self.display.get()
        if atual and atual != "Erro":
            self.expressao_atual += operador
            self.display.delete(0, END)
            self.display.insert(0, atual + operador)
    
    def limpar_tudo(self):
        """Limpar o display e resetar a expressão"""
        self.display.delete(0, END)
        self.display.insert(0, "0")
        self.expressao_atual = ""
    
    def inverter_sinal(self):
        """Inverter o sinal do número atual"""
        atual = self.display.get()
        if atual and atual != "0" and atual != "Erro":
            if atual.startswith("-"):
                novo_valor = atual[1:]
            else:
                novo_valor = "-" + atual
            self.display.delete(0, END)
            self.display.insert(0, novo_valor)
    
    def calcular(self):
        """Avaliar a expressão atual"""
        try:
            expressao = self.display.get()
            # Substituir símbolos visuais por operadores do Python
            expressao = expressao.replace("×", "*").replace("÷", "/")
            
            # Tratar porcentagem
            if "%" in expressao:
                partes = expressao.split("%")
                if len(partes) == 2:
                    expressao = partes[0] + "*0.01"
            
            resultado = eval(expressao)
            
            # Formatar o resultado
            if resultado == int(resultado):
                resultado = int(resultado)
            else:
                resultado = round(resultado, 8)
            
            self.display.delete(0, END)
            self.display.insert(0, str(resultado))
            self.expressao_atual = str(resultado)
            
        except:
            self.display.delete(0, END)
            self.display.insert(0, "Erro")
            self.expressao_atual = ""
    
    def executar(self):
        """Iniciar a aplicação da calculadora"""
        self.janela.mainloop()

# Criar e executar a calculadora
if __name__ == "__main__":
    calculadora = Calculadora()
    calculadora.executar()