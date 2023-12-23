# LLM-Product-Assistant

## Overview

The LLM-Product-Assistant is an interactive Q&A system designed to help users to better understand and navigate the functionalities of a particular product. For this specific project, we focused on troubleshooting issues users might have with Amazon VPC.

## Table of Contents

1. [Technologies Deployed](#technologies-deployed)
2. [Installation & Setup](#installation--setup)
3. [Contributors](#contributors)

## Technologies Deployed

- **LangChain**: html loader, text summarization and chunking, wrappers for OpenAI and Pinecone
- **OpenAI API**: embeddings generation, retrieval
- **Pinecone**: embeddings storage and indexing, similairty search for `top_k`
- **PEFT**: LLaMa fine-tunning

## Installation & Setup

### Prerequisites

- Python version: 3.10.7
- Obtain the required API keys from a team member.

### Steps

1. **Clone the Repository:**
    ```bash
    git clone <repository-link>
    cd LLM-Product-Assistant
    ```

2. **Navigate to the Main Folder:**
    ```bash
    cd path/to/main/folder
    ```

3. **Build the Docker Image:**
    ```bash
    docker build -t chatbot -f 07_Docker/Dockerfile .
    ```

4. **Run the Docker Container:**
    ```bash
    docker run -p 5000:5000 chatbot
    ```

5. **Access the Application:**
    Click on the link that appears in the console to start interacting with the chatbot.

## Contributors

- **Sam Swain**: Project Lead
- **Zhengyuan (Donald) Li**: Generative AI Engineer
- **Brian Hong**: Generative AI Engineer
- **Wencheng Zhang**: Generative AI Engineer
