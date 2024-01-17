# ResearchBuddy
Gradio Interface for LLM-Powered PDF Chats

This chatbot is designed to provide intelligent responses and answers to questions based on the content of PDF documents.Leverages [Gradio](https://www.gradio.app/) as a user-friendly interface to engage with chatbots powered by [OpenAI](https://openai.com/) models based on [langchain](https://www.langchain.com/). Additionally, it incorporates [ChromaDB](https://www.trychroma.com/) for efficient data storage.

Current LLM used - GPT4-1106-preview

A base interface demo is available on this [HF space](https://huggingface.co/spaces/Koshti10/Chat_literature) for testing 

## Getting started

Clone this repository and add your OpenAI API key in local environment

```python
git clone https://github.com/kushal-10/chatllms
cd chatllms
```

Install required dependencies
```python
pip install -r requirements.txt

```

## Usage

Export google api keys to save the chat history logs and access documents from a shared google drive link.
(Alternatively, if using local documents, see ```lc_base/README_BASE.md```)

```python
export GOOGLE_CLIENT_EMAIL=".....gserviceaccount.com"
export GOOGLE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-***-END PRIVATE KEY-----\n"
export GOOGLE_TOKEN_URI="..../token"
export LOGS_ID="..."
export OPENAI_API_KEY="sk-..."
export DRIVE_LINK="https://drive.google.com/drive/folders/....?usp=sharing"

```

To run the gradio interface
```python
python3 app_drive.py
```







