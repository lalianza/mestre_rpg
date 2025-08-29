# Mestre de RPG (RPG Master)


## 🇧🇷 Português

Este projeto tem como objetivo criar um Mestre de RPG automatizado, capaz de narrar aventuras interativas para um jogador. Utilizando o poder da Inteligência Artificial Generativa do Google (Vertex AI com o modelo Gemini Pro), o sistema simula a aleatoriedade de dados, gerencia o estado do jogador e cria narrativas dinâmicas com base nas escolhas do jogador. A base de conhecimento do mundo (inspirada em Arton, de Tormenta RPG) é gerenciada por um sistema de Recuperação Aumentada por Geração (RAG) para garantir a coerência e riqueza da história.

### Funcionalidades

* **Narrativa Dinâmica:** Gera histórias envolventes e adaptativas com o Google Gemini Pro.
* **Gestão de Estado do Jogador:** Armazena e atualiza informações cruciais como HP, inventário e localização.
* **Base de Conhecimento (RAG):** Utiliza ChromaDB para injetar informações ricas sobre o mundo de Arton na narrativa.
* **Simulação de Dados:** Incorpora elementos de aleatoriedade típicos de jogos de RPG.
* **Ambiente Local:** Configuração completa com Docker e Docker Compose para desenvolvimento e execução em ambiente local.

### Arquitetura do Projeto

O projeto é construído em torno de uma API RESTful em Python (FastAPI) e orquestrado por Docker Compose.

* **`main.py` (FastAPI):** O coração da aplicação, gerencia as requisições, orquestra os serviços e interage com o jogador.
* **`src/services/local_db_service.py`:** Gerencia a memória de longo prazo do jogador, salvando e carregando dados em um arquivo JSON local para desenvolvimento.
* **`src/services/rag_service.py`:** Interface com o ChromaDB para gerenciar e consultar a base de conhecimento do mundo de RPG (dados de `data/adventures.jsonl`).
* **`src/services/vertex_service.py`:** Conecta-se à API do Google Vertex AI (modelo Gemini Pro) para gerar a narrativa.
* **`docker-compose.yml`:** Orquestra os contêineres do backend (FastAPI) e do ChromaDB.
* **`data/adventures.jsonl`:** Arquivo contendo a base de conhecimento sobre o mundo de Arton para o RAG.

### Como Iniciar

Siga estes passos para configurar e executar o projeto localmente.

#### Pré-requisitos

* Docker e Docker Compose instalados.
* Conta no Google Cloud Platform com a Vertex AI API ativada.
* Uma conta de serviço do Google Cloud com o papel "Vertex AI User" e sua chave JSON baixada.

#### 1. Clonar o Repositório

# RPG Master

![RPG Master Banner](https://image.pollinations.ai/prompt/fantasy%20rpg%20game%20master%20with%20dice%20and%20storytelling%20elements?width=1200&height=600&seed=42)

## 🇬🇧 English

This project aims to create an automated RPG Master, capable of narrating interactive adventures for a player. Utilizing the power of Google's Generative Artificial Intelligence (**Vertex AI** with the **Gemini Pro** model), the system simulates dice rolls, manages player state, and creates dynamic narratives based on player choices. The world's knowledge base (inspired by Arton from Tormenta RPG) is managed by a **Retrieval Augmented Generation (RAG)** system to ensure story coherence and richness.

### Features

* **Dynamic Narrative:** Generates engaging and adaptive stories with Google Gemini Pro.
* **Player State Management:** Stores and updates crucial information like HP, inventory, and location.
* **Knowledge Base (RAG):** Uses **ChromaDB** to inject rich information about the world of Arton into the narrative.
* **Dice Roll Simulation:** Incorporates randomness elements typical of RPG games.
* **Local Environment:** Full setup with **Docker** and **Docker Compose** for local development and execution.

### Project Architecture

The project is built around a **Python RESTful API** (FastAPI) and orchestrated by **Docker Compose**.

* **`main.py` (FastAPI):** The core of the application, handling requests, orchestrating services, and interacting with the player.
* **`src/services/local_db_service.py`:** Manages the player's long-term memory, saving and loading data to a local JSON file for development.
* **`src/services/rag_service.py`:** Interfaces with ChromaDB to manage and query the RPG world's knowledge base (data from `data/adventures.jsonl`).
* **`src/services/vertex_service.py`:** Connects to the Google Vertex AI API (Gemini Pro model) to generate the narrative.
* **`docker-compose.yml`:** Orchestrates the backend (FastAPI) and ChromaDB containers.
* **`data/adventures.jsonl`:** A file containing the knowledge base about the world of Arton for RAG.

### How to Get Started

Follow these steps to set up and run the project locally.

#### Prerequisites

* Docker and Docker Compose installed.
* Google Cloud Platform account with **Vertex AI API** enabled.
* A Google Cloud service account with the **"Vertex AI User"** role and its JSON key downloaded.

#### 1. Clone the Repository

```bash
git clone [https://github.com/your-username/rpg-master.git](https://github.com/your-username/rpg-master.git)
cd rpg-master

```bash
git clone [https://github.com/seu-usuario/mestre-de-rpg.git](https://github.com/seu-usuario/mestre-de-rpg.git)
cd mestre-de-rpg
