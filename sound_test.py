#!/usr/bin/env python 
import numpy as np
import pygame as pg

duration = 1.0          # in seconds
sample_rate = 14100
bits = 16
frequency_l = 440
frequency_r = 540

normal = True
Folkert = True
Reinier = True
Ewoud = True

def gauss(x,d,mu):
    return np.exp(-(x-mu)**2/(2*d**2))

try:
    pg.mixer.init(frequency = sample_rate, size = -bits, channels = 2)
    Nsamples = int(round(duration*sample_rate))

    

    zeros = np.zeros((Nsamples, 2), dtype = np.int16)
    max_sample = 2**(bits - 1) - 1
    print(max_sample)
    for s in range(Nsamples):
        t = float(s)/sample_rate        # time in seconds
        # left box
        if normal:
            zeros[s][0] = int(round(max_sample*np.sin(2*np.pi*frequency_l*t)))
            zeros[s][1] = int(round(max_sample*np.sin(2*np.pi*frequency_r*t))) 
        elif Folkert:
            zeros[s][0] = int(round(max_sample*np.sin(2*np.pi*frequency_l*t)*gauss(t,.1,.5)))
            zeros[s][1] = int(round(max_sample*np.sin(2*np.pi*frequency_r*t)*gauss(t,.1,.5)))  
        elif Reinier:
            zeros[s][0] = int(round(max_sample*np.sin(2*np.pi*frequency_l*(1+gauss(t,.1,.5))*t)))
            zeros[s][1] = int(round(max_sample*np.sin(2*np.pi*frequency_r*(1+gauss(t,.1,.5))*t)))
        elif Ewoud:
            A = max_sample/5
            zeros[s][0] = int(round(A*np.sin(2*np.pi*frequency_l*t*.8)*gauss(t,.1,.3)+ A*np.sin(2*np.pi*frequency_l*t*.9)*gauss(t,.1,.4) + A*np.sin(2*np.pi*frequency_l*t)*gauss(t,.1,.5) + A*np.sin(2*np.pi*frequency_l*t*1.1)*gauss(t,.1,.6)+A*np.sin(2*np.pi*frequency_l*t*1.2)*gauss(t,.1,.7)))
            zeros[s][1] = int(round(A*np.sin(2*np.pi*frequency_r*t*.8)*gauss(t,.1,.3)+ A*np.sin(2*np.pi*frequency_r*t*.9)*gauss(t,.1,.4) + A*np.sin(2*np.pi*frequency_r*t)*gauss(t,.1,.5) + A*np.sin(2*np.pi*frequency_r*t*1.1)*gauss(t,.1,.6)+A*np.sin(2*np.pi*frequency_r*t*1.2)*gauss(t,.1,.7)))  

    
    print(zeros)
    sound = pg.sndarray.make_sound(zeros)



    sound.play()
    pg.time.wait(int(round(1000*duration)))

finally:
    pg.mixer.quit()

import matplotlib.pyplot as plt
plt.plot(zeros)
plt.show()
