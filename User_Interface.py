# Modules for Tkinter
import tkinter as Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Modules for Image and number processing
import numpy as np
from PIL import ImageTk,Image,ImageSequence

# Importing files to display graphs
import Simulator.Simulator as Simu
import mapping as bmap
import bar_chart_race as bgraph



class Application(Tk.Tk):
    def __init__(self):
        Tk.Tk.__init__(self)
        self.resizable(0, 0)
        self.title("COVID-19 Application")
        self.geometry("250x250")
        self.f = None
        self.changef(MainPage)
        
    def changef(self, f_c):
        """
        Destroys current frame and replaces it with a new one
        """
        n_f = f_c(self)
        if self.f is not None:
            self.f.destroy()
        self.f = n_f
        self.f.pack()
        
class MainPage(Tk.Frame):
    def __init__(self, master):
        Tk.Frame.__init__(self, master)
        self.master.geometry("250x250")
        Tk.Label(self, text="COVID-19 Application").pack(side="top", fill="x", pady=10)
        Tk.Button(self, text="Simulation", command=lambda: master.changef(SimPage)).pack()
        Tk.Button(self, text="Choropleth Map", command=lambda: master.changef(Choropleth_Map)).pack()
        Tk.Button(self, text="Bar Chart", command=lambda: master.changef(Bar_Plot)).pack()
        

class SimPage(Tk.Frame):
    def __init__(self, master):
        Tk.Frame.__init__(self, master)
        # self.master.geometry("500x500")
        self.InfectP = Tk.IntVar()
        self.InfectP.set(90)
        self.ImmuneP = Tk.IntVar()
        self.ImmuneP.set(50)
        self.DeadP = Tk.IntVar()
        self.DeadP.set(10)


        F1 = Tk.Frame(self)
        F1.pack(fill="x")
        InfectL = Tk.Label(F1, text="Infect Probability (%)")
        InfectL.pack(side="left", padx=5, pady=5)
        InfectE = Tk.Spinbox(F1, width=10, from_=0, to=100, textvariable = self.InfectP)
        InfectE.pack(side="right", padx=5)

        F2 = Tk.Frame(self)
        F2.pack(fill="x")
        ImmuneL = Tk.Label(F2, text="Immune Probability (%)")
        ImmuneL.pack(side="left", padx=5, pady=5)
        ImmuneE = Tk.Spinbox(F2, width=10, from_=0, to=100, textvariable = self.ImmuneP)
        ImmuneE.pack(side="right", padx=5)

        F3 = Tk.Frame(self)
        F3.pack(fill="x")
        DeadL = Tk.Label(F3, text="Death Probability (%)")
        DeadL.pack(side="left", padx=5, pady=5)
        DeadE = Tk.Spinbox(F3, width=10, from_=0, to=100, textvariable = self.DeadP)
        DeadE.pack(side="right", padx=5)

        self.allstuff = [self.DeadP, self.ImmuneP, self.InfectP]
        
        Tk.Button(self, text="Start Simulation", command=self.runsim).pack()

        Tk.Button(self, text="Return to Home Page", command=lambda: master.changef(MainPage)).pack()
    def runsim(self):
        def percentage_to_probability(x):
            x = (x.get()/100)
            return x

        numberOFpeople = 100
        radius = np.array([0.03 for i in range(numberOFpeople)])

        #The is passed when creating the players to make all the players healthy/grey
        c0l0r = {"edgecolor": "black", "linewidth": 1, "fill": True, "facecolor":"grey"}
        if self.num_check() == True:
            infect_probability = percentage_to_probability(self.InfectP)
            recover_probability = percentage_to_probability(self.ImmuneP)
            death_probability = percentage_to_probability(self.DeadP)
            
            sim = Simu.Simulation(numberOFpeople, infect_probability, recover_probability, death_probability, radius, c0l0r)
            sim.do_animation()    
        
        #Default values for the 
        # infect_probability = 90
        # infect_probability = percentage_to_probability(infect_probability)
        # recover_probability = 70
        # recover_probability = percentage_to_probability(recover_probability)
        # death_probability = 1
        # death_probability = percentage_to_probability(death_probability)

    def num_check(self):    
        try:
            A = self.InfectP.get()
            B = self.ImmuneP.get()
            C = self.DeadP.get()
        except:
            Tk.messagebox.showinfo('Error', 'Only Numbers are accepted')
            return False
        return True
                


class Choropleth_Map(Tk.Frame):
    def __init__(self, master):
        Tk.Frame.__init__(self, master)
        self.master.geometry("900x750")
        
        Tk.Label(self, text="Choropleth Map").pack(side="top", fill="x", pady=10)
        
######################################################################
        bmap.create_choropleth()
        cmap = Tk.Frame(self)
        cmap.pack()
        displayonTK("bristol_covid_map.gif", cmap)
####################################################################

        Tk.Button(self, text="Return to Home Page",
                  command=lambda: master.changef(MainPage)).pack()

class Bar_Plot(Tk.Frame):
    def __init__(self, master):
        Tk.Frame.__init__(self, master)
        self.master.geometry("900x750")
        Tk.Label(self, text="Bar chart").pack(side="top", fill="x", pady=10)
        
######################################################################
        bgraph.genBarChart()
        bplot = Tk.Frame(self)
        bplot.pack()
        displayonTK("bar_chart.gif", bplot)
####################################################################

        Tk.Button(self, text="Return to Home Page",
                  command=lambda: master.changef(MainPage)).pack()



class displayonTK():
    def __init__(self, location, frm):
        self.location = location
        self.frm = frm
        self.showonTK(location)
    def showonTK(self,location):
        z=300
        x=3*z
        y=2*z
        
        self.canvas= Tk.Canvas(self.frm, width=x, height=y)
        self.canvas.pack()
    
        img = Image.open(self.location)
        self.seq = []
        for img in ImageSequence.Iterator(img):
            img = img.resize(((x),(y)))
            img = ImageTk.PhotoImage(img)
            self.seq.append(img)
        
        self.num = Tk.StringVar()
        
        self.img_list = self.canvas.create_image(0,0, anchor="nw",image=self.seq[0])
        weekNo = Tk.Label(self.frm, textvariable=self.num).pack()
        self.w = Tk.Scale(self.frm, from_=0, to=len(self.seq)-1, orient="horizontal", command=self.slide_update, length=800)
        self.w.pack()
        
    def slide_update(self, val):
        self.num.set(f"Frame {val}")
        self.canvas.itemconfig(self.img_list,image=self.seq[int(val)])


#if __name__ == "__main__":
#    UI = Application()
#    UI.mainloop()

def runUI():
    UI = Application()
    UI.mainloop()
    
#runUI()
