# Mestre de RPG - DM Assistant

Uma ferramenta de IA que atua como um assistente para Mestres de RPG. Ela responde a perguntas, ajuda no planejamento e fornece informações com base em uma base de conhecimento personalizada, usando o poder do RAG Híbrido.

---

### 📚 Sobre o Projeto

Este projeto é um assistente de linha de comando para Mestres de RPG. Ele utiliza um sistema de Geração Aumentada por Recuperação (RAG) para buscar informações em documentos PDF e, em seguida, usa um modelo de linguagem da OpenAI para gerar respostas inteligentes e úteis.

### ✨ Funcionalidades

* **Base de Conhecimento Personalizada:** Carregue seus próprios PDFs para criar sua biblioteca de conhecimento.
* **Busca Híbrida (BM25 + Vetorial):** Usa uma combinação de busca por palavras-chave e busca por similaridade para encontrar a informação mais relevante.
* **Execução Local:** Tudo roda na sua máquina, com total controle sobre os seus dados.

---

### 🛠️ Configuração e Instalação

Siga estes passos para colocar o assistente em funcionamento:

1.  **Pré-requisitos:**
    * Python 3.9+
    * Uma chave de API da OpenAI.
    * `git` instalado.

2.  **Clone o Repositório:**
    ```bash
    git clone [https://github.com/lalianza/mestre_rpg.git](https://github.com/lalianza/mestre_rpg.git)
    cd mestre_rpg
    ```

3.  **Crie e Ative um Ambiente Virtual:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

4.  **Instale as Dependências:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Configure a Chave da API:**
    Crie um arquivo chamado `.env` na pasta raiz do projeto e adicione sua chave de API:
    ```env
    OPENAI_API_KEY="sua_chave_aqui"
    ```

6.  **Prepare a Base de Conhecimento:**
    Coloque seus documentos PDF dentro da pasta `data/documents/`. Em seguida, rode o script abaixo para processar e criar o banco de dados pesquisável:
    ```bash
    python update_vector_store.py
    ```

---

### 🚀 Como Usar

Com a configuração completa, você pode iniciar o assistente diretamente do terminal:

```bash
python main.py
