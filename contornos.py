import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import ani
import os

print(os.getcwd())
im = cv2.imread('images/neymar3.jpg')
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,127,255,0)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

#Darwing
cv2.drawContours(im, contours, -1, (0,255,0), 3)
cv2.imshow('image',im)
cv2.waitKey(0)
cv2.destroyAllWindows()

cnt=np.array(contours)
#o shape 0 é o contorno da imagem (um quadrado, no caso)
cnt[1][1,0] #o 1 é o que a gente quer
#plt.figure()
#plt.plot(cnt[1][:,0,1],cnt[1][:,0,0])

#%% Fourier
#Passando contorno para parte real e imaginaria
signal=cnt[1][:,0,1]-np.mean(cnt[1][:,0,1])+(cnt[1][:,0,0]-np.mean(cnt[1][:,0,0]))*1j
signal=signal/max(np.abs(signal))*1
signal*=-1j #Girando a parada
SIGNAL=np.fft.fft(signal)/len(signal)
#%%Extraindo parametros
def para_extr(SIGNAL, n_para):
    N=len(SIGNAL)
    freq_index=np.arange(N)
    freq_index[freq_index>N/2]-=N
    freq_index
    df=pd.DataFrame(dict(raw=SIGNAL, amplitude=np.abs(SIGNAL), phase=np.angle(SIGNAL), freq=freq_index,
                    abs_freq=np.abs(freq_index)))
    df.sort_values(axis=0, ascending=False, by='amplitude', inplace=True)
    return df[0:n_para]

df_ex=ani.para_extr(SIGNAL, 20)
df_ex.reset_index(inplace=True)
df_ex

ani.ani_start(df_ex, save=False)
