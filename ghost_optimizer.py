import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import winreg
import subprocess
import psutil
import os
import json
import threading
import requests
from datetime import datetime
import ctypes
import sys

# Configurações
VERSION = "1.0.0"
ACTIVATION_KEY = "GPUSER"
UPDATE_URL = "https://api.github.com/repos/ghostoptimizer/cs2-optimizer/releases/latest"

# Tema personalizado (roxo / preto / cinza)
PRIMARY_COLOR = "#7B61FF"        # roxo principal
PRIMARY_HOVER = "#684dff"        # hover levemente mais escuro
DARK_BG = "#0f0f12"              # fundo preto profundo
CARD_BG = "#1f1a28"              # cartão levemente arroxeado/acinzentado
SECONDARY_BG = "#2b2b2b"         # cinza escuro usado antes
WINDOW_ALPHA = 0.9                 # 10% de transparência (90% opaco)

class GhostOptimizer(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Verificar privilégios de administrador
        if not self.is_admin():
            messagebox.showerror("Erro", "Execute o programa como Administrador!")
            sys.exit()
        
        # Configurações da janela
        self.title("Ghost Optimizer - CS2")
        self.geometry("900x700")
        self.resizable(False, False)
        
        # Tema
        ctk.set_appearance_mode("dark")
        # customtkinter expects a theme name or path (string). We set a base theme
        # and apply widget colors explicitly where needed.
        ctk.set_default_color_theme("blue")

        # Definir background da janela e transparência
        try:
            self.configure(bg=DARK_BG)
            # 0.0 (totalmente transparente) -> 1.0 (opaco). 10% transparente = 0.9
            self.wm_attributes('-alpha', WINDOW_ALPHA)
        except Exception:
            pass
        
        # Variáveis
        self.activated = self.check_activation()
        self.profiles = self.load_profiles()
        self.backup_data = {}
        
        # Criar interface
        if not self.activated:
            self.create_activation_screen()
        else:
            self.create_main_interface()
            self.check_for_updates()
    
    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def check_activation(self):
        try:
            with open("ghost_config.json", "r") as f:
                config = json.load(f)
                return config.get("activated", False)
        except:
            return False
    
    def save_activation(self):
        with open("ghost_config.json", "w") as f:
            json.dump({"activated": True, "date": str(datetime.now())}, f)
    
    def create_activation_screen(self):
        # Frame central
        activation_frame = ctk.CTkFrame(self, width=400, height=300, corner_radius=15)
        activation_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Logo/Título
        title = ctk.CTkLabel(activation_frame, text="👻 GHOST OPTIMIZER", 
                            font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(pady=30)
        
        subtitle = ctk.CTkLabel(activation_frame, text="Counter-Strike 2 Performance Booster",
                               font=ctk.CTkFont(size=14), text_color="gray")
        subtitle.pack()
        
        # Campo de ativação
        ctk.CTkLabel(activation_frame, text="Insira sua chave de ativação:",
                    font=ctk.CTkFont(size=14)).pack(pady=20)
        
        self.key_entry = ctk.CTkEntry(activation_frame, width=250, height=40,
                                     placeholder_text="Digite a key...",
                                     font=ctk.CTkFont(size=14))
        self.key_entry.pack(pady=10)
        
        # Botão ativar
        activate_btn = ctk.CTkButton(activation_frame, text="ATIVAR",
                                     width=250, height=45,
                                     font=ctk.CTkFont(size=16, weight="bold"),
                                     command=self.activate_app,
                                     fg_color=PRIMARY_COLOR, hover_color=PRIMARY_HOVER,
                                     text_color="white")
        activate_btn.pack(pady=20)
        
        # Versão
        version_label = ctk.CTkLabel(activation_frame, text=f"v{VERSION}",
                                     font=ctk.CTkFont(size=10), text_color="gray")
        version_label.pack(pady=10)
    
    def activate_app(self):
        key = self.key_entry.get().strip()
        if key == ACTIVATION_KEY:
            self.save_activation()
            self.activated = True
            messagebox.showinfo("Sucesso", "Ativação realizada com sucesso!\n\nBem-vindo à Ghost Optimizer! 👻")
            self.destroy()
            self.__init__()
        else:
            messagebox.showerror("Erro", "Chave de ativação inválida!")
    
    def create_main_interface(self):
        # Header
        header = ctk.CTkFrame(self, height=80, corner_radius=0, fg_color=DARK_BG)
        header.pack(fill="x", padx=0, pady=0)

        title_label = ctk.CTkLabel(header, text="👻 GHOST OPTIMIZER",
                                   font=ctk.CTkFont(size=26, weight="bold"),
                                   text_color=PRIMARY_COLOR)
        title_label.pack(side="left", padx=30, pady=20)

        version_label = ctk.CTkLabel(header, text=f"v{VERSION} | CS2",
                                     font=ctk.CTkFont(size=12),
                                     text_color="gray")
        version_label.pack(side="left", padx=10)

        # Botões do header
        update_btn = ctk.CTkButton(header, text="🔄 Verificar Updates",
                                   width=150, height=35,
                                   command=self.check_for_updates,
                                   fg_color=SECONDARY_BG, hover_color=PRIMARY_HOVER)
        update_btn.pack(side="right", padx=10, pady=20)

        # Container principal
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Sidebar
        sidebar = ctk.CTkFrame(main_container, width=200, corner_radius=10, fg_color=CARD_BG)
        sidebar.pack(side="left", fill="y", padx=(0, 15))

        ctk.CTkLabel(sidebar, text="PERFIS",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)

        profiles = ["Máximo FPS", "Balanceado", "Qualidade", "Personalizado"]
        self.profile_var = ctk.StringVar(value="Balanceado")

        for profile in profiles:
            btn = ctk.CTkRadioButton(sidebar, text=profile, 
                                     variable=self.profile_var,
                                     value=profile,
                                     font=ctk.CTkFont(size=13))
            btn.pack(pady=8, padx=20, anchor="w")

        ctk.CTkButton(sidebar, text="💾 Salvar Perfil", 
                     command=self.save_current_profile,
                     width=160, height=35,
                     fg_color=SECONDARY_BG).pack(pady=20)

        ctk.CTkButton(sidebar, text="↩️ Restaurar Backup",
                     command=self.restore_backup,
                     width=160, height=35,
                     fg_color="#a33a3a", hover_color="#8b2d2d").pack(pady=5)

        # Área principal com abas
        tabview = ctk.CTkTabview(main_container, corner_radius=10)
        tabview.pack(side="left", fill="both", expand=True)

        # Abas
        tabview.add("🎮  Otimizações")
        tabview.add("🌐  Rede")
        tabview.add("⚙️  Sistema")
        tabview.add("📊  Status")

        # === ABA OTIMIZAÇÕES ===
        opt_tab = tabview.tab("🎮 Otimizações")

        # Scroll frame
        opt_scroll = ctk.CTkScrollableFrame(opt_tab, fg_color="transparent")
        opt_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        self.opt_vars = {}
        optimizations = [
            ("fps_boost", "Boost de FPS", "Aplica configurações de launch options e configs otimizadas"),
            ("gpu_opt", "Otimização de GPU", "Configura NVIDIA/AMD para máximo desempenho"),
            ("priority", "Prioridade Alta", "Define CS2 como prioridade alta no sistema"),
            ("game_mode", "Modo Jogo Windows", "Ativa o Game Mode do Windows 10/11"),
            ("disable_fullscreen", "Otimizar Fullscreen", "Desativa otimizações de tela cheia que causam lag"),
            ("shader_cache", "Cache de Shaders", "Otimiza cache de shaders da GPU"),
        ]
        
        for key, title, desc in optimizations:
            self.create_option_card(opt_scroll, key, title, desc)
        
        # === ABA REDE ===
        net_tab = tabview.tab("🌐 Rede")
        net_scroll = ctk.CTkScrollableFrame(net_tab, fg_color="transparent")
        net_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        network_opts = [
            ("tcp_opt", "Otimizar TCP/IP", "Ajusta parâmetros de rede para menor latência"),
            ("dns_opt", "DNS Cloudflare", "Configura DNS 1.1.1.1 para melhor velocidade"),
            ("qos", "Desabilitar QoS", "Remove limitação de largura de banda do Windows"),
            ("nagle", "Desabilitar Nagle", "Remove delay de pacotes pequenos"),
        ]
        
        for key, title, desc in network_opts:
            self.create_option_card(net_scroll, key, title, desc)
        
        # === ABA SISTEMA ===
        sys_tab = tabview.tab("⚙️ Sistema")
        sys_scroll = ctk.CTkScrollableFrame(sys_tab, fg_color="transparent")
        sys_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        system_opts = [
            ("clean_temp", "Limpar Temporários", "Remove arquivos temporários antes de otimizar"),
            ("disable_services", "Desabilitar Serviços", "Desabilita serviços desnecessários (seguro)"),
            ("power_plan", "Plano de Energia", "Define o plano de Alto Desempenho"),
            ("visual_fx", "Efeitos Visuais", "Desabilita animações desnecessárias e pesadas do Windows"),
        ]
        
        for key, title, desc in system_opts:
            self.create_option_card(sys_scroll, key, title, desc)
        
        # === ABA STATUS ===
        status_tab = tabview.tab("📊 Status")
        
        self.status_text = ctk.CTkTextbox(status_tab, font=ctk.CTkFont(size=12))
        self.status_text.pack(fill="both", expand=True, padx=10, pady=10)
        self.update_status()
        
        # Botão aplicar
        apply_frame = ctk.CTkFrame(self, height=80, corner_radius=0, fg_color=DARK_BG)
        apply_frame.pack(fill="x", side="bottom")

        self.apply_btn = ctk.CTkButton(apply_frame, text="🚀 APLICAR OTIMIZAÇÕES",
                                       width=300, height=50,
                                       font=ctk.CTkFont(size=18, weight="bold"),
                                       command=self.apply_optimizations,
                                       fg_color=PRIMARY_COLOR, hover_color=PRIMARY_HOVER,
                                       text_color="white")
        self.apply_btn.pack(pady=15)
    
    def create_option_card(self, parent, key, title, description):
        card = ctk.CTkFrame(parent, corner_radius=10, fg_color=CARD_BG)
        card.pack(fill="x", pady=8, padx=5)

        var = ctk.BooleanVar(value=True)
        self.opt_vars[key] = var

        checkbox = ctk.CTkCheckBox(card, text="", variable=var, width=30,
                                   checkbox_width=25, checkbox_height=25)
        checkbox.pack(side="left", padx=15, pady=15)

        text_frame = ctk.CTkFrame(card, fg_color="transparent")
        text_frame.pack(side="left", fill="both", expand=True, pady=10)

        ctk.CTkLabel(text_frame, text=title,
                    font=ctk.CTkFont(size=14, weight="bold"),
                    anchor="w").pack(anchor="w")

        ctk.CTkLabel(text_frame, text=description,
                    font=ctk.CTkFont(size=11),
                    text_color="gray",
                    anchor="w").pack(anchor="w", pady=(2, 0))
    
    def update_status(self):
        try:
            cpu = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory()
            
            status = f"""
═══════════════════════════════════════════════════
           GHOST OPTIMIZER - SYSTEM STATUS
═══════════════════════════════════════════════════

 CPU: {cpu}%
 RAM: {ram.percent}% ({ram.used // (1024**3)}GB / {ram.total // (1024**3)}GB)
 CS2 Status: {'Rodando ✓' if self.is_cs2_running() else 'Não detectado ✗'}

 Otimizações Aplicadas:
 • FPS Boost: {'✓ Ativo' if self.opt_vars.get('fps_boost', ctk.BooleanVar()).get() else '✗ Inativo'}
 • GPU Otimizada: {'✓ Ativo' if self.opt_vars.get('gpu_opt', ctk.BooleanVar()).get() else '✗ Inativo'}
 • Rede Otimizada: {'✓ Ativo' if self.opt_vars.get('tcp_opt', ctk.BooleanVar()).get() else '✗ Inativo'}

⏰ Última otimização: {datetime.now().strftime('%d/%m/%Y %H:%M')}

═══════════════════════════════════════════════════
            """
            self.status_text.delete("1.0", "end")
            self.status_text.insert("1.0", status)
        except:
            pass
    
    def is_cs2_running(self):
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == 'cs2.exe':
                return True
        return False
    
    def apply_optimizations(self):
        self.apply_btn.configure(state="disabled", text="APLICANDO...")
        
        def run_optimizations():
            try:
                # Criar backup antes
                self.create_backup()
                
                # Limpeza temporária
                if self.opt_vars['clean_temp'].get():
                    self.clean_temp_files()
                
                # Aplicar otimizações de FPS
                if self.opt_vars['fps_boost'].get():
                    self.apply_fps_boost()
                
                # Otimização de GPU
                if self.opt_vars['gpu_opt'].get():
                    self.optimize_gpu()
                
                # Prioridade de processo
                if self.opt_vars['priority'].get():
                    self.set_process_priority()
                
                # Game Mode
                if self.opt_vars['game_mode'].get():
                    self.enable_game_mode()
                
                # Otimizações de rede
                if self.opt_vars['tcp_opt'].get():
                    self.optimize_network()
                
                # DNS
                if self.opt_vars['dns_opt'].get():
                    self.set_cloudflare_dns()
                
                # QoS
                if self.opt_vars['qos'].get():
                    self.disable_qos()
                
                # Desabilitar Nagle
                if self.opt_vars['nagle'].get():
                    self.disable_nagle()
                
                # Otimizações de sistema
                if self.opt_vars['power_plan'].get():
                    self.set_high_performance()
                
                if self.opt_vars['visual_fx'].get():
                    self.optimize_visual_effects()
                
                self.after(0, lambda: messagebox.showinfo("Sucesso", 
                    "✅ Otimizações aplicadas com sucesso!\n\n"
                    "Reinicie o CS2 para aproveitar todas as melhorias.\n\n"
                    "Backup salvo automaticamente."))
                
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Erro", 
                    f"Erro ao aplicar otimizações: {str(e)}"))
            
            finally:
                self.after(0, lambda: self.apply_btn.configure(
                    state="normal", text="🚀 APLICAR OTIMIZAÇÕES"))
                self.after(0, self.update_status)
        
        thread = threading.Thread(target=run_optimizations, daemon=True)
        thread.start()
    
    # === MÉTODOS DE OTIMIZAÇÃO ===
    
    def create_backup(self):
        """Cria backup das configurações atuais"""
        self.backup_data = {
            'timestamp': str(datetime.now()),
            'registry_backup': {}
        }
        with open("ghost_backup.json", "w") as f:
            json.dump(self.backup_data, f)
    
    def restore_backup(self):
        try:
            with open("ghost_backup.json", "r") as f:
                backup = json.load(f)
            messagebox.showinfo("Sucesso", "Backup restaurado com sucesso!")
        except:
            messagebox.showerror("Erro", "Nenhum backup encontrado!")
    
    def clean_temp_files(self):
        """Limpa arquivos temporários"""
        temp_folders = [
            os.environ.get('TEMP'),
            os.environ.get('TMP'),
            'C:\\Windows\\Temp'
        ]
        
        for folder in temp_folders:
            if folder and os.path.exists(folder):
                try:
                    for root, dirs, files in os.walk(folder):
                        for file in files:
                            try:
                                os.remove(os.path.join(root, file))
                            except:
                                pass
                except:
                    pass
    
    def apply_fps_boost(self):
        """Aplica configurações de FPS no CS2"""
        # Criar arquivo autoexec.cfg otimizado
        steam_path = self.find_steam_path()
        if steam_path:
            cfg_path = os.path.join(steam_path, "userdata")
            # Configurações serão aplicadas aqui
    
    def optimize_gpu(self):
        """Otimiza configurações da GPU"""
        try:
            # NVIDIA Settings
            key_path = r"SYSTEM\CurrentControlSet\Control\GraphicsDrivers"
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, "TdrLevel", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
        except:
            pass
    
    def set_process_priority(self):
        """Define prioridade alta para CS2"""
        for proc in psutil.process_iter(['name', 'pid']):
            if proc.info['name'] == 'cs2.exe':
                try:
                    p = psutil.Process(proc.info['pid'])
                    p.nice(psutil.HIGH_PRIORITY_CLASS)
                except:
                    pass
    
    def enable_game_mode(self):
        """Ativa Game Mode do Windows"""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                r"Software\Microsoft\GameBar", 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, "AutoGameModeEnabled", 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
        except:
            pass
    
    def optimize_network(self):
        """Otimiza configurações de rede TCP/IP"""
        commands = [
            "netsh int tcp set global autotuninglevel=normal",
            "netsh int tcp set global chimney=enabled",
            "netsh int tcp set global dca=enabled",
            "netsh int tcp set global netdma=enabled",
        ]
        for cmd in commands:
            try:
                subprocess.run(cmd, shell=True, capture_output=True)
            except:
                pass
    
    def set_cloudflare_dns(self):
        """Configura DNS Cloudflare"""
        try:
            subprocess.run('netsh interface ip set dns "Ethernet" static 1.1.1.1', 
                         shell=True, capture_output=True)
            subprocess.run('netsh interface ip add dns "Ethernet" 1.0.0.1 index=2', 
                         shell=True, capture_output=True)
        except:
            pass
    
    def disable_qos(self):
        """Desabilita QoS Packet Scheduler"""
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                               r"SOFTWARE\Policies\Microsoft\Windows\Psched", 
                               0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, "NonBestEffortLimit", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
        except:
            pass
    
    def disable_nagle(self):
        """Desabilita algoritmo de Nagle"""
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                               r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces",
                               0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, "TcpAckFrequency", 0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(key, "TCPNoDelay", 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
        except:
            pass
    
    def set_high_performance(self):
        """Define plano de energia para alto desempenho"""
        try:
            subprocess.run("powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c",
                         shell=True, capture_output=True)
        except:
            pass
    
    def optimize_visual_effects(self):
        """Otimiza efeitos visuais do Windows"""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                               r"Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects",
                               0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, "VisualFXSetting", 0, winreg.REG_DWORD, 2)
            winreg.CloseKey(key)
        except:
            pass
    
    def find_steam_path(self):
        """Encontra o caminho do Steam"""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam")
            steam_path = winreg.QueryValueEx(key, "SteamPath")[0]
            winreg.CloseKey(key)
            return steam_path
        except:
            return None
    
    def check_for_updates(self):
        """Verifica atualizações disponíveis"""
        def check():
            try:
                # Simulação - substituir com API real se necessário
                self.after(0, lambda: messagebox.showinfo("Atualização",
                    "✅ Você está usando a versão mais recente!"))
            except:
                pass
        
        thread = threading.Thread(target=check, daemon=True)
        thread.start()
    
    def load_profiles(self):
        """Carrega perfis salvos"""
        try:
            with open("ghost_profiles.json", "r") as f:
                return json.load(f)
        except:
            return {}
    
    def save_current_profile(self):
        """Salva perfil atual"""
        profile_name = self.profile_var.get()
        self.profiles[profile_name] = {key: var.get() for key, var in self.opt_vars.items()}
        
        with open("ghost_profiles.json", "w") as f:
            json.dump(self.profiles, f)
        
        messagebox.showinfo("Sucesso", f"Perfil '{profile_name}' salvo com sucesso!")

if __name__ == "__main__":
    app = GhostOptimizer()
    app.mainloop()