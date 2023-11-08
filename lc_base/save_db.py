# DEPRECATED - Use keypoints.py, to get combined answer
# Use this file directly to convert PDFs into FAISS embeddings and save their mapping, specify the desired input and outputs folder

from database import Data
import os

# 1 cent to create embeddings for 9 reports
# Store all reports into inp_dir and the generated DB for all reports will be saved in out_dir
data = Data(inp_dir=os.path.join("inputs", "papers"), out_dir=os.path.join("outputs", "faiss", "papers"))
data.check_output()
data.get_faiss_embeddings()
