from MafiaGame import MafiaGame
import Constants
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm_gui

class Simulator:
    def __init__(self, setup=None, num_iterations=0):
        if(setup == None or num_iterations == 0):
            raise Exception("No game or number of iterations provided")
        self.setup = setup
        self.num_iterations = num_iterations
    
    def run(self, graph=False,verbose=True):
        results = [0]*len(self.setup.teams)
        num_mafia = self.setup.countAlignment(self.setup.mafia_type)+1
        num_town = self.setup.countAlignment(self.setup.town_type)+1
        town_results_by_day = [[0 for x in range(num_mafia)] for x in range(num_town)]
        maf_results_by_day = [[0 for x in range(num_mafia)] for x in range(num_town)]
        self.combined_results_by_day = [[0 for x in range(num_mafia)] for x in range(num_town)]
        last_day_count = [0]*(len(self.setup.players)+1)
        
        for i in tqdm_gui(range(self.num_iterations)):
            sim = MafiaGame(setup=self.setup,verbose=verbose)
            sim.play()
            for [town,maf] in sim.alignment_numbers_history:
                if(sim.winner.name == "Town"):
                    town_results_by_day[town][maf]+=1
                else:
                    maf_results_by_day[town][maf]+=1
            results[[x.name for x in self.setup.teams].index(sim.winner.name)]+=1
            last_day_count[sum(sim.alignment_numbers_history[-1])]+=1

        # Results
        for i,alignment in enumerate(self.setup.teams):
            print(f"{alignment.name}: {results[i]/self.num_iterations}")
        for i,num in enumerate(last_day_count):
            if(num != 0):
                print(f"{i}: {num/self.num_iterations}")
        for i in range(len(town_results_by_day)):
            for j in range(len(town_results_by_day[i])):
                t = town_results_by_day[i][j]
                m = maf_results_by_day[i][j]
                if t+m == 0:
                    print("----",end="  ")
                    self.combined_results_by_day[i][j] = -1
                else:
                    self.combined_results_by_day[i][j] = t/(t+m)
                    print("%3.2f"%(self.combined_results_by_day[i][j]),end="  ")
            print("")
        if(graph):
            self.drawGraph()

    def drawGraph(self):
        ax = plt.axes(projection='3d')
        zline = []
        yline = []
        xline = []
        for i,row in enumerate(self.combined_results_by_day):
            for j,cell in enumerate(row):
                if(cell > 0 and j > 0):
                    zline.append(cell)
                    xline.append(i)
                    yline.append(j)
        ax.scatter(xline, yline, zline,c=zline,cmap='cool')

        # Data for three-dimensional scattered points
        # ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='Greens')
        plt.show()
