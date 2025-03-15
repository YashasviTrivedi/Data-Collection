import faiss
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import subprocess  # Runs scraping scripts before FAISS processing

# ✅ Run web scraping scripts first
subprocess.run(["python", "States_data.py"])
subprocess.run(["python", "VP_data.py"])

# ✅ Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# ✅ Load scraped dataset
csv_file = "States_data.csv"
df = pd.read_csv(csv_file)

# ✅ Convert timestamp to datetime
df["Timestamp"] = pd.to_datetime(df["Timestamp"])
df.columns = df.columns.str.strip()

# ✅ Convert text data into embeddings
df["text"] = df.apply(lambda x: f"Timestamp: {x['Timestamp']}, State: {x['State']}, Current Exchange Price: {x['Current Exchange Price (₹/Unit)']},Current Demand Met: {x['Current Demand Met (MW)']},Current Power Purchased: {x['Current Power Purchased (MW)']}", axis=1)
text_embeddings = np.array(model.encode(df["text"].tolist()))

# ✅ Create FAISS index
index = faiss.IndexFlatL2(text_embeddings.shape[1])
index.add(text_embeddings)
faiss.write_index(index, "faiss_index.bin")

print("✅ FAISS index updated successfully with the latest scraped data!")
