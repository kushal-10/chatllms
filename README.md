# ChatLLMs
Gradio Interface for GPT-Powered PDF Chats

This chatbot is designed to provide intelligent responses and answers to questions based on the content of PDF documents.Leverages [Gradio](https://www.gradio.app/) as a user-friendly interface to engage with chatbots powered by [OpenAI](https://openai.com/) models based on [langchain](https://www.langchain.com/). Additionally, it incorporates [ChromaDB](https://www.trychroma.com/) for efficient data storage.

## Getting started

Clone this repository and add your OpenAI API key in local environment

```python
git clone https://github.com/kushal-10/chatllms
cd chatllms
export OPENAI_API_KEY = <your secret key>
```

Install required dependencies
```python
pip install -r requirements.txt
```

## Usage

### Chatting over all the given documents, using stuff to iterate over 100 most relevant documents

Step 1: 

Create a new folder under `inputs`, for example `new_docs`, and add your PDFs here. 

Step 2:
Specify this as `inp_dir` in `save_db.py` and additionally specify where you would like the Chroma database to be stored in `out_dir`.Then run

```python
python3 lc_base/save_db.py
```

Step 3:
Specify the `out_dir` in `app.py` along with additional parameters and then run `app.py` to run the gradio interface locally.
```
python3 app.py
```

Add the API key and chat away!!

### Chatting over summaries of all given documents using map_reduce.

Step 1: 

Create a new folder under `inputs`, for example `new_docs`, and add your PDFs here. 

Step 2:
Specify this as `inpur_dir` in `main.py` and additionally specify in which folder you would like the individual Chroma database to be stored in `output_dir`. Also specify where you would like to save combined database of summaries. Change other params if required. Then run

```python
python3 main.py
```

Step 3:
Specify the `output_dir` in `app.py` along with additional parameters and then run `app.py` to run the gradio interface locally.
```
python3 app.py
```

Add the API key and chat away!!

All the responses will be saved in csv files under logs folder









