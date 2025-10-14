# 👻 GHOST OPTIMIZER - CS2

### Otimização Profissional para Counter-Strike 2

---

## 📋 ÍNDICE
- [Instalação](#instalação)
- [Como Usar](#como-usar)
- [Estrutura de Arquivos](#estrutura-de-arquivos)
- [Criar Executável](#criar-executável)
- [Funcionalidades](#funcionalidades)
- [Troubleshooting](#troubleshooting)

---

## 🚀 INSTALAÇÃO

### Pré-requisitos
- Windows 10/11
- Python 3.8 ou superior
- Privilégios de Administrador

### Passo 1: Instalar Python
1. Baixe Python em: https://www.python.org/downloads/
2. **IMPORTANTE**: Marque "Add Python to PATH" durante instalação
3. Instale normalmente

### Passo 2: Configurar Projeto
1. Crie uma pasta chamada `GhostOptimizer` na área de trabalho
2. Abra o VSCode
3. Abra a pasta criada (File > Open Folder)
4. Crie os seguintes arquivos:

```
GhostOptimizer/
│
├── ghost_optimizer.py          (código principal - ARTIFACT 1)
├── requirements.txt            (dependências - ARTIFACT 2)
├── README.md                   (este arquivo - ARTIFACT 3)
└── icon.ico                    (opcional - ícone do programa)
```

### Passo 3: Instalar Dependências

Abra o Terminal no VSCode (Ctrl + ') e execute:

```bash
pip install -r requirements.txt
```

---

## 🎮 COMO USAR

### Executar pela primeira vez:

1. **Abra o Prompt de Comando como ADMINISTRADOR**
   - Pressione Windows + X
   - Clique em "Terminal (Admin)" ou "Prompt de Comando (Admin)"

2. **Navegue até a pasta do projeto**
   ```bash
   cd Desktop\GhostOptimizer
   ```

3. **Execute o programa**
   ```bash
   python ghost_optimizer.py
   ```

4. **Ativação**
   - Digite a key: `GPUSER`
   - Clique em ATIVAR

5. **Aplicar Otimizações**
   - Escolha o perfil desejado (Máximo FPS, Balanceado, etc)
   - Marque as otimizações que deseja aplicar
   - Clique em "🚀 APLICAR OTIMIZAÇÕES"

---

## 📦 CRIAR EXECUTÁVEL (.EXE)

Para distribuir sem precisar de Python instalado:

### 1. Instalar PyInstaller
```bash
pip install pyinstaller
```

### 2. Criar o executável
```bash
pyinstaller --onefile --windowed --icon=icon.ico --name="GhostOptimizer" ghost_optimizer.py
```

### 3. O executável estará em:
```
GhostOptimizer/dist/GhostOptimizer.exe
```

### 4. Para distribuir:
- Copie o arquivo `GhostOptimizer.exe` da pasta `dist/`
- Distribua para sua comunidade
- **IMPORTANTE**: Usuários devem executar como ADMINISTRADOR

---

## 🛠️ ESTRUTURA DE ARQUIVOS

```
GhostOptimizer/
│
├── ghost_optimizer.py          # Código principal
├── requirements.txt            # Bibliotecas necessárias
├── README.md                   # Este arquivo
├── icon.ico                    # Ícone (opcional)
│
├── ghost_config.json          # Criado automaticamente (ativação)
├── ghost_backup.json          # Criado automaticamente (backup)
├── ghost_profiles.json        # Criado automaticamente (perfis)
│
└── dist/                      # Pasta criada pelo PyInstaller
    └── GhostOptimizer.exe    # Executável final
```

---

## ✨ FUNCIONALIDADES

### 🎮 Otimizações de FPS
- **Boost de FPS**: Aplica launch options e configs otimizadas
- **Otimização GPU**: Configura NVIDIA/AMD para máximo desempenho
- **Prioridade Alta**: CS2 como processo prioritário
- **Game Mode**: Ativa modo jogo do Windows
- **Fullscreen Optimizado**: Remove delays de tela cheia
- **Cache de Shaders**: Otimiza renderização

### 🌐 Otimizações de Rede
- **TCP/IP Otimizado**: Reduz latência de rede
- **DNS Cloudflare**: 1.1.1.1 para velocidade
- **Desabilitar QoS**: Remove limitação de banda
- **Desabilitar Nagle**: Remove delay de pacotes

### ⚙️ Otimizações de Sistema
- **Limpeza Temporários**: Remove arquivos desnecessários
- **Desabilitar Serviços**: Apenas serviços seguros e inúteis
- **Plano de Energia**: Alto desempenho
- **Efeitos Visuais**: Reduz animações do Windows

### 🔒 Segurança
- **Sistema de Backup**: Backup automático antes de aplicar
- **Rollback**: Restaurar configurações anteriores
- **Verificação de Admin**: Exige privilégios corretos

### 💾 Perfis
- **Máximo FPS**: Prioriza desempenho máximo
- **Balanceado**: Equilíbrio entre FPS e qualidade
- **Qualidade**: Mantém gráficos bonitos
- **Personalizado**: Você escolhe cada opção

---

## 🔧 TROUBLESHOOTING

### ❌ "Execute o programa como Administrador"
**Solução**: Clique com botão direito no executável > Executar como Administrador

### ❌ "ModuleNotFoundError: No module named 'customtkinter'"
**Solução**: 
```bash
pip install -r requirements.txt
```

### ❌ "tkinter not found"
**Solução** (Windows):
- Reinstale Python marcando "tcl/tk and IDLE"

### ❌ Programa não abre
**Solução**:
1. Verifique se Python está instalado: `python --version`
2. Execute pelo terminal para ver erros: `python ghost_optimizer.py`
3. Certifique-se de estar como Administrador

### ❌ CS2 não detectado
**Solução**:
- Execute o CS2 antes de aplicar otimizações
- Algumas otimizações funcionam mesmo com CS2 fechado

### ❌ Erro ao criar executável
**Solução**:
```bash
pip install --upgrade pyinstaller
pyinstaller --clean --onefile --windowed ghost_optimizer.py
```

---

## 📝 NOTAS IMPORTANTES

### ⚠️ AVISOS
- **SEMPRE execute como Administrador**
- **Crie um ponto de restauração do Windows antes** (opcional, mas recomendado)
- **Feche antivírus** se ele bloquear (falso positivo comum em otimizadores)
- **Reinicie o CS2** após aplicar otimizações

### 🎯 RECOMENDAÇÕES
1. Use o perfil **Balanceado** primeiro
2. Teste por algumas partidas
3. Ajuste conforme necessário
4. Salve seu perfil personalizado

### 🔄 Sistema de Backup
- Backup criado automaticamente antes de cada otimização
- Para restaurar: clique em "↩️ Restaurar Backup"
- Backup salvo em `ghost_backup.json`

---

## 🆕 ATUALIZAÇÕES

### Como atualizar:
1. Clique em "🔄 Verificar Updates" no programa
2. Ou baixe a nova versão e substitua o arquivo

### Versão Atual: 1.0.0
- ✅ Sistema de ativação
- ✅ Interface gráfica profissional
- ✅ 10+ otimizações diferentes
- ✅ Sistema de perfis
- ✅ Backup automático
- ✅ Verificação de updates

---

## 🎨 PERSONALIZAÇÃO

### Mudar cores:
Edite em `ghost_optimizer.py`:
```python
# Linha ~15
fg_color="#00ff88"  # Cor principal (verde Ghost)
hover_color="#00cc66"  # Cor ao passar mouse
```

### Adicionar ícone:
1. Crie/baixe um arquivo `icon.ico`
2. Coloque na pasta do projeto
3. Ao criar executável, use:
```bash
pyinstaller --onefile --windowed --icon=icon.ico ghost_optimizer.py
```

---

## 📞 SUPORTE

### Problemas?
- Servidor Discord: **Ghost Optimizer**
- Key de ativação: `GPUSER`

### Reportar bugs:
1. Anote o erro exato
2. Informe sua versão do Windows
3. Compartilhe no Discord

---

## 📜 LICENÇA

© 2024 Ghost Optimizer - Todos os direitos reservados
Uso exclusivo para membros da comunidade Ghost Optimizer

---

## 🙏 CRÉDITOS

Desenvolvido com carinho para a comunidade Ghost Optimizer 👻

**Tecnologias usadas:**
- Python 3.x
- CustomTkinter (interface)
- PSUtil (monitoramento)
- Requests (updates)

---

## 🚀 QUICK START (Resumo Rápido)

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Executar (como Admin!)
python ghost_optimizer.py

# 3. Ativar com a key
GPUSER

# 4. Aplicar otimizações
# Escolha perfil > Marque opções > APLICAR
```

---

## 📊 COMPARATIVO DE PERFIS

| Perfil | FPS Médio | Qualidade | Uso RAM | Latência |
|--------|-----------|-----------|---------|----------|
| **Máximo FPS** | ⭐⭐⭐⭐⭐ | ⭐⭐ | Baixo | Mínima |
| **Balanceado** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Médio | Baixa |
| **Qualidade** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Alto | Normal |
| **Personalizado** | Você decide! | Você decide! | Variável | Variável |

---

**Bom jogo e muito FPS! 🎮🚀**