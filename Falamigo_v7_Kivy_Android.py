
"""
Falamigo AAC v7.0 - Versao Kivy para Android
Autor: HGC Software Solutions
Compativel com: Buildozer (APK) / Pydroid3 / Desktop
"""

import json
import os
from datetime import datetime

# Kivy imports
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.progressbar import ProgressBar
from kivy.uix.slider import Slider
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.utils import get_color_from_hex
from kivy.metrics import dp, sp

# TTS
try:
    import pyttsx3
    TTS_ENGINE = pyttsx3.init()
    TTS_ENGINE.setProperty("rate", 150)
    TTS_ENGINE.setProperty("volume", 1.0)
    print("[TTS] pyttsx3 OK")
except Exception as e:
    print(f"[TTS] pyttsx3 nao disponivel: {e}")
    TTS_ENGINE = None

CORES = {
    "primaria": "#1565C0", "secundaria": "#1976D2", "sucesso": "#4CAF50",
    "alerta": "#FF9800", "perigo": "#D32F2F", "fundo": "#E3F2FD",
    "branco": "#FFFFFF", "texto": "#333333", "cinza": "#757575",
    "quero": "#2196F3", "preciso": "#4CAF50", "pessoas": "#E91E63",
    "lugares": "#9C27B0", "comidas": "#FF5722", "brincar": "#FF9800",
    "rotina_manha": "#FF9800", "rotina_tarde": "#FFC107",
    "rotina_noite": "#3F51B5", "sinto": "#FFC107",
    "perguntas": "#9C27B0", "fichario": "#4CAF50", "config": "#757575",
}

CATEGORIAS = {
    "quero": {"titulo": "QUERO", "cor": CORES["quero"],
        "itens": [("AGUA","Quero agua"),("COMER","Quero comer"),("BANHEIRO","Quero banheiro"),
                  ("DORMIR","Quero dormir"),("BRINCAR","Quero brincar"),("TV","Quero ver TV"),
                  ("MUSICA","Quero musica"),("SAIR","Quero sair"),("CELULAR","Quero o celular"),
                  ("LIVRO","Quero ler um livro"),("DESENHAR","Quero desenhar"),("JOGAR","Quero jogar")]},
    "preciso": {"titulo": "PRECISO", "cor": CORES["preciso"],
        "itens": [("AJUDA","Preciso de ajuda"),("ABRACO","Quero um abraco"),("SIM","Sim"),
                  ("NAO","Nao"),("GOSTEI","Gostei"),("NAO SEI","Nao sei"),
                  ("POR FAVOR","Por favor"),("OBRIGADO","Obrigado"),("SILENCIO","Quero silencio"),
                  ("PARAR","Quero parar"),("MAIS","Quero mais"),("MENOS","Quero menos")]},
    "pessoas": {"titulo": "PESSOAS", "cor": CORES["pessoas"],
        "itens": [("MAE","Quero minha mae"),("PAI","Quero meu pai"),("VOVO (F)","Quero minha vovo"),
                  ("VOVO (M)","Quero meu vovo"),("IRMA","Quero minha irma"),("IRMAO","Quero meu irmao"),
                  ("PROFESSOR","Quero meu professor"),("MEDICO","Quero o medico"),
                  ("ENFERMEIRA","Quero a enfermeira"),("AMIGO","Quero meu amigo"),
                  ("POLICIAL","Preciso da policia"),("BOMBEIRO","Preciso dos bombeiros")]},
    "lugares": {"titulo": "LUGARES", "cor": CORES["lugares"],
        "itens": [("CASA","Quero ir para casa"),("ESCOLA","Quero ir para escola"),
                  ("HOSPITAL","Preciso ir ao hospital"),("MERCADO","Quero ir ao mercado"),
                  ("PARQUE","Quero ir ao parque"),("CINEMA","Quero ir ao cinema"),
                  ("PRAIA","Quero ir a praia"),("PARQUE DIV.","Quero ir ao parque de diversoes"),
                  ("PISCINA","Quero ir a piscina"),("LANCHONETE","Quero ir a lanchonete"),
                  ("PASSEAR","Quero passear de carro"),("QUINTAL","Quero ir ao quintal")]},
    "comidas": {"titulo": "COMIDAS", "cor": CORES["comidas"],
        "itens": [("PIZZA","Quero pizza"),("HAMBURGUER","Quero hamburguer"),("BATATA","Quero batata frita"),
                  ("MACARRAO","Quero macarrao"),("FRANGO","Quero frango"),("MACA","Quero maca"),
                  ("BANANA","Quero banana"),("SORVETE","Quero sorvete"),("CHOCOLATE","Quero chocolate"),
                  ("BISCOITO","Quero biscoito"),("SUCO","Quero suco"),("LEITE","Quero leite")]},
    "brincar": {"titulo": "BRINCAR", "cor": CORES["brincar"],
        "itens": [("BOLA","Quero jogar bola"),("QUEBRA-CABECA","Quero quebra-cabeca"),("JOGO","Quero jogar um jogo"),
                  ("BONECA","Quero brincar de boneca"),("CARRINHO","Quero brincar de carrinho"),("DESENHAR","Quero desenhar"),
                  ("FANTASIA","Quero brincar de fantasia"),("CIRCO","Quero brincar de circo"),
                  ("BLOCOS","Quero brincar de blocos"),("CANTAR","Quero cantar"),
                  ("DANCAR","Quero dancar"),("TEATRO","Quero brincar de teatro")]}
}

ROTINAS = {
    "manha": {"titulo": "ROTINA DA MANHA", "cor": CORES["rotina_manha"],
        "itens": [("ACORDAR","Acordei"),("BANHEIRO","Preciso ir ao banheiro"),("ESCOVAR","Quero escovar os dentes"),
                  ("BANHO","Quero tomar banho"),("ARRUMAR","Quero me arrumar"),("CAFE","Quero cafe da manha"),
                  ("REMEDIO","Preciso tomar remedio"),("ESCOLA","Quero ir para escola")]},
    "tarde": {"titulo": "ROTINA DA TARDE", "cor": CORES["rotina_tarde"],
        "itens": [("CHEGAR","Cheguei da escola"),("ALMOCAR","Quero almocar"),("LICAO","Quero fazer licao"),
                  ("BRINCAR","Quero brincar"),("TV","Quero ver TV"),("LANCHE","Quero lanche"),
                  ("SONECA","Quero dormir um pouco"),("DESENHAR","Quero desenhar")]},
    "noite": {"titulo": "ROTINA DA NOITE", "cor": CORES["rotina_noite"],
        "itens": [("JANTAR","Quero jantar"),("BANHO","Quero tomar banho"),("ESCOVAR","Quero escovar os dentes"),
                  ("HISTORIA","Quero ouvir uma historia"),("MUSICA","Quero ouvir musica"),
                  ("REMEDIO","Preciso tomar remedio"),("DORMIR","Quero dormir"),("PELÚCIA","Quero minha pelucia")]}
}

PERGUNTAS = {
    "geral": {"titulo": "PERGUNTAS GERAIS", "cor": CORES["perguntas"],
        "itens": [("POR QUE?","Por que?"),("O QUE?","O que?"),("QUEM?","Quem?"),("ONDE?","Onde?"),
                  ("QUANDO?","Quando?"),("QUAL?","Qual?"),("QUANTOS?","Quantos?"),("QUANTAS?","Quantas?"),
                  ("COMO?","Como?"),("O QUE ACONTECEU?","O que aconteceu?"),("PARA QUE?","Para que?"),("DE QUEM?","De quem?")]},
    "motivos": {"titulo": "POR QUE?", "cor": "#E91E63",
        "itens": [("POR QUE NAO?","Por que nao?"),("POR QUE SIM?","Por que sim?"),("POR QUE TRISTE?","Por que estou triste?"),
                  ("POR QUE BRAVO?","Por que estou bravo?"),("POR QUE ANSIOSO?","Por que estou ansioso?"),
                  ("POR QUE ACONTECEU?","Por que aconteceu?"),("POR QUE EU?","Por que eu?"),("POR QUE AGORA?","Por que agora?"),
                  ("POR QUE ISSO?","Por que isso?"),("POR QUE AQUI?","Por que aqui?"),("POR QUE ASSIM?","Por que assim?"),("POR QUE VOCE?","Por que voce?")]},
    "escolha": {"titulo": "ESCOLHAS", "cor": "#4CAF50",
        "itens": [("QUAL QUER?","Qual voce quer?"),("QUAL PREFERE?","Qual voce prefere?"),("QUAL MELHOR?","Qual e melhor?"),
                  ("QUAL SEU?","Qual e o seu?"),("QUAL DELE?","Qual e o dele?"),("QUAL DELA?","Qual e o dela?"),
                  ("QUAL NOSSO?","Qual e o nosso?"),("QUAL DELES?","Qual e o deles?"),("QUAL CERTO?","Qual e o certo?"),
                  ("QUAL ERRADO?","Qual e o errado?"),("QUAL PRIMEIRO?","Qual e o primeiro?"),("QUAL ULTIMO?","Qual e o ultimo?")]},
    "confirmacao": {"titulo": "CONFIRMACAO", "cor": "#2196F3",
        "itens": [("ESTA CERTO?","Esta certo?"),("ESTA ERRADO?","Esta errado?"),("ESTA BEM?","Esta bem?"),
                  ("ESTA BOM?","Esta bom?"),("ESTA PRONTO?","Esta pronto?"),("ESTA ACABANDO?","Esta acabando?"),
                  ("ESTA COMECANDO?","Esta comecando?"),("ESTA ACABOU?","Esta acabou?"),("ESTA AQUI?","Esta aqui?"),
                  ("ESTA LA?","Esta la?"),("ESTA ASSIM?","Esta assim?"),("ESTA DIFERENTE?","Esta diferente?")]},
    "direcao": {"titulo": "DIRECAO", "cor": "#FF9800",
        "itens": [("PARA CIMA?","Para cima?"),("PARA BAIXO?","Para baixo?"),("PARA ESQUERDA?","Para esquerda?"),
                  ("PARA DIREITA?","Para direita?"),("PARA TRAS?","Para tras?"),("PARA FRENTE?","Para frente?"),
                  ("PARA ONDE?","Para onde?"),("PARA CASA?","Para casa?"),("PARA ESCOLA?","Para escola?"),
                  ("PARA HOSPITAL?","Para hospital?"),("PARA CARRO?","Para o carro?"),("PARA PORTA?","Para a porta?")]},
    "tempo": {"titulo": "TEMPO", "cor": "#00BCD4",
        "itens": [("DE MANHA?","De manha?"),("DE TARDE?","De tarde?"),("DE NOITE?","De noite?"),
                  ("AGORA?","Agora?"),("DEPOIS?","Depois?"),("ANTES?","Antes?"),
                  ("HOJE?","Hoje?"),("AMANHA?","Amanha?"),("ONTEM?","Ontem?"),
                  ("JA?","Ja?"),("AINDA?","Ainda?"),("QUE HORAS?","Que horas?")]}
}

SENTIMENTOS = [("FELIZ","Estou feliz","#4CAF50"),("TRISTE","Estou triste","#2196F3"),
    ("BRAVO","Estou bravo","#F44336"),("ANSIOSO","Estou ansioso","#FF9800"),
    ("COM MEDO","Estou com medo","#9C27B0"),("CANSADO","Estou cansado","#00BCD4"),("AMOR","Eu te amo","#E91E63")]

DORES = [("CABECA","Estou com dor de cabeca"),("BRACO","Estou com dor no braco"),("PERNA","Estou com dor na perna"),
    ("BARRIGA","Estou com dor na barriga"),("COSTAS","Estou com dor nas costas"),("PEITO","Estou com dor no peito"),
    ("DENTE","Estou com dor no dente"),("OLHO","Estou com dor no olho"),("GARGANTA","Estou com dor de garganta"),("OUVIDO","Estou com dor de ouvido")]

NIVEIS_DOR = [("1","Dor leve","#4CAF50"),("2","Dor moderada","#8BC34A"),("3","Dor forte","#FFC107"),
    ("4","Dor muito forte","#FF9800"),("5","Dor insuportavel","#F44336")]


class Storage:
    """Gerencia armazenamento local JSON"""
    def __init__(self):
        self.data_dir = os.path.join(os.path.expanduser("~"), ".falamigo")
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        self.users_file = os.path.join(self.data_dir, "users.json")
        self.config_file = os.path.join(self.data_dir, "config.json")
        self.rotinas_file = os.path.join(self.data_dir, "rotinas.json")

    def load_users(self):
        try:
            with open(self.users_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []

    def save_users(self, users):
        with open(self.users_file, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)

    def load_config(self):
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {"rate": 150, "volume": 1.0, "pitch": 1.0}

    def save_config(self, config):
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

    def load_rotinas(self, user_name):
        try:
            with open(self.rotinas_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get(user_name, {"manha": [], "tarde": [], "noite": []})
        except:
            return {"manha": [], "tarde": [], "noite": []}

    def save_rotinas(self, user_name, rotinas):
        try:
            with open(self.rotinas_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            data = {}
        data[user_name] = rotinas
        with open(self.rotinas_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


class FalamigoApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.storage = Storage()
        self.users = self.storage.load_users()
        self.current_user = None
        self.user_data = self.get_default_user_data()
        self.phrase = []
        self.rotinas_done = {"manha": [], "tarde": [], "noite": []}
        self.tts_config = self.storage.load_config()
        self.current_tab = "comunicar"

    def get_default_user_data(self):
        return {
            "nome": "", "idade": "", "genero": "", "responsavel": "", "telefone": "",
            "comidaFavorita": "", "desenhoFavorito": "", "corFavorita": "",
            "brinquedoFavorito": "", "musicaFavorita": "", "atividadeFavorita": "",
            "roupaFavorita": "", "animalFavorito": "", "lugarFavorito": "",
            "jogoFavorito": "", "personagemFavorito": "", "bebidaFavorita": "",
            "contatoEmergencia": "", "medicamentos": "", "alergias": "",
            "condicoesMedicas": "", "medico": "", "convenio": "", "tipoSanguineo": "",
            "escola": "", "serie": "", "professor": "", "amigos": "",
            "rotinaManha": "", "rotinaTarde": "", "rotinaNoite": "", "outrasInfo": ""
        }

    def build(self):
        Window.clearcolor = get_color_from_hex(CORES["fundo"])
        self.sm = ScreenManager()
        self.sm.add_widget(LoginScreen(name="login", app=self))
        self.sm.add_widget(MainScreen(name="main", app=self))
        self.sm.current = "login"
        return self.sm

    def speak(self, text):
        if not text:
            return
        print(f"[FALAR] {text}")
        main_screen = self.sm.get_screen("main")
        if main_screen:
            main_screen.update_display(text, speaking=True)
            Clock.schedule_once(lambda dt: main_screen.update_display(), 1.5)
        if TTS_ENGINE:
            try:
                TTS_ENGINE.setProperty("rate", self.tts_config.get("rate", 150))
                TTS_ENGINE.setProperty("volume", self.tts_config.get("volume", 1.0))
                TTS_ENGINE.say(text)
                TTS_ENGINE.runAndWait()
                return
            except Exception as e:
                print(f"[TTS Erro] {e}")
        # Android TTS via JNI
        try:
            from android.runnable import run_on_ui_thread
            from jnius import autoclass
            @run_on_ui_thread
            def android_tts():
                Locale = autoclass("java.util.Locale")
                TextToSpeech = autoclass("android.speech.tts.TextToSpeech")
                PythonActivity = autoclass("org.kivy.android.PythonActivity")
                activity = PythonActivity.mActivity
                tts = TextToSpeech(activity, None)
                tts.setLanguage(Locale("pt", "BR"))
                tts.speak(text, TextToSpeech.QUEUE_FLUSH, None)
            android_tts()
            return
        except Exception as e:
            print(f"[TTS] Android nao disponivel: {e}")

    def add_phrase(self, text):
        self.phrase.append(text)
        self.speak(text)
        main_screen = self.sm.get_screen("main")
        if main_screen:
            main_screen.update_display()

    def undo_phrase(self):
        if self.phrase:
            self.phrase.pop()
            self.speak("Desfeito")
            main_screen = self.sm.get_screen("main")
            if main_screen:
                main_screen.update_display()

    def clear_phrase(self):
        self.phrase = []
        self.speak("Apaguei tudo")
        main_screen = self.sm.get_screen("main")
        if main_screen:
            main_screen.update_display()

    def speak_all(self):
        if not self.phrase:
            self.speak("Adicione frases")
            return
        text = " ".join(self.phrase)
        self.speak(text)

    def vibrate(self, pattern=None):
        try:
            from android.runnable import run_on_ui_thread
            from jnius import autoclass
            @run_on_ui_thread
            def do_vibrate():
                PythonActivity = autoclass("org.kivy.android.PythonActivity")
                activity = PythonActivity.mActivity
                vibrator = activity.getSystemService("vibrator")
                if pattern:
                    vibrator.vibrate(pattern, -1)
                else:
                    vibrator.vibrate(300)
            do_vibrate()
        except:
            pass

    def save_user_data(self):
        if self.current_user:
            for i, u in enumerate(self.users):
                if u.get("nome") == self.current_user.get("nome"):
                    self.users[i] = dict(self.user_data)
                    break
            self.storage.save_users(self.users)
        self.storage.save_rotinas(self.user_data.get("nome", "guest"), self.rotinas_done)

    def load_user_data(self):
        if self.current_user:
            self.user_data.update(self.current_user)
            self.rotinas_done = self.storage.load_rotinas(self.user_data.get("nome", "guest"))


class LoginScreen(Screen):
    def __init__(self, app=None, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.build_ui()

    def build_ui(self):
        layout = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(15))
        title = Label(text="[b]FALAMIGO[/b]", markup=True, font_size=sp(32),
                      color=get_color_from_hex(CORES["primaria"]),
                      size_hint_y=None, height=dp(60))
        layout.add_widget(title)
        subtitle = Label(text="Seu assistente de comunicacao", font_size=sp(16),
                           color=get_color_from_hex(CORES["cinza"]),
                           size_hint_y=None, height=dp(30))
        layout.add_widget(subtitle)

        tabs = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        self.btn_entrar = Button(text="ENTRAR", background_color=get_color_from_hex(CORES["primaria"]),
                                 color=get_color_from_hex(CORES["branco"]), bold=True)
        self.btn_cadastrar = Button(text="CADASTRAR", background_color=get_color_from_hex(CORES["cinza"]),
                                    color=get_color_from_hex(CORES["branco"]), bold=True)
        self.btn_entrar.bind(on_press=lambda x: self.show_tab("entrar"))
        self.btn_cadastrar.bind(on_press=lambda x: self.show_tab("cadastrar"))
        tabs.add_widget(self.btn_entrar)
        tabs.add_widget(self.btn_cadastrar)
        layout.add_widget(tabs)

        scroll = ScrollView()
        self.content = BoxLayout(orientation="vertical", spacing=dp(10), size_hint_y=None)
        self.content.bind(minimum_height=self.content.setter("height"))
        scroll.add_widget(self.content)
        layout.add_widget(scroll)
        self.add_widget(layout)
        self.show_tab("entrar")

    def show_tab(self, tab):
        self.content.clear_widgets()
        if tab == "entrar":
            self.btn_entrar.background_color = get_color_from_hex(CORES["primaria"])
            self.btn_cadastrar.background_color = get_color_from_hex(CORES["cinza"])
            self.build_entrar()
        else:
            self.btn_entrar.background_color = get_color_from_hex(CORES["cinza"])
            self.btn_cadastrar.background_color = get_color_from_hex(CORES["primaria"])
            self.build_cadastrar()

    def build_entrar(self):
        users = self.app.users
        if not users:
            lbl = Label(text="Nenhum usuario cadastrado.\nCrie um novo!", font_size=sp(14),
                        color=get_color_from_hex(CORES["cinza"]),
                        size_hint_y=None, height=dp(60))
            self.content.add_widget(lbl)
        else:
            for i, user in enumerate(users):
                avatar = "F" if user.get("genero") == "feminino" else "M" if user.get("genero") == "masculino" else "?"
                info = f"{user.get('nome', 'Sem nome')} - {user.get('idade', '?')} anos"
                btn = Button(text=f"[{avatar}] {info}", size_hint_y=None, height=dp(60),
                             background_color=get_color_from_hex(CORES["secundaria"]),
                             color=get_color_from_hex(CORES["branco"]), font_size=sp(16))
                btn.bind(on_press=lambda x, idx=i: self.select_user(idx))
                self.content.add_widget(btn)
        btn_guest = Button(text="ENTRAR COMO CONVIDADO", size_hint_y=None, height=dp(60),
                           background_color=get_color_from_hex(CORES["alerta"]),
                           color=get_color_from_hex(CORES["branco"]), font_size=sp(16), bold=True)
        btn_guest.bind(on_press=self.login_guest)
        self.content.add_widget(btn_guest)

    def build_cadastrar(self):
        fields = [("nome", "Nome completo"), ("idade", "Idade"),
                  ("responsavel", "Responsavel (nome)"), ("telefone", "Telefone do responsavel")]
        self.inputs = {}
        for key, hint in fields:
            lbl = Label(text=hint, size_hint_y=None, height=dp(30),
                        color=get_color_from_hex(CORES["primaria"]),
                        font_size=sp(14), bold=True, halign="left")
            lbl.bind(size=lbl.setter("text_size"))
            self.content.add_widget(lbl)
            inp = TextInput(hint_text=hint, multiline=False, size_hint_y=None, height=dp(50),
                            font_size=sp(16), background_color=get_color_from_hex(CORES["branco"]),
                            foreground_color=get_color_from_hex(CORES["texto"]))
            self.inputs[key] = inp
            self.content.add_widget(inp)
        lbl_gen = Label(text="Genero", size_hint_y=None, height=dp(30),
                        color=get_color_from_hex(CORES["primaria"]),
                        font_size=sp(14), bold=True, halign="left")
        lbl_gen.bind(size=lbl_gen.setter("text_size"))
        self.content.add_widget(lbl_gen)
        self.spinner_genero = Spinner(text="Selecione",
            values=("Masculino", "Feminino", "Prefiro nao informar"),
            size_hint_y=None, height=dp(50), font_size=sp(16),
            background_color=get_color_from_hex(CORES["branco"]))
        self.content.add_widget(self.spinner_genero)
        btn = Button(text="CADASTRAR", size_hint_y=None, height=dp(60),
                     background_color=get_color_from_hex(CORES["sucesso"]),
                     color=get_color_from_hex(CORES["branco"]), font_size=sp(18), bold=True)
        btn.bind(on_press=self.register_user)
        self.content.add_widget(btn)

    def select_user(self, index):
        self.app.current_user = self.app.users[index]
        self.app.load_user_data()
        self.enter_app()

    def login_guest(self, instance):
        self.app.current_user = None
        self.app.user_data = self.app.get_default_user_data()
        self.app.user_data["nome"] = "Convidado"
        self.enter_app()

    def register_user(self, instance):
        nome = self.inputs["nome"].text.strip()
        if not nome:
            self.show_popup("Erro", "Por favor, digite o nome!")
            return
        genero_map = {"Masculino": "masculino", "Feminino": "feminino",
                      "Prefiro nao informar": "nao-informar", "Selecione": ""}
        new_user = {"nome": nome, "idade": self.inputs["idade"].text,
                    "genero": genero_map.get(self.spinner_genero.text, ""),
                    "responsavel": self.inputs["responsavel"].text,
                    "telefone": self.inputs["telefone"].text}
        new_user.update(self.app.get_default_user_data())
        new_user["contatoEmergencia"] = self.inputs["telefone"].text
        self.app.users.append(new_user)
        self.app.storage.save_users(self.app.users)
        self.app.current_user = new_user
        self.app.user_data = dict(new_user)
        self.show_popup("Sucesso", "Usuario cadastrado!")
        self.enter_app()

    def enter_app(self):
        main_screen = self.app.sm.get_screen("main")
        main_screen.setup()
        self.app.sm.current = "main"
        Clock.schedule_once(lambda dt: self.app.speak(
            f"Ola {self.app.user_data.get('nome', '')}! Bem-vindo ao Falamigo!"), 0.5)

    def show_popup(self, title, msg):
        popup = Popup(title=title, content=Label(text=msg, font_size=sp(16)),
                      size_hint=(0.8, 0.3), auto_dismiss=True)
        popup.open()


class MainScreen(Screen):
    def __init__(self, app=None, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.build_ui()

    def build_ui(self):
        self.main_layout = BoxLayout(orientation="vertical")
        # Header
        self.header = BoxLayout(size_hint_y=None, height=dp(50), padding=dp(5))
        with self.header.canvas.before:
            Color(*get_color_from_hex(CORES["primaria"]))
            self.header_rect = Rectangle(pos=self.header.pos, size=self.header.size)
        self.header.bind(pos=self.update_header_rect, size=self.update_header_rect)
        self.header_label = Label(text="FALAMIGO v7.0", font_size=sp(20),
                                  bold=True, color=get_color_from_hex(CORES["branco"]))
        self.header.add_widget(self.header_label)
        self.main_layout.add_widget(self.header)
        # Welcome
        self.welcome = Label(text="Ola!", font_size=sp(18), bold=True,
                             color=get_color_from_hex(CORES["primaria"]),
                             size_hint_y=None, height=dp(40))
        self.main_layout.add_widget(self.welcome)
        # Emergencia
        self.emergency_btn = Button(text="EMERGENCIA - TOQUE AQUI", size_hint_y=None, height=dp(50),
                                    background_color=get_color_from_hex(CORES["perigo"]),
                                    color=get_color_from_hex(CORES["branco"]),
                                    font_size=sp(16), bold=True)
        self.emergency_btn.bind(on_press=self.show_emergency)
        self.main_layout.add_widget(self.emergency_btn)
        # Display
        self.display = Label(text="Toque nas frases...", font_size=sp(18), bold=True,
                             color=get_color_from_hex(CORES["branco"]),
                             size_hint_y=None, height=dp(70), markup=True)
        with self.display.canvas.before:
            Color(*get_color_from_hex(CORES["secundaria"]))
            self.display_rect = Rectangle(pos=self.display.pos, size=self.display.size)
        self.display.bind(pos=self.update_display_rect, size=self.update_display_rect)
        self.main_layout.add_widget(self.display)
        # Controles
        controls = BoxLayout(size_hint_y=None, height=dp(55), spacing=dp(5), padding=dp(5))
        btn_speak = Button(text="FALAR", background_color=get_color_from_hex(CORES["sucesso"]),
                           color=get_color_from_hex(CORES["branco"]), font_size=sp(16), bold=True)
        btn_speak.bind(on_press=lambda x: self.app.speak_all())
        controls.add_widget(btn_speak)
        btn_undo = Button(text="DESFAZER", background_color=get_color_from_hex(CORES["alerta"]),
                          color=get_color_from_hex(CORES["branco"]), font_size=sp(14), bold=True)
        btn_undo.bind(on_press=lambda x: self.app.undo_phrase())
        controls.add_widget(btn_undo)
        btn_clear = Button(text="LIMPAR", background_color=get_color_from_hex(CORES["perigo"]),
                           color=get_color_from_hex(CORES["branco"]), font_size=sp(14), bold=True)
        btn_clear.bind(on_press=lambda x: self.app.clear_phrase())
        controls.add_widget(btn_clear)
        self.main_layout.add_widget(controls)
        # Content
        self.scroll = ScrollView()
        self.content_area = BoxLayout(orientation="vertical", spacing=dp(10),
                                      padding=dp(10), size_hint_y=None)
        self.content_area.bind(minimum_height=self.content_area.setter("height"))
        self.scroll.add_widget(self.content_area)
        self.main_layout.add_widget(self.scroll)
        # Nav
        self.nav = GridLayout(cols=4, size_hint_y=None, height=dp(70), spacing=dp(2))
        self.nav_buttons = {}
        nav_items = [("comunicar","COMUNICAR",CORES["primaria"]),("rotinas","ROTINAS",CORES["rotina_manha"]),
                     ("sobremim","SOBRE MIM",CORES["pessoas"]),("fichario","FICHARIO",CORES["fichario"]),
                     ("sinto","SINTO",CORES["sinto"]),("perguntas","PERGUNTAS",CORES["perguntas"]),
                     ("config","CONFIG",CORES["config"])]
        for key, label, color in nav_items:
            btn = Button(text=label, background_color=get_color_from_hex(color),
                         color=get_color_from_hex(CORES["branco"]), font_size=sp(11), bold=True)
            btn.bind(on_press=lambda x, k=key: self.switch_tab(k))
            self.nav_buttons[key] = btn
            self.nav.add_widget(btn)
        self.main_layout.add_widget(self.nav)
        self.add_widget(self.main_layout)

    def update_header_rect(self, instance, value):
        self.header_rect.pos = instance.pos
        self.header_rect.size = instance.size

    def update_display_rect(self, instance, value):
        self.display_rect.pos = instance.pos
        self.display_rect.size = instance.size

    def setup(self):
        nome = self.app.user_data.get("nome", "amigo")
        self.welcome.text = f"Ola, {nome}!"
        self.switch_tab("comunicar")

    def update_display(self, text=None, speaking=False):
        if text:
            self.display.text = f"[color=#FFFF00]>>[/color] {text}" if speaking else text
            with self.display.canvas.before:
                Color(*get_color_from_hex(CORES["sucesso"] if speaking else CORES["secundaria"]))
                self.display_rect = Rectangle(pos=self.display.pos, size=self.display.size)
        else:
            if not self.app.phrase:
                self.display.text = "Toque nas frases..."
            else:
                recent = self.app.phrase[-3:]
                txt = " ".join(recent)
                if len(self.app.phrase) > 3:
                    txt = f"... +{len(self.app.phrase)-3} {txt}"
                self.display.text = txt
            with self.display.canvas.before:
                Color(*get_color_from_hex(CORES["secundaria"]))
                self.display_rect = Rectangle(pos=self.display.pos, size=self.display.size)

    def switch_tab(self, tab):
        self.app.current_tab = tab
        for key, btn in self.nav_buttons.items():
            cores_nav = {"comunicar": CORES["primaria"], "rotinas": CORES["rotina_manha"],
                         "sobremim": CORES["pessoas"], "fichario": CORES["fichario"],
                         "sinto": CORES["sinto"], "perguntas": CORES["perguntas"], "config": CORES["config"]}
            btn.background_color = get_color_from_hex(CORES["primaria"] if key == tab else cores_nav.get(key, CORES["cinza"]))
        self.content_area.clear_widgets()
        if tab == "comunicar": self.show_comunicar()
        elif tab == "rotinas": self.show_rotinas()
        elif tab == "sobremim": self.show_sobre_mim()
        elif tab == "fichario": self.show_fichario()
        elif tab == "sinto": self.show_sinto()
        elif tab == "perguntas": self.show_perguntas()
        elif tab == "config": self.show_config()

    def show_comunicar(self):
        grid = GridLayout(cols=2, spacing=dp(10), size_hint_y=None)
        grid.bind(minimum_height=grid.setter("height"))
        for key, data in CATEGORIAS.items():
            btn = Button(text=f"[b]{data['titulo']}[/b]", markup=True, size_hint_y=None, height=dp(80),
                         background_color=get_color_from_hex(data["cor"]),
                         color=get_color_from_hex(CORES["branco"]), font_size=sp(18))
            btn.bind(on_press=lambda x, k=key: self.show_categoria(k))
            grid.add_widget(btn)
        btn_avancado = Button(text="[b]MONTAR FRASE[/b]", markup=True, size_hint_y=None, height=dp(80),
                              background_color=get_color_from_hex("#FF6F00"),
                              color=get_color_from_hex(CORES["branco"]), font_size=sp(18))
        btn_avancado.bind(on_press=self.show_comunicar_avancado)
        grid.add_widget(btn_avancado)
        self.content_area.add_widget(grid)

    def show_categoria(self, cat):
        self.content_area.clear_widgets()
        data = CATEGORIAS[cat]
        title = Label(text=data["titulo"], font_size=sp(20), bold=True,
                      color=get_color_from_hex(CORES["branco"]), size_hint_y=None, height=dp(50))
        with title.canvas.before:
            Color(*get_color_from_hex(data["cor"]))
            title_rect = Rectangle(pos=title.pos, size=title.size)
        title.bind(pos=lambda obj, val: setattr(title_rect, "pos", val),
                   size=lambda obj, val: setattr(title_rect, "size", val))
        self.content_area.add_widget(title)
        btn_voltar = Button(text="< VOLTAR", size_hint_y=None, height=dp(45),
                            background_color=get_color_from_hex(CORES["cinza"]),
                            color=get_color_from_hex(CORES["branco"]), font_size=sp(14), bold=True)
        btn_voltar.bind(on_press=lambda x: self.switch_tab("comunicar"))
        self.content_area.add_widget(btn_voltar)
        grid = GridLayout(cols=2, spacing=dp(8), size_hint_y=None)
        grid.bind(minimum_height=grid.setter("height"))
        for label, phrase in data["itens"]:
            btn = Button(text=f"[b]{label}[/b]", markup=True, size_hint_y=None, height=dp(70),
                         background_color=get_color_from_hex(data["cor"]),
                         color=get_color_from_hex(CORES["branco"]), font_size=sp(16))
            btn.bind(on_press=lambda x, p=phrase: self.app.add_phrase(p))
            grid.add_widget(btn)
        self.content_area.add_widget(grid)

    def show_comunicar_avancado(self, instance=None):
        self.content_area.clear_widgets()
        sections = [("PRONOMES", "#2196F3", ["Eu", "Voce", "Ele", "Ela", "Nos", "Eles"]),
                    ("VERBOS", "#F44336", ["quero", "preciso", "gosto", "estou", "tenho", "vou", "posso"]),
                    ("OBJETOS", "#00BCD4", ["agua", "comida", "banho", "brincar", "TV", "celular", "tablet"]),
                    ("PESSOAS", "#E91E63", ["mae", "pai", "vovo", "vovo", "amigo", "professor"]),
                    ("CONECTIVOS", "#4CAF50", ["sim", "nao", "por favor", "obrigado", "desculpa", "mais"]),
                    ("LUGARES", "#FF9800", ["casa", "escola", "parque", "quarto", "banheiro", "cozinha"])]
        btn_voltar = Button(text="< VOLTAR", size_hint_y=None, height=dp(45),
                            background_color=get_color_from_hex(CORES["cinza"]),
                            color=get_color_from_hex(CORES["branco"]), font_size=sp(14), bold=True)
        btn_voltar.bind(on_press=lambda x: self.switch_tab("comunicar"))
        self.content_area.add_widget(btn_voltar)
        for title, color, words in sections:
            lbl = Label(text=title, font_size=sp(16), bold=True,
                        color=get_color_from_hex(CORES["primaria"]), size_hint_y=None, height=dp(35))
            self.content_area.add_widget(lbl)
            grid = GridLayout(cols=3, spacing=dp(5), size_hint_y=None)
            grid.bind(minimum_height=grid.setter("height"))
            for word in words:
                btn = Button(text=word.upper(), size_hint_y=None, height=dp(50),
                             background_color=get_color_from_hex(color),
                             color=get_color_from_hex(CORES["branco"]), font_size=sp(14), bold=True)
                btn.bind(on_press=lambda x, w=word: self.app.add_phrase(w))
                grid.add_widget(btn)
            self.content_area.add_widget(grid)


    def show_rotinas(self):
        total_items = sum(len(r["itens"]) for r in ROTINAS.values())
        total_done = sum(len(v) for v in self.app.rotinas_done.values())
        progress = int((total_done / total_items) * 100) if total_items > 0 else 0
        lbl_progress = Label(text=f"Progresso: {total_done}/{total_items} ({progress}%)",
                             font_size=sp(14), bold=True,
                             color=get_color_from_hex(CORES["primaria"]),
                             size_hint_y=None, height=dp(30))
        self.content_area.add_widget(lbl_progress)
        pb = ProgressBar(max=100, value=progress, size_hint_y=None, height=dp(20))
        self.content_area.add_widget(pb)
        btn_reset = Button(text="REINICIAR ROTINAS", size_hint_y=None, height=dp(45),
                           background_color=get_color_from_hex(CORES["alerta"]),
                           color=get_color_from_hex(CORES["branco"]), font_size=sp(14), bold=True)
        btn_reset.bind(on_press=self.reset_rotinas)
        self.content_area.add_widget(btn_reset)
        for period, data in ROTINAS.items():
            title = Label(text=data["titulo"], font_size=sp(16), bold=True,
                        color=get_color_from_hex(CORES["branco"]), size_hint_y=None, height=dp(40))
            with title.canvas.before:
                Color(*get_color_from_hex(data["cor"]))
                title_rect = Rectangle(pos=title.pos, size=title.size)
            title.bind(pos=lambda obj, val, rect=title_rect: setattr(rect, "pos", val),
                       size=lambda obj, val, rect=title_rect: setattr(rect, "size", val))
            self.content_area.add_widget(title)
            for idx, (label, phrase) in enumerate(data["itens"]):
                is_done = idx in self.app.rotinas_done[period]
                btn = Button(text=f"{'[s]' if is_done else ''}{label}{'[/s]' if is_done else ''}",
                             markup=True, size_hint_y=None, height=dp(55),
                             background_color=get_color_from_hex(CORES["sucesso"] if is_done else data["cor"]),
                             color=get_color_from_hex(CORES["branco"]), font_size=sp(14), bold=True)
                btn.bind(on_press=lambda x, p=period, i=idx, ph=phrase: self.toggle_rotina(p, i, ph))
                self.content_area.add_widget(btn)

    def toggle_rotina(self, period, idx, phrase):
        if idx in self.app.rotinas_done[period]:
            self.app.rotinas_done[period].remove(idx)
        else:
            self.app.rotinas_done[period].append(idx)
            self.app.add_phrase(phrase)
        self.app.storage.save_rotinas(self.app.user_data.get("nome", "guest"), self.app.rotinas_done)
        self.content_area.clear_widgets()
        self.show_rotinas()

    def reset_rotinas(self, instance):
        self.app.rotinas_done = {"manha": [], "tarde": [], "noite": []}
        self.app.storage.save_rotinas(self.app.user_data.get("nome", "guest"), self.app.rotinas_done)
        self.app.speak("Rotinas reiniciadas")
        self.content_area.clear_widgets()
        self.show_rotinas()

    def show_sobre_mim(self):
        infos = [("Comida Favorita", "comidaFavorita"), ("Desenho Favorito", "desenhoFavorito"),
                 ("Cor Favorita", "corFavorita"), ("Brinquedo Favorito", "brinquedoFavorito"),
                 ("Musica Favorita", "musicaFavorita"), ("Atividade Favorita", "atividadeFavorita"),
                 ("Roupa Favorita", "roupaFavorita"), ("Animal Favorito", "animalFavorito"),
                 ("Lugar Favorito", "lugarFavorito"), ("Jogo Favorito", "jogoFavorito"),
                 ("Personagem Favorito", "personagemFavorito"), ("Bebida Favorita", "bebidaFavorita")]
        for label, key in infos:
            valor = self.app.user_data.get(key, "Nao informado")
            box = BoxLayout(size_hint_y=None, height=dp(80), padding=dp(5))
            info_layout = BoxLayout(orientation="vertical")
            lbl = Label(text=f"[b]{label}[/b]", markup=True, font_size=sp(14),
                        color=get_color_from_hex(CORES["primaria"]), halign="left", size_hint_y=0.5)
            lbl.bind(size=lbl.setter("text_size"))
            val_lbl = Label(text=valor, font_size=sp(16), color=get_color_from_hex(CORES["texto"]),
                            halign="left", size_hint_y=0.5)
            val_lbl.bind(size=val_lbl.setter("text_size"))
            info_layout.add_widget(lbl)
            info_layout.add_widget(val_lbl)
            btn_falar = Button(text="FALAR", size_hint_x=None, width=dp(80),
                               background_color=get_color_from_hex(CORES["quero"]),
                               color=get_color_from_hex(CORES["branco"]), font_size=sp(12), bold=True)
            btn_falar.bind(on_press=lambda x, l=label, v=valor: self.app.add_phrase(f"{l}: {v}"))
            box.add_widget(info_layout)
            box.add_widget(btn_falar)
            self.content_area.add_widget(box)

    def show_fichario(self):
        sections = [
            ("Dados Pessoais", [("Nome", "nome"), ("Idade", "idade"), ("Genero", "genero"),
                                ("Responsavel", "responsavel"), ("Telefone", "telefone")], CORES["primaria"]),
            ("Preferencias", [("Comida", "comidaFavorita"), ("Desenho", "desenhoFavorito"),
                              ("Cor", "corFavorita"), ("Brinquedo", "brinquedoFavorito"),
                              ("Musica", "musicaFavorita"), ("Atividade", "atividadeFavorita"),
                              ("Roupa", "roupaFavorita"), ("Animal", "animalFavorito"),
                              ("Lugar", "lugarFavorito"), ("Jogo", "jogoFavorito"),
                              ("Personagem", "personagemFavorito"), ("Bebida", "bebidaFavorita")], CORES["fichario"]),
            ("Informacoes Medicas", [("Contato Emergencia", "contatoEmergencia"), ("Medicamentos", "medicamentos"),
                                      ("Alergias", "alergias"), ("Condicoes", "condicoesMedicas"),
                                      ("Medico", "medico"), ("Convenio", "convenio"),
                                      ("Tipo Sanguineo", "tipoSanguineo")], CORES["perigo"]),
            ("Escola", [("Escola", "escola"), ("Serie", "serie"),
                        ("Professor", "professor"), ("Amigos", "amigos")], CORES["quero"]),
        ]
        for sec_title, fields, color in sections:
            title = Label(text=sec_title, font_size=sp(16), bold=True,
                          color=get_color_from_hex(CORES["branco"]), size_hint_y=None, height=dp(35))
            with title.canvas.before:
                Color(*get_color_from_hex(color))
                title_rect = Rectangle(pos=title.pos, size=title.size)
            title.bind(pos=lambda obj, val, rect=title_rect: setattr(rect, "pos", val),
                       size=lambda obj, val, rect=title_rect: setattr(rect, "size", val))
            self.content_area.add_widget(title)
            for label, key in fields:
                valor = self.app.user_data.get(key, "---")
                row = BoxLayout(size_hint_y=None, height=dp(35))
                lbl = Label(text=f"{label}:", font_size=sp(13), color=get_color_from_hex(CORES["cinza"]),
                            halign="left", size_hint_x=0.4)
                lbl.bind(size=lbl.setter("text_size"))
                val = Label(text=str(valor), font_size=sp(13), color=get_color_from_hex(CORES["texto"]),
                            halign="right", size_hint_x=0.6)
                val.bind(size=val.setter("text_size"))
                row.add_widget(lbl)
                row.add_widget(val)
                self.content_area.add_widget(row)
        btn_editar = Button(text="EDITAR FICHARIO", size_hint_y=None, height=dp(50),
                            background_color=get_color_from_hex(CORES["alerta"]),
                            color=get_color_from_hex(CORES["branco"]), font_size=sp(16), bold=True)
        btn_editar.bind(on_press=lambda x: self.switch_tab("config"))
        self.content_area.add_widget(btn_editar)
        btn_sair = Button(text="SAIR / TROCAR USUARIO", size_hint_y=None, height=dp(50),
                          background_color=get_color_from_hex(CORES["perigo"]),
                          color=get_color_from_hex(CORES["branco"]), font_size=sp(16), bold=True)
        btn_sair.bind(on_press=self.logout)
        self.content_area.add_widget(btn_sair)

    def show_sinto(self):
        grid = GridLayout(cols=2, spacing=dp(10), size_hint_y=None)
        grid.bind(minimum_height=grid.setter("height"))
        for label, phrase, color in SENTIMENTOS:
            btn = Button(text=f"[b]{label}[/b]", markup=True, size_hint_y=None, height=dp(80),
                         background_color=get_color_from_hex(color),
                         color=get_color_from_hex(CORES["branco"]), font_size=sp(16))
            btn.bind(on_press=lambda x, p=phrase: self.app.add_phrase(p))
            grid.add_widget(btn)
        btn_dor = Button(text="[b]ESTOU COM DOR[/b]", markup=True, size_hint_y=None, height=dp(80),
                         background_color=get_color_from_hex(CORES["perigo"]),
                         color=get_color_from_hex(CORES["branco"]), font_size=sp(16))
        btn_dor.bind(on_press=self.show_dores)
        grid.add_widget(btn_dor)
        self.content_area.add_widget(grid)

    def show_dores(self, instance=None):
        self.content_area.clear_widgets()
        btn_voltar = Button(text="< VOLTAR", size_hint_y=None, height=dp(45),
                            background_color=get_color_from_hex(CORES["cinza"]),
                            color=get_color_from_hex(CORES["branco"]), font_size=sp(14), bold=True)
        btn_voltar.bind(on_press=lambda x: self.switch_tab("sinto"))
        self.content_area.add_widget(btn_voltar)
        title = Label(text="ONDE ESTA DOENDO?", font_size=sp(18), bold=True,
                      color=get_color_from_hex(CORES["perigo"]), size_hint_y=None, height=dp(40))
        self.content_area.add_widget(title)
        grid = GridLayout(cols=2, spacing=dp(8), size_hint_y=None)
        grid.bind(minimum_height=grid.setter("height"))
        for label, phrase in DORES:
            btn = Button(text=f"[b]{label}[/b]", markup=True, size_hint_y=None, height=dp(70),
                         background_color=get_color_from_hex(CORES["perigo"]),
                         color=get_color_from_hex(CORES["branco"]), font_size=sp(14))
            btn.bind(on_press=lambda x, p=phrase: self.app.add_phrase(p))
            grid.add_widget(btn)
        self.content_area.add_widget(grid)
        lbl_int = Label(text="INTENSIDADE DA DOR", font_size=sp(16), bold=True,
                        color=get_color_from_hex(CORES["primaria"]), size_hint_y=None, height=dp(35))
        self.content_area.add_widget(lbl_int)
        box_int = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(5))
        for num, phrase, color in NIVEIS_DOR:
            btn = Button(text=num, background_color=get_color_from_hex(color),
                         color=get_color_from_hex(CORES["branco"]), font_size=sp(20), bold=True)
            btn.bind(on_press=lambda x, p=phrase: self.app.add_phrase(p))
            box_int.add_widget(btn)
        self.content_area.add_widget(box_int)

    def show_perguntas(self):
        grid = GridLayout(cols=2, spacing=dp(10), size_hint_y=None)
        grid.bind(minimum_height=grid.setter("height"))
        for key, data in PERGUNTAS.items():
            btn = Button(text=f"[b]{data['titulo']}[/b]", markup=True, size_hint_y=None, height=dp(80),
                         background_color=get_color_from_hex(data["cor"]),
                         color=get_color_from_hex(CORES["branco"]), font_size=sp(14))
            btn.bind(on_press=lambda x, k=key: self.show_pergunta_categoria(k))
            grid.add_widget(btn)
        self.content_area.add_widget(grid)

    def show_pergunta_categoria(self, cat):
        self.content_area.clear_widgets()
        data = PERGUNTAS[cat]
        btn_voltar = Button(text="< VOLTAR", size_hint_y=None, height=dp(45),
                            background_color=get_color_from_hex(CORES["cinza"]),
                            color=get_color_from_hex(CORES["branco"]), font_size=sp(14), bold=True)
        btn_voltar.bind(on_press=lambda x: self.switch_tab("perguntas"))
        self.content_area.add_widget(btn_voltar)
        title = Label(text=data["titulo"], font_size=sp(18), bold=True,
                      color=get_color_from_hex(CORES["branco"]), size_hint_y=None, height=dp(45))
        with title.canvas.before:
            Color(*get_color_from_hex(data["cor"]))
            title_rect = Rectangle(pos=title.pos, size=title.size)
        title.bind(pos=lambda obj, val, rect=title_rect: setattr(rect, "pos", val),
                   size=lambda obj, val, rect=title_rect: setattr(rect, "size", val))
        self.content_area.add_widget(title)
        grid = GridLayout(cols=2, spacing=dp(8), size_hint_y=None)
        grid.bind(minimum_height=grid.setter("height"))
        for label, phrase in data["itens"]:
            btn = Button(text=f"[b]{label}[/b]", markup=True, size_hint_y=None, height=dp(70),
                         background_color=get_color_from_hex(data["cor"]),
                         color=get_color_from_hex(CORES["branco"]), font_size=sp(13))
            btn.bind(on_press=lambda x, p=phrase: self.app.add_phrase(p))
            grid.add_widget(btn)
        self.content_area.add_widget(grid)


    def show_config(self):
        fields = [
            ("Dados Pessoais", [("cfg-nome", "Nome", "nome"), ("cfg-idade", "Idade", "idade"),
                                ("cfg-responsavel", "Responsavel", "responsavel"),
                                ("cfg-telefone", "Telefone", "telefone")]),
            ("Preferencias", [("cfg-comida", "Comida Favorita", "comidaFavorita"),
                              ("cfg-desenho", "Desenho Favorito", "desenhoFavorito"),
                              ("cfg-cor", "Cor Favorita", "corFavorita"),
                              ("cfg-brinquedo", "Brinquedo Favorito", "brinquedoFavorito"),
                              ("cfg-musica", "Musica Favorita", "musicaFavorita"),
                              ("cfg-atividade", "Atividade Favorita", "atividadeFavorita"),
                              ("cfg-roupa", "Roupa Favorita", "roupaFavorita"),
                              ("cfg-animal", "Animal Favorito", "animalFavorito"),
                              ("cfg-lugar", "Lugar Favorito", "lugarFavorito"),
                              ("cfg-jogo", "Jogo Favorito", "jogoFavorito"),
                              ("cfg-personagem", "Personagem Favorito", "personagemFavorito"),
                              ("cfg-bebida", "Bebida Favorita", "bebidaFavorita")]),
            ("Informacoes Medicas", [("cfg-contato", "Contato Emergencia", "contatoEmergencia"),
                                       ("cfg-medicamentos", "Medicamentos", "medicamentos"),
                                       ("cfg-alergias", "Alergias", "alergias"),
                                       ("cfg-condicoes", "Condicoes Medicas", "condicoesMedicas"),
                                       ("cfg-medico", "Medico", "medico"),
                                       ("cfg-convenio", "Convenio", "convenio"),
                                       ("cfg-sangue", "Tipo Sanguineo", "tipoSanguineo")]),
            ("Escola", [("cfg-escola", "Escola", "escola"), ("cfg-serie", "Serie", "serie"),
                        ("cfg-professor", "Professor", "professor"), ("cfg-amigos", "Amigos", "amigos")]),
            ("Outras", [("cfg-outras", "Outras Informacoes", "outrasInfo")]),
        ]
        self.config_inputs = {}
        for sec_title, sec_fields in fields:
            lbl = Label(text=sec_title, font_size=sp(16), bold=True,
                        color=get_color_from_hex(CORES["primaria"]), size_hint_y=None, height=dp(35))
            self.content_area.add_widget(lbl)
            for cid, label, key in sec_fields:
                lbl_inp = Label(text=label, font_size=sp(13), bold=True,
                                color=get_color_from_hex(CORES["cinza"]), size_hint_y=None, height=dp(25))
                self.content_area.add_widget(lbl_inp)
                if key in ["medicamentos", "alergias", "condicoesMedicas", "amigos", "outrasInfo"]:
                    inp = TextInput(text=self.app.user_data.get(key, ""), multiline=True,
                                    size_hint_y=None, height=dp(80), font_size=sp(15))
                else:
                    inp = TextInput(text=self.app.user_data.get(key, ""), multiline=False,
                                    size_hint_y=None, height=dp(45), font_size=sp(15))
                self.config_inputs[cid] = (inp, key)
                self.content_area.add_widget(inp)

        # Audio config
        lbl_audio = Label(text="Configuracoes de Audio", font_size=sp(16), bold=True,
                          color=get_color_from_hex(CORES["primaria"]), size_hint_y=None, height=dp(35))
        self.content_area.add_widget(lbl_audio)

        lbl_rate = Label(text=f"Velocidade: {self.app.tts_config.get('rate', 150)}", font_size=sp(14),
                         color=get_color_from_hex(CORES["primaria"]), size_hint_y=None, height=dp(25))
        self.content_area.add_widget(lbl_rate)
        slider_rate = Slider(min=50, max=300, value=self.app.tts_config.get("rate", 150),
                             size_hint_y=None, height=dp(40))
        slider_rate.bind(value=lambda obj, val: lbl_rate.setter("text")(lbl_rate, f"Velocidade: {int(val)}"))
        self.config_inputs["cfg-rate"] = (slider_rate, "rate")
        self.content_area.add_widget(slider_rate)

        lbl_vol = Label(text=f"Volume: {int(self.app.tts_config.get('volume', 1.0)*100)}%", font_size=sp(14),
                        color=get_color_from_hex(CORES["primaria"]), size_hint_y=None, height=dp(25))
        self.content_area.add_widget(lbl_vol)
        slider_vol = Slider(min=0, max=1, value=self.app.tts_config.get("volume", 1.0),
                            size_hint_y=None, height=dp(40))
        slider_vol.bind(value=lambda obj, val: lbl_vol.setter("text")(lbl_vol, f"Volume: {int(val*100)}%"))
        self.config_inputs["cfg-volume"] = (slider_vol, "volume")
        self.content_area.add_widget(slider_vol)

        btn_testar = Button(text="TESTAR AUDIO", size_hint_y=None, height=dp(50),
                            background_color=get_color_from_hex(CORES["quero"]),
                            color=get_color_from_hex(CORES["branco"]), font_size=sp(16), bold=True)
        btn_testar.bind(on_press=self.testar_audio)
        self.content_area.add_widget(btn_testar)

        btn_salvar = Button(text="SALVAR TUDO", size_hint_y=None, height=dp(60),
                            background_color=get_color_from_hex(CORES["sucesso"]),
                            color=get_color_from_hex(CORES["branco"]), font_size=sp(18), bold=True)
        btn_salvar.bind(on_press=self.salvar_config)
        self.content_area.add_widget(btn_salvar)

    def testar_audio(self, instance):
        rate = self.config_inputs.get("cfg-rate", (None, None))[0]
        vol = self.config_inputs.get("cfg-volume", (None, None))[0]
        if rate:
            self.app.tts_config["rate"] = int(rate.value)
        if vol:
            self.app.tts_config["volume"] = vol.value
        self.app.speak("Teste de audio do Falamigo")

    def salvar_config(self, instance):
        for cid, (widget, key) in self.config_inputs.items():
            if cid in ["cfg-rate", "cfg-volume"]:
                if key == "rate":
                    self.app.tts_config["rate"] = int(widget.value)
                elif key == "volume":
                    self.app.tts_config["volume"] = widget.value
            else:
                self.app.user_data[key] = widget.text
        self.app.storage.save_config(self.app.tts_config)
        self.app.save_user_data()
        self.app.speak("Informacoes salvas com sucesso")
        popup = Popup(title="Sucesso", content=Label(text="Dados salvos!", font_size=sp(16)),
                      size_hint=(0.8, 0.3), auto_dismiss=True)
        popup.open()

    def show_emergency(self, instance):
        box = BoxLayout(orientation="vertical", spacing=dp(10), padding=dp(20))
        lbl = Label(text="EMERGENCIA", font_size=sp(22), bold=True,
                    color=get_color_from_hex(CORES["perigo"]))
        box.add_widget(lbl)
        info = ""
        if self.app.user_data.get("nome"):
            info += f"Nome: {self.app.user_data['nome']}\n"
        if self.app.user_data.get("contatoEmergencia"):
            info += f"Contato: {self.app.user_data['contatoEmergencia']}\n"
        if self.app.user_data.get("medicamentos"):
            info += f"Medicamentos: {self.app.user_data['medicamentos']}\n"
        if self.app.user_data.get("alergias"):
            info += f"Alergias: {self.app.user_data['alergias']}\n"
        lbl_info = Label(text=info or "Nenhuma informacao cadastrada", font_size=sp(14),
                         color=get_color_from_hex(CORES["texto"]))
        box.add_widget(lbl_info)

        def emergency_type(tipo):
            msgs = {"crise": "ESTOU TENDO UMA CRISE! PRECISO DE AJUDA IMEDIATA!",
                    "dor": "ESTOU COM MUITA DOR! PRECISO DE AJUDA AGORA!",
                    "ajuda": "PRECISO DE AJUDA URGENTE!"}
            msg = msgs.get(tipo, "PRECISO DE AJUDA!")
            full = msg
            if self.app.user_data.get("nome"):
                full += f" Meu nome e {self.app.user_data['nome']}."
            if self.app.user_data.get("contatoEmergencia"):
                full += f" Contato: {self.app.user_data['contatoEmergencia']}."
            self.app.add_phrase(full)
            self.app.vibrate([500, 200, 500, 200, 500])
            popup.dismiss()

        btn_crise = Button(text="ESTOU TENDO UMA CRISE", background_color=get_color_from_hex(CORES["alerta"]),
                           color=get_color_from_hex(CORES["branco"]), font_size=sp(14), bold=True)
        btn_crise.bind(on_press=lambda x: emergency_type("crise"))
        box.add_widget(btn_crise)
        btn_dor = Button(text="ESTOU COM MUITA DOR", background_color=get_color_from_hex(CORES["perigo"]),
                         color=get_color_from_hex(CORES["branco"]), font_size=sp(14), bold=True)
        btn_dor.bind(on_press=lambda x: emergency_type("dor"))
        box.add_widget(btn_dor)
        btn_ajuda = Button(text="PRECISO DE AJUDA", background_color=get_color_from_hex(CORES["primaria"]),
                           color=get_color_from_hex(CORES["branco"]), font_size=sp(14), bold=True)
        btn_ajuda.bind(on_press=lambda x: emergency_type("ajuda"))
        box.add_widget(btn_ajuda)

        popup = Popup(title="SOS", content=box, size_hint=(0.9, 0.8), auto_dismiss=True)
        popup.open()

    def logout(self, instance):
        self.app.sm.current = "login"
        self.app.current_user = None
        self.app.phrase = []
        login_screen = self.app.sm.get_screen("login")
        login_screen.show_tab("entrar")


if __name__ == "__main__":
    FalamigoApp().run()
