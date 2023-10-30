from database import Data

# 1 cent to create embeddings for 9 reports
data = Data(inp_dir='reports', out_dir="output_reports")
data.check_output()
data.get_faiss_embeddings()
