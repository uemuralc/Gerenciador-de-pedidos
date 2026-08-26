<img width="1919" height="1029" alt="image" src="https://github.com/user-attachments/assets/97ca24d2-2427-4b60-9dce-634edddb6ed5" />


# 📦 Painel de Gestão - Pedidos e Estoque

Um aplicativo leve, rápido e eficiente desenvolvido com Python e tecnologias Web para facilitar o controle de pedidos de clientes e o gerenciamento de matérias-primas no estoque. 

O sistema conta com um backend robusto em **Flask** estruturado em módulos (**Blueprints**), banco de dados **SQLite** e uma interface moderna e segura.

## ✨ Funcionalidades

* **📋 Fila de Pedidos:** Cadastro, edição, exclusão e alteração de status (Pendente, Em Andamento, Finalizado) de pedidos.
* **🛠️ Gestão de Estoque:** Controle de matérias-primas com botões de acesso rápido para adicionar ou subtrair quantidades e alertas visuais de estoque baixo.
* **👤 Perfil do Cliente:** Histórico detalhado de compras por cliente, calculando o valor total gasto automaticamente.
* **📊 Exportação de Relatórios:** Geração de relatórios em Excel (`.csv`) com caixas de diálogo nativas do sistema operacional para salvar os arquivos com segurança.
* **🔒 Segurança Avançada:** 
  * Sistema de **Sessões Protegidas** (Controle de Acesso por senha no backend).
  * Blindagem no Frontend contra ataques **XSS (Cross-Site Scripting)**.
* **⚡ Produtividade:** Interface focada em usabilidade, com suporte a notificações em Toast e Modais interativos.

## 🚀 Tecnologias Utilizadas

* **Backend:** Python 3, Flask (com Blueprints)
* **Frontend:** HTML5, CSS3, JavaScript Vanilla (Sanitização Anti-XSS)
* **Banco de Dados:** SQLite (com gerenciamento de conexões otimizado)

## 📁 Estrutura do Projeto

O código-fonte foi refatorado seguindo rigorosas boas práticas de engenharia de software e separação de interesses:

```text
/
├── app.py              # Arquivo principal (Ponto de entrada e configuração do Flask)
├── auth.py             # Módulo de segurança e controle de sessões (Login)
├── database.py         # Módulo de conexão e inicialização do SQLite
├── rotas_pedidos.py    # Blueprint com as regras e rotas CRUD de Pedidos
├── rotas_estoque.py    # Blueprint com as regras e rotas CRUD de Estoque
├── banco_de_dados.db   # Banco de dados SQLite (Gerado automaticamente)
├── templates/
│   └── index.html      # Estrutura da interface visual
└── static/
    ├── style.css       # Estilização do aplicativo
    └── script.js       # Lógica de interface, segurança Anti-XSS e API
⚙️ Como Executar o Projeto
Pré-requisitos
Certifique-se de ter o Python 3 instalado em sua máquina.

Instalação e Execução
Clone este repositório:

Bash
git clone [https://github.com/uemuralc/Gerenciador-de-pedidos.git](https://github.com/uemuralc/Gerenciador-de-pedidos.git)
Acesse a pasta do projeto:

Bash
cd Gerenciador-de-pedidos
Instale as bibliotecas necessárias:

Bash
pip install flask pywebview
Execute o aplicativo:

Bash
python app.py
Nota de Acesso: A senha padrão configurada para desbloquear as abas do sistema é 1234. Você pode alterá-la editando a variável correspondente no arquivo auth.py.