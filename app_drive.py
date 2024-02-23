# Application file for Gradio App for OpenAI Model

import gradio as gr
import time
import datetime
import os

from lc_base.chain import openai_chain
from driveapi.drive import upload_chat_to_drive
from driveapi.drive_database import create_chroma_db

# global time_diff, model_name, search_type
time_diff = 0
# model_name="gpt-3.5-turbo-1106"
# model_name = "gpt-4-1106-preview"
model_name = "gpt-4-0125-preview"
search_type = "stuff"
input_question = ""
model_response = ""
user_feedback = ""

dir = ""
title = """<h1 align="center">ResearchBuddy</h1>"""
description = """<br><br><h3 align="center">This is a GPT based Research Buddy to assist in navigating new research topics.</h3>"""

def save_api_key(api_key):
    os.environ['OPENAI_API_KEY'] = str(api_key)
    return f"API Key saved in the environment: {api_key}"

def save_drive_link(drive_link):
    os.environ['DRIVE_LINK'] = str(drive_link)
    print(f"API Key saved in the environment: {drive_link}")
    return None

def create_data_from_drive():
    global db
    db = create_chroma_db()
    return "Processing Completed - You can start the chat now!"

def user(user_message, history):
    return "", history + [[user_message, None]]

def respond(message, chat_history):

    global time_diff, model_response, input_question

    print("Database is ...................")
    print(type(db))
    question = str(message)
    chain = openai_chain(inp_dir=dir)
    # prompt = '''You are an AI assistant equipped with advanced analytical capabilities. 
    # You have been provided with a carefully curated set of documents relevant to a specific question. 
    # Your task is to meticulously analyze these documents and provide a comprehensive answer to the following question. 
    # Ensure that your response is detailed, accurate, and maintains a formal, academic tone. 
    # The information required to answer this question is contained within the documents. 
    # Please proceed with a thorough examination to deliver a well-informed response. Question:  '''

    # query = prompt + question
    query = question

    start_time = time.time()

    output = chain.get_response_from_drive(query=query, database=db, k=10, model_name=model_name, type=search_type)
    print(output)

    # Update global variables to log
    time_diff = time.time() - start_time
    model_response = output
    input_question = question
    
    bot_message = output
    chat_history.append((message, bot_message))

    time.sleep(2)
    return " ", chat_history

def save_feedback(feedback):
    global user_feedback
    user_feedback = feedback

    curr_date = datetime.datetime.now()
    file_name = f"chat_{curr_date.day}_{curr_date.month}_{curr_date.hour}_{curr_date.minute}_{curr_date.second}.csv"
    log_data = [
        ["Question", "Response", "Model", "Time", "Feedback"],
        [input_question, model_response, model_name, time_diff, user_feedback]
    ]
    
    if user_feedback[0] != "None":
        upload_chat_to_drive(log_data, file_name)

def default_feedback():
    return "None"

def default_text():
    return ""

def text_feedback(feedback):
    global text_feedback
    text_feedback = feedback

    curr_date = datetime.datetime.now()
    file_name = f"chat_{curr_date.day}_{curr_date.month}_{curr_date.hour}_{curr_date.minute}_{curr_date.second}.csv"
    log_data = [
        ["Question", "Response", "Model", "Time", "Feedback"],
        [input_question, model_response, model_name, time_diff, text_feedback]
    ]

    upload_chat_to_drive(log_data, file_name)

with gr.Blocks(theme=gr.themes.Soft(primary_hue="emerald", neutral_hue="slate")) as chat:
    gr.HTML(title)

    global db

    with gr.Row():
        with gr.Column():
            api_key_input = gr.Textbox(lines=1, label="Enter your OpenAI API Key, then press Enter...")

        with gr.Column():
            drive_link_input = gr.Textbox(lines=1, label="Enter your shared drive link, then press Enter...")

    with gr.Row():
        process_files_input = gr.Button(value="Process files")   

    with gr.Row():
        status_message = gr.Text(label="Status", value="Click - Process Files")

    
    
    api_key_input.submit(save_api_key, [api_key_input])
    drive_link_input.submit(fn=save_drive_link, inputs=[drive_link_input])
    drive_link_check = os.environ.get("DRIVE_LINK")
    process_files_input.click(fn=create_data_from_drive, outputs=status_message)

    chatbot = gr.Chatbot(height=750)
    msg = gr.Textbox(label="Send a message", placeholder="Send a message",
                             show_label=False, container=False)  

    with gr.Row():
        with gr.Column():
            gr.Examples([
                ["Explain these documents to me in simpler terms."],
                ["What does these documents talk about?"],
                ["Give the key topics covered in these documents in less than 10 words."],
                ["What are the key findings in these documents?"],
            ], inputs=msg, label= "Click on any example to copy in the chatbox"
            )

    with gr.Row():
        with gr.Column():
            feedback_radio = gr.Radio(
                choices=["1", "2", "3", "4", "5", "6", "None"],
                value=["None"],
                label="How would you rate the current response?",
                info="Choosing a number sends the following diagnostic data to the developer - Question, Response, Time Taken. Let it be [None] to not send any data.",
            )
        
        with gr.Column():
            feedback_text = gr.Textbox(lines=1, label="Additional comments on the current response...")


    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    msg.submit(default_feedback, outputs=[feedback_radio])
    msg.submit(default_text, outputs=[feedback_text])

    feedback_radio.change(
        fn=save_feedback,
        inputs=[feedback_radio]
    )

    feedback_text.submit(
        fn=text_feedback,
        inputs=[feedback_text]
    )

    gr.HTML(description)


chat.queue()
chat.launch()