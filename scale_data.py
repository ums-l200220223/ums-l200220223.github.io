#scale.py
import tarfile
import pandas as pd
from itertools import islice
from sklearn.feature_extraction.text import CountVectorizer

def load_yelp_reviews(num_docs):
    # Membuka arsip .tar
    with tarfile.open('data_group.tar', 'r') as tar:
        # Mengakses file data_group_cleaned.csv di dalam arsip
        datafile = tar.extractfile('data_group_cleaned.csv')
        if datafile is None:
            raise FileNotFoundError("data_group_cleaned.csv tidak ditemukan dalam arsip data_group.tar")
        
        # Membaca file CSV ke dalam DataFrame
        df = pd.read_csv(datafile)
        
        # Memastikan kolom 'Message' ada
        if 'Message' not in df.columns:
            raise KeyError("Kolom 'Message' tidak ditemukan dalam file data_group_cleaned.csv")
        
        # Hilangkan baris dengan NaN di kolom 'Message'
        df['Message'] = df['Message'].fillna("").astype(str)
        
        # Mengambil sejumlah dokumen sesuai num_docs
        return list(islice(df['Message'], num_docs))

def make_matrix(docs, binary=False):
    # Modify min_df and max_df values
    vec = CountVectorizer(min_df=5, max_df=0.9, binary=binary)  # Adjusted parameters
    mtx = vec.fit_transform(docs)
    
    # Extract column names
    cols = [None] * len(vec.vocabulary_)
    for word, index in vec.vocabulary_.items():
        cols[index] = word
    
    return mtx, cols

# Contoh penggunaan
num_docs = 100
docs = load_yelp_reviews(num_docs)
mtx, cols = make_matrix(docs)

print("Matrix shape:", mtx.shape)
print("Feature names:", cols[:10])  # Menampilkan 10 fitur pertama
