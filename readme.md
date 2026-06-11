📦 Sistema de Controle de Estoque

📌 Visão Geral
O Sistema de Controle de Estoque é uma aplicação desktop desenvolvida em Python, com interface moderna utilizando CustomTkinter.

O sistema permite gerenciar produtos, controlar níveis de estoque e acompanhar movimentações de forma simples, rápida e eficiente.

---

🚀 Funcionalidades

- Cadastro de produtos
- Edição de produtos
- Exclusão de produtos
- Controle de estoque mínimo
- Busca dinâmica por nome, categoria e fornecedor
- Alerta automático de estoque baixo
- Dashboard com gráfico de movimentação
- Exportação de dados para Excel

---

🛠️ Tecnologias Utilizadas

- Python
- CustomTkinter
- SQLite (banco local)
- Matplotlib

---

⚙️ Instalação (Usuário Final)

1. Execute o arquivo:
   setup.exe

2. Clique em "Avançar"

3. Finalize a instalação

4. Abra o sistema pelo Menu Iniciar ou Área de Trabalho

---

⚠️ Aviso do Windows

Ao executar o instalador ou o sistema, pode aparecer a mensagem:

"Windows protegeu seu PC"

Neste caso:

- Clique em "Mais informações"
- Clique em "Executar mesmo assim"

Isso é normal para aplicações não assinadas.

---

💾 Banco de Dados

O banco de dados é criado automaticamente no caminho:

C:\Users\SEU_USUARIO\AppData\Local\ControleEstoque\estoque.db

- Não é necessário configurar
- Cada usuário possui seu próprio banco de dados

---

🧑‍💻 Execução em Desenvolvimento

Instalar dependências:

pip install customtkinter matplotlib

Rodar o sistema:

python main.py

---

📦 Gerar Executável (.exe)

python -m PyInstaller --onefile --windowed main.py

O executável será gerado em:

dist\main.exe

---

🧰 Criar Instalador (Inno Setup)

Utilize o seguinte script no arquivo installer.iss:

[Setup]
AppName=Controle de Estoque
AppVersion=1.0
DefaultDirName={pf}\ControleEstoque
DefaultGroupName=ControleEstoque
OutputDir=output
OutputBaseFilename=setup

[Files]
Source: "dist\main.exe"; DestDir: "{app}"

[Icons]
Name: "{group}\Controle de Estoque"; Filename: "{app}\main.exe"
Name: "{commondesktop}\Controle de Estoque"; Filename: "{app}\main.exe"

Resultado:

output\setup.exe

---

📤 Distribuição

O sistema pode ser compartilhado via:

- WhatsApp
- Email
- Google Drive
- Pendrive

Recomenda-se enviar em formato .zip.

---

🎯 Boas Práticas

- Sempre gerar um novo .exe após alterações no código
- Recriar o instalador após atualizar o executável
- Nunca salvar dados dentro da pasta "Program Files"

---

👨‍💻 Autores

Kauan Machado Vieira  
Davi de Almeida Atab  
Vinnicius Franco Rodrigues  
Sulivan Matheus Leal Tibes  
