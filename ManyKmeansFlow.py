import os

# Menonaktifkan plugin Metaflow yang tidak diperlukan
os.environ['METAFLOW_KUBERNETES_PLUGIN_ENABLED'] = 'false'
os.environ['METAFLOW_BATCH_PLUGIN_ENABLED'] = 'false'
os.environ['METAFLOW_S3_PLUGIN_ENABLED'] = 'false'
os.environ['METAFLOW_CONDA_STEP_DECORATOR'] = 'false'

from metaflow import FlowSpec, step, Parameter, resources, conda_base, profile

# Decorator conda_base untuk menentukan versi Python dan pustaka
@conda_base(python='3.8.3', libraries={'scikit-learn': '0.24.1'})
class ManyKmeansFlow(FlowSpec):

    # Parameter untuk jumlah dokumen yang akan digunakan
    num_docs = Parameter('num-docs', help='Number of documents to process', default=100000)

    @resources(memory=4000)
    @step
    def start(self):
        import scale_data
        # Memuat dokumen dan membuat matriks
        docs = scale_data.load_yelp_reviews(self.num_docs)  # Memuat data ulasan
        self.mtx, self.cols = scale_data.make_matrix(docs)  # Membuat matriks dari dokumen
        self.k_params = list(range(5, 55, 5))  # Range nilai k untuk K-Means
        self.next(self.train_kmeans, foreach='k_params')  # Langkah foreach

    @resources(cpu=4, memory=4000)
    @step
    def train_kmeans(self):
        from sklearn.cluster import KMeans
        self.k = self.input
        with profile('k-means'):
            # Melatih model K-Means dengan nilai k tertentu
            kmeans = KMeans(n_clusters=self.k, verbose=1, n_init=1, random_state=42)
            kmeans.fit(self.mtx)
            self.clusters = kmeans.labels_
        self.next(self.analyze)

    @step
    def analyze(self):
        from analyze_kmeans import top_words
        # Mendapatkan top words untuk setiap cluster
        self.top = top_words(self.k, self.clusters, self.mtx, self.cols)
        self.next(self.join)

    @step
    def join(self, inputs):
        # Menggabungkan hasil analisis dari setiap k
        self.top = {inp.k: inp.top for inp in inputs}
        self.next(self.end)

    @step
    def end(self):
        # Langkah akhir (opsional)
        print("K-Means clustering selesai. Hasil tersedia untuk setiap k.")

if __name__ == '__main__':
    ManyKmeansFlow()


# try:
    # from metaflow.plugins.aws.batch import batch_decorator
# except ImportError:
    # batch_decorator = None  # Plugin tidak tersedia
