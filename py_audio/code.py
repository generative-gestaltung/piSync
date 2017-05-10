class Code:

    def _init (self):
        self.w0 = WaveFile("wav/loop1.wav")
        #self.w0 = WaveFile("wav/sin_left.wav")

    def _calc (self, phase):
        return self.w0.get_sample(phase)
