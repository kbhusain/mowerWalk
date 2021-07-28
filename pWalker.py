#--------------------------------------------------------------------------------
# Free to use.
# Author:  kamran husain  kbhusain@gmail.com
# Date:    july 28, 2021
#--------------------------------------------------------------------------------
import numpy as np
import pandas as pd
from scipy.spatial import ConvexHull, convex_hull_plot_2d
import matplotlib.pyplot as plt
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
#--------------------------------------------------------------------------------
# These points define my lawn endpoints in a clockwise manner. 
# you can probably store them in a text file - 
# you can also use a convex hull algorithm or sort them in a clockwise manner
coordinates = [ (0,0), (10,0), (10,10), (15, 10),
                (15,65), (45, 65), 
                (45,10), (60,10), (60,75), (0,75) ]
VELOCITY = 2.0
TDELTA   = 1.0 
#THETA    = np.pi / 4 
THETA    = np.random.random_sample() * np.pi/4
movingPossible = True

#--------------------------------------------------------------------------------
# A garden for the mower to roam on. 
#--------------------------------------------------------------------------------
class aGarden:
    def __init__(self,wd,ht,coordinates):
        self.bins = np.zeros((wd,ht),float)
        self.coordinates = coordinates; 
        self.polygon = Polygon(coordinates)
        

#--------------------------------------------------------------------------------
# Needs a lawn to walk on. 
#--------------------------------------------------------------------------------
class aMower:
    def __init__(self,garden,backs_up=0):
        self.garden = garden
        #print(polygon.contains(point))
        # Create your arrays;
        # =====================================
        # Initial movement.
        # =====================================
        self.x = 0; 
        self.y = 10;
        self.azimuth = THETA
        self.velocity = VELOCITY
        self.thetaStepSize = 50
        dt = np.pi/self.thetaStepSize
        if backs_up:
            self.thetaSteps  = [ (dt * float(i)) + (np.pi/2)  for i in range(self.thetaStepSize)]
        else:
            self.thetaSteps  = [ (dt * float(i)) - (np.pi/2)  for i in range(self.thetaStepSize)]
        self.lastTheta = 0;

    def resetLocation(self):
        self.x = 0; 
        self.y = 10;
        self.azimuth =  np.random.random_sample() * np.pi/4
        
    def moveMe(self, method='STEP'):
        dy = self.velocity * np.sin(self.azimuth)
        dx = self.velocity * np.cos(self.azimuth)
        v  = self.garden.polygon.contains(Point(self.x+dx,self.y+dy))
        if v:
            self.x  += dx 
            self.y  += dy
        else:

            if method == 'STEP': 
                self.lastTheta = (self.lastTheta + 1) % self.thetaStepSize
                dTheta = self.thetaSteps[self.lastTheta]
            # This forces the guy into a corner and makes him stay there. 
            if method == 'STEP_RANDOM': 
                self.lastTheta = (self.lastTheta + 1) % self.thetaStepSize 
                dTheta = self.thetaSteps[self.lastTheta] - ((np.random.random_sample() * np.pi/16) - (np.pi/8))
            if method == 'RANDOM': 
                dTheta = (np.random.random_sample() * np.pi/2) - (np.pi/4)
            self.azimuth += dTheta
            # print("Turning...", azimuth, dTheta)
        self.garden.bins[int(self.x)][int(self.y)] += 1.0

    def getLocation(self):
        return (self.x, self.y)


if __name__ == '__main__':
    my_coordinates = [ (0,0), (10,0), (10,10), (15, 10),
                    (15,65), (45, 65), (45,75), (0,75)]

    coordinates = [ (0,0), (10,0), (10,10), (15, 10),
                (15,65), (45, 65), 
                (45,10), (60,10), (60,75), (0,75) ]


    # Create you gardens and a mower for each 
    myGardens = [ aGarden(100,100,coordinates) for i in range(4) ]
    myMower0  = aMower(myGardens[0])
    myMower1  = aMower(myGardens[1],backs_up=0)
    myMower2  = aMower(myGardens[2],backs_up=1)
    myMower3  = aMower(myGardens[3],backs_up=1)

    # You can try a londer period. 
    for day in range(5): 
        i = 0 
        movingPossible = True

        # Mowers start from the base. 
        myMower0.resetLocation()
        myMower1.resetLocation()
        myMower2.resetLocation()
        myMower3.resetLocation()

        # in case you get stuck forever. -- happens in real life --- 
        while movingPossible: 
            i = i+1
            if i > 50000: movingPossible = False
            myMower0.moveMe('RANDOM')
            myMower1.moveMe('STEP')
            myMower2.moveMe('STEP')
            myMower3.moveMe('STEP_RANDOM')
            #if i % 10000 == 0: print(myMower.getLocation())
        colorMapName = 'YlGnBu'
        titles = [ 'Random', 'Step - no backup', 'Step - backs up','Step - back/random']
        
        #--------------------------------------------------------------------------------
        # Draw out the results. 
        #--------------------------------------------------------------------------------
        fig,axs = plt.subplots(2,2)
        k =0
        fig.suptitle("Day - %d - Run " % (day+1))
        for i in range(2):
            for j in range(2):
                ax = axs[i,j]
                ax.set_title(titles[k])
                df = pd.DataFrame(myGardens[k].bins)
                c1 = ax.pcolor(df,cmap=colorMapName)
                fig.colorbar(c1,ax=ax)
                k +=1 
        name = "Day - %d" % (day + 1)
        plt.savefig(name)
        plt.show()