
"""
FALAMIGO v3.2 Windows Edition
Aplicativo TTS para Windows usando Tkinter e pyttsx3
"""

import os
import sys
import random
import threading
import tkinter as tk
from tkinter import ttk, font

# CONFIGURAÇÃO DO TTS
try:
    import pyttsx3
    TTS_ENGINE = pyttsx3.init()
    TTS_ENGINE.setProperty('rate', 150)
    TTS_ENGINE.setProperty('volume', 0.9)
    voices = TTS_ENGINE.getProperty('voices')
    for voice in voices:
        if 'portuguese' in voice.name.lower() or 'brazil' in voice.name.lower():
            TTS_ENGINE.setProperty('voice', voice.id)
            break
    TTS_METHOD = "pyttsx3"
except ImportError:
    print("Aviso: pyttsx3 não instalado. Instale com: pip install pyttsx3")
    TTS_METHOD = "none"

# PALETA DE CORES
COLORS = {
    'acao': '#27AE60', 'objeto': '#F39C12', 'emocao': '#3498DB',
    'social': '#EC7063', 'lugar': '#9B59B6', 'necessidade': '#16A085',
    'config': '#7F8C8D', 'emergencia': '#E74C3C', 'header': '#2C3E50',
    'bg': '#F0F4F7', 'white': '#FFFFFF', 'display_border': '#3498DB',
    'text_dark': '#2C3E50', 'text_light': '#FFFFFF',
}

WELCOME_COLORS = ['#F0F4F7', '#E8F6F3', '#FEF9E7', '#F5EEF8', '#EBF5FB', '#FDEDEC', '#F5F7DC', '#FFFAF0', '#E0F7FA', '#F3E5F5']

# DADOS DAS CATEGORIAS
CATEGORY_DATA = {
    'conversar': {'title': 'FALAR', 'color': COLORS['acao'], 'items': [
        ("OI!", "Oi", COLORS['acao']), ("TUDO BEM?", "Tudo bem?", '#2ECC71'),
        ("BOM DIA", "Bom dia", '#F1C40F'), ("BOA NOITE", "Boa noite", COLORS['lugar']),
        ("SIM", "Sim", COLORS['acao']), ("NÃO", "Não", COLORS['emergencia']),
        ("OBRIGADO", "Obrigado", COLORS['emocao']), ("TCHAU", "Tchau", '#95A5A6'),
        ("ESTOU DOENTE", "Estou doente, quero ligar para o meu pai ou mãe", COLORS['emergencia']),
        ("NÃO ESTOU BEM", "Não estou me sentindo bem, quero ligar para os meus pais", '#C0392B'),
        ("PRECISO DOS PAIS", "Preciso falar com os meus pais agora", COLORS['emergencia']),
        ("QUERO MÉDICO", "Quero ir ao médico", '#E67E22'),
    ]},
    'quero': {'title': 'QUERO', 'color': COLORS['acao'], 'items': [
        ("ÁGUA", "Quero água", COLORS['emocao']), ("COMIDA", "Quero comer", '#E67E22'),
        ("BRINCAR", "Quero brincar", COLORS['acao']), ("DESENHAR", "Quero desenhar", COLORS['lugar']),
        ("TV", "Quero ver TV", COLORS['emergencia']), ("MÚSICA", "Quero música", COLORS['objeto']),
        ("SAIR", "Quero sair", COLORS['necessidade']), ("DORMIR", "Quero dormir", '#34495E'),
    ]},
    'brincar': {'title': 'BRINCAR', 'color': COLORS['acao'], 'items': [
        ("BOLA", "Jogar bola", '#E67E22'), ("CARRINHO", "Carrinho", COLORS['emergencia']),
        ("LEGO", "Lego", COLORS['emocao']), ("DINO", "Dinossauro", COLORS['acao']),
        ("BONECA", "Boneca", '#FD79A8'), ("QUEBRA-CABEÇA", "Quebra-cabeça", '#FDCB6E'),
        ("BICICLETA", "Bicicleta", '#00B894'), ("BOLHAS", "Bolhas de sabão", '#74B9FF'),
    ]},
    'comer': {'title': 'COMER', 'color': COLORS['objeto'], 'items': [
        ("MAÇÃ", "Quero maçã", COLORS['emergencia']), ("BANANA", "Quero banana", '#F1C40F'),
        ("PÃO", "Quero pão", '#D35400'), ("ARROZ", "Quero arroz", '#BDC3C7'),
        ("CARNE", "Quero carne", '#C0392B'), ("FRANGO", "Quero frango", '#E67E22'),
        ("LEITE", "Quero leite", '#ECF0F1'), ("SUCO", "Quero suco", COLORS['objeto']),
    ]},
    'preciso': {'title': 'PRECISO', 'color': COLORS['necessidade'], 'items': [
        ("BANHEIRO", "Vou ao banheiro", COLORS['necessidade']), ("BANHO", "Vou tomar banho", '#1ABC9C'),
        ("ROUPA", "Preciso trocar de roupa", COLORS['lugar']), ("AJUDA", "Preciso de ajuda", COLORS['emergencia']),
        ("REMÉDIO", "Preciso do remédio", COLORS['emocao']), ("DENTES", "Vou escovar os dentes", '#1ABC9C'),
        ("ABRAÇO", "Quero um abraço", '#FD79A8'), ("ATENÇÃO", "Preciso de atenção", '#F1C40F'),
    ]},
    'sinto': {'title': 'SENTIR', 'color': COLORS['emocao'], 'items': [
        ("FELIZ", "Estou feliz", '#F1C40F'), ("TRISTE", "Estou triste", COLORS['emocao']),
        ("RAIVA", "Estou com raiva", COLORS['emergencia']), ("MEDO", "Estou com medo", COLORS['lugar']),
        ("CANSADO", "Estou cansado", '#34495E'), ("FOME", "Estou com fome", '#E67E22'),
        ("SEDE", "Estou com sede", COLORS['emocao']), ("DOR", "Estou com dor", '#C0392B'),
        ("CALOR", "Estou com calor", COLORS['emergencia']), ("FRIO", "Estou com frio", '#74B9FF'),
        ("SONO", "Estou com sono", '#6C5CE7'), ("AMOR", "Eu te amo", '#FD79A8'),
    ]},
    'familia': {'title': 'FAMÍLIA', 'color': COLORS['lugar'], 'items': [
        ("PAPAI", "Papai", '#3498DB'), ("MAMÃE", "Mamãe", '#E84393'),
        ("VOVÔ", "Vovô", '#7F8C8D'), ("VOVÓ", "Vovó", '#546E7A'),
        ("IRMÃO", "Irmão", '#0984E3'), ("IRMÃ", "Irmã", '#F368E0'),
        ("CACHORRO", "Meu cachorro", '#E67E22'), ("GATO", "Meu gato", '#95A5A6'),
    ]},
}

class FalamigoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Falamigo v3.2")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        self.root.configure(bg=COLORS['bg'])
        self.phrase = []
        self.user_name = tk.StringVar(value="Cleomilson")
        self.current_frame = None
        self.screen_history = []
        self.font_title = font.Font(family="Segoe UI", size=28, weight="bold")
        self.font_header = font.Font(family="Segoe UI", size=18, weight="bold")
        self.font_button = font.Font(family="Segoe UI", size=11, weight="bold")
        self.font_normal = font.Font(family="Segoe UI", size=11)
        self.font_small = font.Font(family="Segoe UI", size=9)
        self.show_welcome_screen()

    def speak(self, text):
        def run():
            try:
                if TTS_METHOD == "pyttsx3":
                    engine = pyttsx3.init()
                    engine.setProperty('rate', 150)
                    engine.setProperty('volume', 0.9)
                    voices = engine.getProperty('voices')
                    for voice in voices:
                        if 'portuguese' in voice.name.lower() or 'brazil' in voice.name.lower():
                            engine.setProperty('voice', voice.id)
                            break
                    engine.say(text)
                    engine.runAndWait()
                else:
                    print(f"[TTS] {text}")
            except Exception as e:
                print(f"Erro TTS: {e}")
        threading.Thread(target=run, daemon=True).start()

    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

    def create_button(self, parent, text, bg_color, command, fg_color=None, height=2, width=15):
        if fg_color is None:
            fg_color = COLORS['text_light'] if bg_color != COLORS['white'] else COLORS['text_dark']
        btn = tk.Button(parent, text=text, bg=bg_color, fg=fg_color, font=self.font_button,
                        relief="flat", cursor="hand2", height=height, width=width,
                        command=command, activebackground=self.darken(bg_color), bd=0, padx=10, pady=5)
        return btn

    def darken(self, hex_color, factor=0.8):
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darkened = tuple(int(c * factor) for c in rgb)
        return f'#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}'

    def show_welcome_screen(self):
        self.clear_frame()
        self.screen_history = []
        bg_color = random.choice(WELCOME_COLORS)
        self.current_frame = tk.Frame(self.root, bg=bg_color)
        self.current_frame.pack(fill="both", expand=True)
        container = tk.Frame(self.current_frame, bg=bg_color)
        container.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(container, text="[ F ]", font=font.Font(family="Segoe UI", size=72, weight="bold"),
                 fg=COLORS['emocao'], bg=bg_color).pack(pady=10)
        tk.Label(container, text="FALAMIGO", font=self.font_title, fg=COLORS['header'], bg=bg_color).pack()
        tk.Label(container, text="Seu assistente de comunicação", font=self.font_normal,
                 fg=COLORS['config'], bg=bg_color).pack(pady=20)
        tk.Label(container, text="Seja bem-vindo!", font=font.Font(family="Segoe UI", size=14, weight="bold"),
                 fg=COLORS['emocao'], bg=bg_color).pack(pady=20)
        name_frame = tk.Frame(container, bg=bg_color)
        name_frame.pack(pady=20)
        tk.Label(name_frame, text="Seu nome:", font=self.font_small, fg=COLORS['header'], bg=bg_color).pack()
        tk.Entry(name_frame, textvariable=self.user_name, font=self.font_normal, justify="center",
                 width=25, relief="flat", bg=COLORS['white'], fg=COLORS['header'],
                 highlightthickness=1, highlightcolor=COLORS['emocao']).pack(pady=5)
        self.create_button(container, "ENTRAR NO APP", COLORS['acao'], self.enter_app, height=2, width=20).pack(pady=20)
        tk.Label(container, text="Versão 3.2 Windows Edition", font=self.font_small,
                 fg=COLORS['config'], bg=bg_color).pack(side="bottom", pady=20)

    def enter_app(self):
        nome = self.user_name.get().strip()
        if nome:
            terminacoes = ['a', 'e', 'i', 'y']
            ultima = nome[-1].lower() if nome else ''
            saudacao = f"Bem-vinda, {nome}!" if ultima in terminacoes else f"Bem-vindo, {nome}!"
            self.speak(saudacao)
        self.show_menu_screen()

    def show_menu_screen(self):
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg=COLORS['bg'])
        self.current_frame.pack(fill="both", expand=True)
        header = tk.Frame(self.current_frame, bg=COLORS['header'], height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="FALAMIGO", font=self.font_header, fg=COLORS['white'], bg=COLORS['header']).pack(expand=True)
        display_frame = tk.Frame(self.current_frame, bg=COLORS['white'], highlightbackground=COLORS['display_border'], highlightthickness=2)
        display_frame.pack(fill="x", padx=20, pady=15)
        self.display_label = tk.Label(display_frame, text="Toque para falar...", font=self.font_normal,
                                      fg=COLORS['header'], bg=COLORS['white'], wraplength=700, height=3)
        self.display_label.pack(fill="x", padx=10, pady=10)
        ctrl_frame = tk.Frame(self.current_frame, bg=COLORS['bg'])
        ctrl_frame.pack(fill="x", padx=20, pady=5)
        self.create_button(ctrl_frame, "FALAR", COLORS['acao'],
                           lambda: self.speak(' '.join(self.phrase)) if self.phrase else None, width=12).pack(side="left", expand=True, padx=5)
        self.create_button(ctrl_frame, "VOLTAR", COLORS['objeto'], self.undo_last, width=12).pack(side="left", expand=True, padx=5)
        self.create_button(ctrl_frame, "LIMPAR", COLORS['emergencia'], self.clear_all, width=12).pack(side="left", expand=True, padx=5)
        nav_frame = tk.Frame(self.current_frame, bg=COLORS['bg'])
        nav_frame.pack(fill="x", padx=20, pady=5)
        self.create_button(nav_frame, "← VOLTAR", COLORS['header'], self.go_back, width=12).pack(side="left", expand=True, padx=5)
        self.create_button(nav_frame, "INÍCIO", COLORS['header'], lambda: self.show_menu_screen(), width=12).pack(side="left", expand=True, padx=5)
        grid_frame = tk.Frame(self.current_frame, bg=COLORS['bg'])
        grid_frame.pack(fill="both", expand=True, padx=20, pady=10)
        for i in range(2):
            grid_frame.grid_columnconfigure(i, weight=1)
            grid_frame.grid_rowconfigure(i, weight=1)
        categories = [
            ("FALAR", COLORS['acao'], lambda: self.show_category('conversar'), "QUERO", COLORS['acao'], lambda: self.show_category('quero')),
            ("BRINCAR", COLORS['acao'], lambda: self.show_category('brincar'), "COMER", COLORS['objeto'], lambda: self.show_category('comer')),
            ("PRECISO", COLORS['necessidade'], lambda: self.show_category('preciso'), "SENTIR", COLORS['emocao'], lambda: self.show_category('sinto')),
            ("FAMÍLIA", COLORS['lugar'], lambda: self.show_category('familia'), "AJUSTES", COLORS['config'], self.show_config),
        ]
        row, col = 0, 0
        for cat in categories:
            cell = tk.Frame(grid_frame, bg=COLORS['bg'])
            cell.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
            self.create_button(cell, cat[0], cat[1], cat[2], height=4).pack(fill="both", expand=True, pady=(0, 3))
            self.create_button(cell, cat[3], cat[4], cat[5], height=4).pack(fill="both", expand=True, pady=(3, 0))
            col += 1
            if col > 1:
                col = 0
                row += 1
        self.update_display()

    def update_display(self):
        if self.phrase:
            self.display_label.config(text=' '.join(self.phrase), fg=COLORS['header'])
        else:
            self.display_label.config(text="Toque para falar...", fg=COLORS['config'])

    def undo_last(self):
        if self.phrase:
            self.phrase.pop()
            self.update_display()

    def clear_all(self):
        self.phrase = []
        self.update_display()

    def go_back(self):
        if self.screen_history:
            screen = self.screen_history.pop()
            if screen == 'menu':
                self.show_menu_screen()

    def show_category(self, category_key):
        self.screen_history.append('menu')
        self.clear_frame()
        data = CATEGORY_DATA[category_key]
        self.current_frame = tk.Frame(self.root, bg=COLORS['bg'])
        self.current_frame.pack(fill="both", expand=True)
        header = tk.Frame(self.current_frame, bg=data['color'], height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        self.create_button(header, "← VOLTAR", COLORS['white'], self.show_menu_screen,
                           fg_color=data['color'], width=10).pack(side="left", padx=10)
        tk.Label(header, text=data['title'], font=self.font_header, fg=COLORS['white'], bg=data['color']).pack(side="left", expand=True)
        canvas_frame = tk.Frame(self.current_frame, bg=COLORS['bg'])
        canvas_frame.pack(fill="both", expand=True, padx=20, pady=10)
        canvas = tk.Canvas(canvas_frame, bg=COLORS['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['bg'])
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        for i in range(2):
            scrollable_frame.grid_columnconfigure(i, weight=1)
        row, col = 0, 0
        for label, phrase, color in data['items']:
            self.create_button(scrollable_frame, label, color, lambda p=phrase, c=color: self.add_phrase(p, c),
                               height=3, width=15).grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
            col += 1
            if col > 1:
                col = 0
                row += 1

    def add_phrase(self, phrase, color):
        self.phrase.append(phrase)
        self.speak(phrase)
        if hasattr(self, 'display_label'):
            self.update_display()
            self.display_label.master.config(highlightbackground=color)
            self.root.after(300, lambda: self.display_label.master.config(highlightbackground=COLORS['display_border']))

    def show_config(self):
        self.screen_history.append('menu')
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg=COLORS['bg'])
        self.current_frame.pack(fill="both", expand=True)
        tk.Label(self.current_frame, text="AJUSTES", font=self.font_title, fg=COLORS['header'], bg=COLORS['bg']).pack(pady=30)
        container = tk.Frame(self.current_frame, bg=COLORS['bg'])
        container.pack(pady=20)
        tk.Label(container, text="Seu nome:", font=self.font_normal, fg=COLORS['config'], bg=COLORS['bg']).pack(anchor="w", pady=(0, 5))
        tk.Entry(container, textvariable=self.user_name, font=self.font_normal, width=30, relief="flat",
                 bg=COLORS['white'], fg=COLORS['header'], highlightthickness=1, highlightcolor=COLORS['emocao']).pack(pady=(0, 20))
        tk.Label(container, text=f"TTS: {TTS_METHOD.upper()}", font=self.font_small, fg=COLORS['config'], bg=COLORS['bg']).pack(pady=(0, 30))
        self.create_button(container, "TELA INICIAL", COLORS['emocao'], self.show_welcome_screen, width=20).pack(pady=5)
        self.create_button(container, "SALVAR E VOLTAR", COLORS['acao'], self.show_menu_screen, width=20).pack(pady=5)

def main():
    root = tk.Tk()
    style = ttk.Style()
    available_themes = style.theme_names()
    if 'clam' in available_themes:
        style.theme_use('clam')
    elif 'alt' in available_themes:
        style.theme_use('alt')
    app = FalamigoApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
