import customtkinter as ctk
import threading
import time

# Aparencia da aplicação
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

# ---Components---

class HomePage(ctk.CTkFrame):  # Página inicial (corrigido o nome da classe)
    def __init__(self, master):
        super().__init__(master)

        label = ctk.CTkLabel(self, text="Bem-vindo a Automação de testes do Salesforce", font=ctk.CTkFont(size=24, weight="bold"))
        label.pack(pady=40, padx=40)

        textlabel = ctk.CTkLabel(self, width=400, height=200,
        text="Essa ferramenta foi criada com o intuito de ajudar nos testes. \n\n"
             "Certifique-se que todos os campos estão preenchidos,"
             "e que todas as informações estão corretas antes de enviar a mensagem no grupo. \n\n"
             "Feedbacks: procurar Rogerin",
        justify="center", wraplength=400)
        textlabel.configure(state="disabled") # Bloqueia a edição
        textlabel.pack(pady=10, padx=20)

class AutomationPage(ctk.CTkFrame):  # Página onde a automação é realizada
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ---Frame Esquerda com SCROLL---
        form_frame = ctk.CTkScrollableFrame(self, label_text="Formulário de Mensagem")
        form_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)

        # ---Frame Direita---
        preview_frame = ctk.CTkFrame(self)
        preview_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=10)

        # ---Título(esquerda)---
        title_label = ctk.CTkLabel(form_frame, text="Preencha os campos abaixo:", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=20, padx=20)

        # ---Período do dia (Picklist)---
        periodo_label = ctk.CTkLabel(form_frame, text="Período do Dia:")
        periodo_label.pack(pady=(10, 0), padx=20, anchor="w")
        self.periodo_var = ctk.StringVar(value="Bom dia")
        periodo_menu = ctk.CTkOptionMenu(form_frame, values=["Bom dia", "Boa tarde", "Boa noite"],
                                         variable=self.periodo_var, command=self.update_preview)
        periodo_menu.pack(pady=5, padx=20, fill="x")

        # Número da Tarefa
        task_num_label = ctk.CTkLabel(form_frame, text="Número da Tarefa SF:")
        task_num_label.pack(pady=(10, 0), padx=20, anchor="w")
        self.task_num_entry = ctk.CTkEntry(form_frame, placeholder_text="Ex: 12345")
        self.task_num_entry.pack(pady=5, padx=20, fill="x")
        self.task_num_entry.bind("<KeyRelease>", self.update_preview)

        # Checkboxes
        checkbox_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        checkbox_frame.pack(pady=10, padx=20, fill="x")
        self.check_operacoes_var = ctk.StringVar(value="")
        self.check_docs_var = ctk.StringVar(value="")

        checkbox_operacoes = ctk.CTkCheckBox(checkbox_frame, text="Operações",
                                             variable=self.check_operacoes_var, onvalue="x", offvalue="",
                                             command=self.update_preview)
        checkbox_operacoes.pack(side="left", padx=5)

        checkbox_docs = ctk.CTkCheckBox(checkbox_frame, text="Documentações",
                                        variable=self.check_docs_var, onvalue="x", offvalue="",
                                        command=self.update_preview)
        checkbox_docs.pack(side="left", padx=5)

        # Título da task
        task_title_label = ctk.CTkLabel(form_frame, text="Título da Task:")
        task_title_label.pack(pady=(10, 0), padx=20, anchor="w")
        self.task_title_entry = ctk.CTkEntry(form_frame, placeholder_text="Título da Task")
        self.task_title_entry.pack(pady=5, padx=20, fill="x")
        self.task_title_entry.bind("<KeyRelease>", self.update_preview)

        # Objetivo
        objective_label = ctk.CTkLabel(form_frame, text="Objetivo:")
        objective_label.pack(pady=(10, 0), padx=20, anchor="w")
        self.objective_entry = ctk.CTkEntry(form_frame, height=20, placeholder_text="Objetivo da Task")
        self.objective_entry.pack(pady=5, padx=20, fill="x")
        self.objective_entry.bind("<KeyRelease>", self.update_preview)

        # Links
        planilha_label = ctk.CTkLabel(form_frame, text="Link da Planilha:")
        planilha_label.pack(pady=(10, 0), padx=20, anchor="w")
        self.planilha_entry = ctk.CTkEntry(form_frame, placeholder_text="https://...")
        self.planilha_entry.pack(pady=5, padx=20, fill="x")
        self.planilha_entry.bind("<KeyRelease>", self.update_preview)

        instrucao_label = ctk.CTkLabel(form_frame, text="Link da Instrução de Testes:")
        instrucao_label.pack(pady=(10, 0), padx=20, anchor="w")
        self.instrucao_entry = ctk.CTkEntry(form_frame, placeholder_text="https://...")
        self.instrucao_entry.pack(pady=5, padx=20, fill="x")
        self.instrucao_entry.bind("<KeyRelease>", self.update_preview)

        # --- BOTÃO E STATUS ---
        self.send_button = ctk.CTkButton(form_frame, text="Enviar Mensagem", command=self.start_automation_thread)
        self.send_button.pack(pady=20, padx=20)

        self.status_label = ctk.CTkLabel(form_frame, text="Pronto para começar.", anchor="w")
        self.status_label.pack(pady=10, padx=20, fill="x")

        # ---Preview da Mensagem---
        preview_label = ctk.CTkLabel(preview_frame, text="Preview da Mensagem", font=ctk.CTkFont(size=20, weight="bold"))
        preview_label.pack(pady=20, padx=20)

        self.preview_text = ctk.CTkTextbox(preview_frame, activate_scrollbars=True, state="disabled",
                                           wrap="word", font=("Arial", 14))
        self.preview_text.pack(pady=10, padx=20, fill="both", expand=True)

        self.update_preview(None)

    def update_preview(self, event=None):
        """Atualiza o texto de preview com os dados dos campos."""
        periodo = self.periodo_var.get()
        task_num = self.task_num_entry.get() or "[Número da Task]"
        task_title = self.task_title_entry.get() or "[Título da Task]"
        objetivo = self.objective_entry.get() or "[Objetivo]"
        link_planilha = self.planilha_entry.get() or "[Link Planilha]"
        link_instrucao = self.instrucao_entry.get() or "[Link Instrução]"
        operacoes = self.check_operacoes_var.get()
        docs = self.check_docs_var.get()

        mensagem = (
            f"{periodo}, pessoal! \n\n"
            f"Tarefa *SF-{task_num}* - LIBERADA PARA TESTES.\n\n"
            f"[{operacoes.capitalize()}] *Operações* \n"
            f"[{docs.capitalize()}] *Documentações*\n\n"
            f"*Título*: \n{task_title}\n\n"
            f"*Objetivo:* \n{objetivo}\n\n"
            f"*Link da Planilha:* \n{link_planilha}\n\n"
            f"*Link da Instrução de Testes:* \n{link_instrucao}\n\n"
            "Qualquer dúvida, por favor falem conosco."
        )

        self.preview_text.configure(state="normal")
        self.preview_text.delete("1.0", "end")
        self.preview_text.insert("1.0", mensagem)
        self.preview_text.configure(state="disabled")

    def start_automation_thread(self):
        self.send_button.configure(state="disabled", text="Enviando...")
        self.status_label.configure(text="Iniciando automação...")

        dados_para_automacao = {"mensagem": self.preview_text.get("1.0", "end-1c")}
        automation_thread = threading.Thread(target=self.run_backend_logic, args=(dados_para_automacao,))
        automation_thread.start()

    def run_backend_logic(self, dados):

        print(dados["mensagem"])

        try:
            self.status_label.configure(text="Abrindo navegador...")
            time.sleep(3)
            self.status_label.configure(text="Enviando mensagem no WhatsApp...")
            time.sleep(5)
            self.status_label.configure(text="Automação concluída com sucesso!", text_color="green")

        except Exception as e:
            print(f"Ocorreu um erro na automação: {e}")
            self.status_label.configure(text=f"Erro na automação: {e}", text_color="red")

        finally:
            self.send_button.configure(state="normal", text="Enviar Mensagem")


class SettingsPage(ctk.CTkFrame):
    """Página de configurações."""
    def __init__(self, master):
        super().__init__(master)
        
        label = ctk.CTkLabel(self, text="Configurações", font=ctk.CTkFont(size=24, weight="bold"))
        label.pack(pady=40, padx=40)

        appearance_label = ctk.CTkLabel(self, text="Tema da Aplicação:")
        appearance_label.pack(pady=10)

        appearance_menu = ctk.CTkOptionMenu(self, values=["Light", "Dark"],
                                           command=ctk.set_appearance_mode)
        appearance_menu.pack(pady=5)


# ---------- COMPONENTES DE LAYOUT ----------

class Header(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, height=60, fg_color=("gray90", "gray13"))
        self.pack_propagate(False)

        title_label = ctk.CTkLabel(self, text="Dashboard de Automação", font=ctk.CTkFont(size=22, weight="bold"))
        title_label.pack(side="left", padx=20)

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, show_frame_callback):
        super().__init__(master, width=220, fg_color=("gray85", "gray10"))
        self.pack_propagate(False)

        menu_label = ctk.CTkLabel(self, text="Menu", font=ctk.CTkFont(size=20, weight="bold"))
        menu_label.pack(pady=20, padx=10)
        
        home_button = ctk.CTkButton(self, text="Página Inicial", command=lambda: show_frame_callback("Home"))
        home_button.pack(pady=10, padx=20, fill="x")

        automation_button = ctk.CTkButton(self, text="Gerador de Mensagem", command=lambda: show_frame_callback("Automation"))
        automation_button.pack(pady=10, padx=20, fill="x")

        settings_button = ctk.CTkButton(self, text="Configurações", command=lambda: show_frame_callback("Settings"))
        settings_button.pack(pady=10, padx=20, fill="x")


# ---------- JANELA PRINCIPAL (APP) ----------

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1600x800")
        self.title("Dashboard de Automação")
        self.minsize(800, 800)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.header = Header(self)
        self.header.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.sidebar = Sidebar(self, self.show_frame)
        self.sidebar.grid(row=1, column=0, sticky="ns")

        self.main_content_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content_container.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)
        self.main_content_container.grid_rowconfigure(0, weight=1)
        self.main_content_container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (HomePage, AutomationPage, SettingsPage):
            page_name = F.__name__.replace("Page", "")
            frame = F(self.main_content_container)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Home")

    def show_frame(self, page_name):
        """Eleva o frame solicitado para o topo, tornando-o visível."""
        frame = self.frames[page_name]
        frame.tkraise()

# ---------- EXECUÇÃO ----------

if __name__ == "__main__":
    app = App()
    app.mainloop()
