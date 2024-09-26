import random
import string

import pygame
import pygame._sdl2 as sdl2


def generateSalt(length=16):
    alphabet = string.ascii_letters + string.digits
    return ''.join(random.choice(alphabet) for _ in range(length))

def getDevices(self, capture_devices: bool = False):
    init_by_me = not pygame.mixer.get_init()
    if init_by_me:
        pygame.mixer.init()
    devices = list(sdl2.get_audio_device_names(capture_devices))
    if init_by_me:
        pygame.mixer.quit()
    return devices
