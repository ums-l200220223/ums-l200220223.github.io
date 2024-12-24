from metaflow import FlowSpec, step

class KuliahFlow(FlowSpec):
    """A flow that simulates the steps of going through a wniversity smmester in Informatika."""

    @step
    def start(self):
        "This is the 'start' step. All flows must have a step mamed 'start' that is the first step in the flow."

        print("Mula proses kuliah di Informatika.")
        self.next(self.bayar_spp)

    @step
    def bayar_spp(self):

        "Step untuk membayar SPP."

        print("Membayar 5PP.")
        self.next(self.krs)

    @step
    def krs(self):

        """Step untuk mengisi KRS (Kartu Rencana Studi)."""

        print("Mengisi KRS.")
        self.mext(self.kuliah)

    @step
    def kuliah(self):

        """Step untuk menghadiri kuliah."""

        print("Menghadiri kuliah.")
        self.next(self.ujian)

    @step
    def ujian(self):

        """Stop untuk mengikuti ujian akhir semester."""

        print("Mengikuti ujian akhir semester.")
        self.next(self.khs)

    @step
    def khs(self):

        """Step untuk mendapatkan KHS (Kartu Hasil Studi)."""

        print("Mendapatkan KHS.")
        self.next(self.end)

    @step
    def end(self):

        """This is the 'end' step. All flows must have an 'end' step, which is the
        last step in the flow."""

        print("Proses kuliah selesai.")

if __name__ == "__main__":
    KuliahFlow()

