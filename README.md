<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/a5347f6c-c71a-4f53-913f-d6fb81d06f24" />


# 📦 Painel de Gestão - Pedidos e Estoque

Um aplicativo desktop leve, rápido e eficiente desenvolvido com Python e tecnologias Web para facilitar o controle de pedidos de clientes e o gerenciamento de matérias-primas no estoque. 

O sistema foi desenhado para rodar como um aplicativo nativo no Windows, combinando o poder do backend em **Flask** e **SQLite** com uma interface moderna renderizada via **PyWebView**.

## ✨ Funcionalidades

* **📋 Fila de Pedidos:** Cadastro, edição, exclusão e alteração de status (Pendente, Em Andamento, Finalizado) de pedidos.
* **🛠️ Gestão de Estoque:** Controle de matérias-primas com botões de acesso rápido para adicionar ou subtrair quantidades.
* **👤 Perfil do Cliente:** Histórico detalhado de compras por cliente, calculando o valor total gasto automaticamente.
* **📊 Exportação de Relatórios:** Geração de relatórios em Excel (`.csv`) com caixas de diálogo nativas do sistema operacional para salvar os arquivos com segurança.
* **🔒 Área Restrita:** Proteção por senha no backend para evitar acessos não autorizados a abas sensíveis do sistema.
* **⚡ Produtividade:** Interface focada em usabilidade, com suporte a atalhos de teclado (como a tecla `Enter` para salvar formulários), notificações em Toast e Modais interativos.

## 🚀 Tecnologias Utilizadas

* **Backend:** Python 3, Flask
* **Frontend:** HTML5, CSS3, JavaScript Vanilla
* **Banco de Dados:** SQLite (nativo, com proteção contra corrupção de dados)
* **Desktop Wrapper:** PyWebView (para empacotar a aplicação web como um software desktop)

## 📁 Estrutura do Projeto

O código-fonte foi refatorado seguindo boas práticas de modularização de software e o padrão do Flask:

```text
/
├── Gerenciamento_de_pedidos.py  # Arquivo principal (Backend e rotas API)
├── banco_de_dados.db            # Banco de dados SQLite (Gerado automaticamente)
├── templates/
│   └── index.html               # Estrutura da interface
└── static/
    ├── style.css                # Estilização do aplicativo
    └── script.js                # Lógica de interface e comunicação com a API
⚙️ Como Executar o Projeto
Pré-requisitos
Certifique-se de ter o Python 3 instalado em sua máquina.

Instalação
Clone este repositório:

Bash
git clone [https://github.com/uemuralc/Gerenciador-de-pedidos.git](https://github.com/uemuralc/Gerenciador-de-pedidos.git)
Acesse a pasta do projeto:

Bash
cd nome-do-repositorio
Instale as bibliotecas necessárias:

Bash
pip install flask pywebview
Execute o aplicativo:

Bash
python Gerenciamento_de_pedidos.py
Nota: A senha padrão configurada para acessar as áreas restritas é 1234. Você pode alterá-la editando a variável SENHA_SISTEMA no arquivo .py.
