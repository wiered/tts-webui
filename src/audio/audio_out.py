import io

import numpy as np
import pygame
from pydub import AudioSegment

from utils.utils import getDevices


class AudioConverter:
    def convertBytesIOToSound(self, sound_fp: io.BytesIO, speed_factor: float):
        """_summary_

        Args:
            sound_fp (io.BytesIO): mp3 BytesIO file
            speed_factor (float): Sound speed factor, less - faster, more - slower
        """
        audio_segment = AudioSegment.from_file(sound_fp, format="mp3")
        new_sample_rate = int(audio_segment.frame_rate * speed_factor)
        audio_segment = audio_segment.set_frame_rate(new_sample_rate)

        raw_data = np.array(audio_segment.get_array_of_samples())
        raw_data = np.column_stack(([np.repeat(raw_data, 2), np.repeat(raw_data, 2)]))

        sound = pygame.sndarray.make_sound(raw_data)

        return sound


class AudioOut():
    def __init__(self):
        pass

    def initMixer(self, device: str = None):
        if device is None:
            devices = getDevices(False)
            if not devices:
                raise RuntimeError("No device!")
            device = devices[0]
        pygame.mixer.pre_init(devicename=device)
        pygame.mixer.init()

    def stopMixer(self):
        pygame.mixer.stop()
        pygame.mixer.music.stop()
        pygame.mixer.quit()

    def playSoundFromFile(self, filename):
        sound = pygame.mixer.Sound("sounds/" + filename)
        sound.play()

        while pygame.mixer.get_busy():
            pygame.time.Clock().tick(10)

    def playSound(self, sound_fp):
        converter = AudioConverter()
        sound = converter.convertBytesIOToSound(sound_fp, 0.9)
        sound.play()

        while pygame.mixer.get_busy():
            pygame.time.Clock().tick(10)

    def __enter__(self):
        pygame.mixer.init()

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pygame.mixer.stop()
        pygame.mixer.music.stop()
        pygame.mixer.quit()

        return True
