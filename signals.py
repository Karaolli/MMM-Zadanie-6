import numpy as np

def sine(frequency : float, phase : float, duration : float, cutoff : float, time_step : float):
    t = np.arange(0, duration, time_step)
    y = np.sin(2 * np.pi * frequency * t + phase * np.pi / 180)
    y[t > duration * cutoff] = 0
    return t, y

def square(frequency : float, phase : float, duration : float, cutoff : float, time_step : float):
    t = np.arange(0, duration, time_step)
    y = np.sign(np.sin(2 * np.pi * frequency * t + phase * np.pi / 180))
    y[t > duration * cutoff] = 0
    return t, y

def sawtooth(frequency : float, phase : float, duration : float, cutoff : float, time_step : float):
    t = np.arange(0, duration, time_step)
    y = 2 * ((t * frequency + phase / 360) % 1) - 1
    y[t > duration * cutoff] = 0
    return t, y