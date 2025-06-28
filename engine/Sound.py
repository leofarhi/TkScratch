import wave
import numpy as np

class Sound:
    def __init__(self, name, filepath):
        self.name = name
        self.filepath = filepath
        self.duration = self._get_duration()

    def _get_duration(self):
        try:
            with wave.open(self.filepath, 'rb') as wf:
                frames = wf.getnframes()
                rate = wf.getframerate()
                return round(frames / float(rate), 2)
        except:
            return 0.0
        
    def get_duration_str(self):
        minutes = int(self.duration // 60)
        seconds = int(self.duration % 60)
        milliseconds = int((self.duration - int(self.duration)) * 1000)
        return f"{minutes}:{seconds:02}.{milliseconds:03}"

    def get_waveform_data(self, points=5000):
        try:
            with wave.open(self.filepath, 'rb') as wf:
                frames = wf.readframes(wf.getnframes())
                samples = np.frombuffer(frames, dtype=np.int16)
                if len(samples) > points:
                    factor = len(samples) // points
                    samples = samples[:factor * points].reshape(-1, factor).mean(axis=1)
                return samples
        except:
            return np.zeros(points)
        
test_sound = Sound("Example Sound", "tests/test.wav")