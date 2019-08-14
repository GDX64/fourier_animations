import numpy as np
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle, Arrow
from matplotlib.collections import CircleCollection, LineCollection
import pandas as pd

#Saving
dpi=130 #animation resolution
save=False #change for a name to save the animation, like animation.mp4
#Drawing: Change this parameters if you want to chose the circles manualy
#It has no effect if calling this module inside another script
freq=np.array([ 1, -1, 3,-3, 5, -5])*1
amplitudes=np.array([0.7, 0.7, 0.3, 0.3, 0.2, 0.2])*0.4
thetas=np.array([0,0,np.pi/2,-np.pi/2,0,0])+np.pi/2
d_frame=pd.DataFrame(dict(amplitude=amplitudes,phase=thetas,freq=freq))
d_frame
#parameters
time_pass=False     #if true, the graphic will move along the y axis
STRECH_FACTOR=1       #changes how much the graphic moves along y axis
frame_rate=60        #speed of animation
N_POINTS=60*10         #Number of points of the animation
Ts=1/N_POINTS*STRECH_FACTOR            #How much the graphic slides with time
N_CICLES=1           #number of cicles of the animation

#Classe principal que administra todos os atributos
class Fourier_ani(object):
    def __init__(self, ax, d_frame):
        self.d_frame=d_frame #data frame with parameters for the drawing
        self.xdata = np.array([])
        self.ydata = np.array([])
        self.ax=ax
        self.line = Line2D(self.xdata, self.ydata, color='b')
        self.ax.add_line(self.line)
        self.ax.set_ylim(-1.2, 1.2)
        self.ax.set_xlim(-1.2, 1.2)
        self.circles=[] #circle object vector

        #init circles
        N=len(d_frame.freq)-1
        for i in range(N):
            self.circles.append(L_circle(self.d_frame.amplitude[i], self.d_frame.phase[i], self.d_frame.freq[i]))
            self.circles[-1].init_me(self.ax)

        #changing the last dot color
        self.circles.append(L_circle(self.d_frame.amplitude[N], self.d_frame.phase[N],
                            self.d_frame.freq[N]))
        self.circles[-1].init_me(self.ax, dot_color='r')


    def update_circles(self, t):
        center=np.array((0,0), dtype=float)
        #pdb.set_trace()
        for circle in self.circles:
            center=np.array(circle.update_me(tuple(center),t))

    #This method will be called repeatly by the FuncAnimation every new frame
    def update(self, t):
        self.update_circles(t)
        #that's all for the line
        self.xdata=np.append(self.xdata, self.circles[-1].dot.center[0])
        self.ydata=np.append(self.ydata, self.circles[-1].dot.center[1])
        #Used for the time slide case
        if(time_pass==True):
            self.xdata-=Ts
        self.line.set_data(self.xdata, self.ydata)

        return self.line, #It has no real use, all the graphical work was already done


#===Circle class====
class L_circle(object):
    ''' This class was build to hold all the graphic stuff of a circle of the animation
        the circle, the dot, and the bar.
        r: It is the radius of the circle
        theta0 the initial angle of the dot
        frequency: if it's negative, the circle is going to turn in the opposite direction
        o: center of the circle'''
    def __init__(self, r, theta0, frequency, o=(0,0)):
        self.o=o
        self.r=r
        self.theta0=theta0
        self.theta=0
        self.frequency=frequency
        self.c=Circle(self.o,radius=self.r, fill=False, animated=False, edgecolor=(0.8,0.9,0.9))
        self.bar=Line2D([],[], color=(1,0.9,0.9))

    def init_me(self, ax, dot_color='g'):
        '''Used to initiate the circle, I could have putted that all in the __init__? Yes, I could
            but I like it better
            Pass the axis where it all will be drawn and the dot color'''
        self.dot=Circle((np.cos(self.theta)*self.r+self.o[0], np.sin(self.theta)*self.r+self.o[1]),
                    animated=False, radius=0.01, color=dot_color)
        ax.add_patch(self.c)
        ax.add_patch(self.dot)
        ax.add_line(self.bar)

    def update_me(self, new_o, t):
        '''Method used to update each circle, pass the new center and the time of simulation'''
        self.o=new_o
        self.theta=self.frequency*2*np.pi*t+self.theta0
        self.c.center=self.o
        self.dot.center=(np.cos(self.theta)*self.r+self.o[0], np.sin(self.theta)*self.r+self.o[1])
        self.bar.set_xdata((self.o[0], self.dot.center[0]))
        self.bar.set_ydata((self.o[1], self.dot.center[1]))

        return self.dot.center

#%% Extrator de parametros
def para_extr(SIGNAL, n_para):
    '''Pass the fft of the signal you want to parse and the number of coeficients to extract
        The function will return the coeficients with greater absolute value'''
    N=len(SIGNAL)
    #We must separate it into negative and positive frequencys
    freq_index=np.arange(N)
    freq_index[freq_index>N/2]-=N
    freq_index
    d_frame=pd.DataFrame(dict(raw=SIGNAL, amplitude=np.abs(SIGNAL), phase=np.angle(SIGNAL), freq=freq_index,
                    abs_freq=np.abs(freq_index)))
    d_frame.sort_values(axis=0, ascending=False, by='amplitude', inplace=True)
    return d_frame[0:n_para]


#%%Funcao de animacao
def ani_start(d_frame, save=False):
    #time vector
    t=np.linspace(0,N_CICLES,N_POINTS)
    #Draw axis
    fig, ax = plt.subplots(figsize=(8,8))
    ax.add_line(Line2D((0,0), (-1000,1000), color=(0.3,0.3,0.3)))
    ax.add_line(Line2D((-1000,10000), (0,0), color=(0.3,0.3,0.3)))
    #creating animation class
    f_ani1=Fourier_ani(ax, d_frame)
    #animation object
    ani = animation.FuncAnimation(fig, f_ani1.update, t, interval=int(1000/frame_rate), blit=False, repeat=False)
    #save if it's setted to
    if(save!=False):
        ani.save(save, fps=frame_rate, writer='ffmpeg', dpi=dpi)
    plt.show()

#I guess you know what's this
if(__name__=='__main__'):
    ani_start(d_frame)
