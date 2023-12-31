
from RRT import RRT 
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np


class Plotter:

    def __init__(self,rrt):
        self.rrt = rrt 
        self.fig,self.ax = plt.subplots()
        self.plot_vertices()
        self.plot_edges() 
        self.plot_circle_obstacles()
        self.ax.set_xlim(0,self.rrt.D[0])
        self.ax.set_ylim(0,self.rrt.D[1])


        ratio = 1.0
        xleft, xright = self.ax.get_xlim()
        ybottom, ytop = self.ax.get_ylim()
        self.ax.set_aspect(abs((xright-xleft)/(ybottom-ytop))*ratio)

        plt.show()

    def plot_vertices(self): 
        for v in self.rrt.G: 
            plt.plot(v[0],v[1],'bo')
    
    def plot_edges(self):
        segs = [] 
        for v in self.rrt.G.keys():
            v_primes = self.rrt.G[v] 
            if len(v_primes) > 0: 
                for vp in v_primes: 
                    segs.append(np.array([v,vp]))
        
        line_segments = LineCollection(segs, linewidths=(1),
                                colors='black', linestyle='solid')
        self.ax.add_collection(line_segments)

    def plot_circle_obstacles(self): 
        for crc in self.rrt.circle_obstacles:
            circle = plt.Circle((crc[0],crc[1]),crc[2])
            self.ax.add_patch(circle) 

        
def main(): 

    rrt = RRT(q_init=(10,10),K=500,delta=1,D=(50,50))
    plotter = Plotter(rrt)

main() 

    


