## Save logs in a csv file

import pandas as pd
import os

def save_log(file_path:str, query:str, response:str, model_name:str, time_taken:float, inp:str, data:str):
    '''
    Takes in the chat query and response and save in a log file
    Args:
        file_path: The path to log csv file
        query: The string of query to the model
        reponse: Response string from the model
        model_name: The model prompted
        time: Time taken to generate response
        inp: Input directory of the PDF file 
        data: Dir containing chroma DB
    '''
    key_list = ['query', 'response', 'model', 'querywords', 'responsewords', 'time', 'inputdir', 'datadir']
    if not os.path.exists(file_path):
        data_df = pd.DataFrame(columns=key_list)
        data_df.to_csv(file_path)
        # data_df[0] = [0,0,0,0,0,0,0,0]

    df_log = pd.read_csv(file_path)
    l = len(df_log)
    append_row = [query, response, model_name, len(query), len(response), time_taken, inp, data]
    df_log.loc[l, key_list] = append_row
    df_log.to_csv(file_path)


# save_log('logs/policy_stuff1.csv', 'temp_query', 'temp_response', 'gpt4', 23, 'tmp_inp', 'tmp_dir')
