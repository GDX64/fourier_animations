import numpy as np
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle, Arrow
from matplotlib.collections import CircleCollection, LineCollection
import pandas as pd

#Saving
dpi=130
save=False
time_pass=False
#Drawing
freq=np.array([ 1, -1, 3,-3, 5, -5])*1
amplitudes=np.array([0.7, 0.7, 0.3, 0.3, 0.2, 0.2])*0.7
thetas=np.array([0,0,0,0,0,0])+np.pi/2
d_frame=pd.DataFrame(dict(amplitude=amplitudes,phase=thetas,freq=freq))
d_frame
#parametros
STRECH_FACTOR=4
frame_rate=60
N_POINTS=60*10
Ts=1/N_POINTS*STRECH_FACTOR
N_CICLES=1

#Classe principal que administra todos os atributos
class Fourier_ani(object):
    def __init__(self, ax, df):
        self.df=df
        self.xdata = np.array([])
        self.ydata = np.array([])
        self.ax=ax
        self.line = Line2D(self.xdata, self.ydata, color='b')
        self.ax.add_line(self.line)
        self.ax.set_ylim(-1.2, 1.2)
        self.ax.set_xlim(-1.2, 1.2)
        self.circles=[] #vetor com os circulitos

        #init circles
        N=len(df.freq)-1
        for i in range(N):
            self.circles.append(l_circle(self.df.amplitude[i], self.df.phase[i], self.df.freq[i]))
            self.circles[-1].init_me(self.ax)

        #a cor da ponta é diferente
        self.circles.append(l_circle(self.df.amplitude[N], self.df.phase[N],
                            self.df.freq[N]))
        self.circles[-1].init_me(self.ax, dot_color='r')


    def update_circles(self, t):
        center=np.array((0,0), dtype=float)
        #pdb.set_trace()
        for circle in self.circles:
            center=np.array(circle.update_me(tuple(center),t))


    def update(self, t):
        self.update_circles(t)
        self.xdata=np.append(self.xdata, self.circles[-1].dot.center[0])
        self.ydata=np.append(self.ydata, self.circles[-1].dot.center[1])
        if(time_pass==True):
            self.xdata-=Ts
        self.line.set_data(self.xdata, self.ydata)

        return self.line,


#===Circle class====
class l_circle(object):
    def __init__(self, r, theta0, frequency, o=(0,0)):
        self.o=o
        self.r=r
        self.theta0=theta0
        self.theta=0
        self.frequency=frequency
        self.c=Circle(self.o,radius=self.r, fill=False, animated=False, edgecolor=(0.8,0.9,0.9))
        self.bar=Line2D([],[], color=(1,0.9,0.9))

    def init_me(self, ax, dot_color='g'):
        self.dot=Circle((np.cos(self.theta)*self.r+self.o[0], np.sin(self.theta)*self.r+self.o[1]),
                    animated=False, radius=0.01, color=dot_color)
        ax.add_patch(self.c)
        ax.add_patch(self.dot)
        ax.add_line(self.bar)

    def update_me(self, new_o, t):
        self.o=new_o
        self.theta=self.frequency*2*np.pi*t+self.theta0
        self.c.center=self.o
        self.dot.center=(np.cos(self.theta)*self.r+self.o[0], np.sin(self.theta)*self.r+self.o[1])
        self.bar.set_xdata((self.o[0], self.dot.center[0]))
        self.bar.set_ydata((self.o[1], self.dot.center[1]))

        return self.dot.center

#%% Extrator de parametros
def para_extr(SIGNAL, n_para):
    N=len(SIGNAL)
    freq_index=np.arange(N)
    freq_index[freq_index>N/2]-=N
    freq_index
    df=pd.DataFrame(dict(raw=SIGNAL, amplitude=np.abs(SIGNAL), phase=np.angle(SIGNAL), freq=freq_index,
                    abs_freq=np.abs(freq_index)))
    df.sort_values(axis=0, ascending=False, by='amplitude', inplace=True)
    return df[0:n_para]


#%%Funcao de animacao
def ani_start(df, save=False):
    #%%data test
    t=np.linspace(0,N_CICLES,N_POINTS)
    #%%Draw test
    fig, ax = plt.subplots(figsize=(8,8))
    ax.add_line(Line2D((0,0), (-1000,1000), color=(0.3,0.3,0.3)))
    ax.add_line(Line2D((-1000,10000), (0,0), color=(0.3,0.3,0.3)))

    # pass a generator in "emitter" to produce data for the update func
    f_ani1=Fourier_ani(ax, df)
    ani = animation.FuncAnimation(fig, f_ani1.update, t, interval=int(1000/frame_rate), blit=False, repeat=False)
    if(save!=False):
        ani.save(save, fps=frame_rate, writer='ffmpeg', dpi=dpi)
    plt.show()

if(__name__=='__main__'):
    ani_start(d_frame)
