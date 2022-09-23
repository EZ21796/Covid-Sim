import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
from itertools import combinations
# To Display graphs on Tkinter window
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as Tk




class Person:
    """
    Class to create a  Person.
    """
    def __init__(self, key, x, y, vx, vy, stat, r, c0l0r):

        self.key = key
        self.location = np.array((x, y))
        self.velocity = np.array((vx, vy))
        self.r = r
        self.mass = (self.r**2)
        self.stat = stat
        self.c0l0r = c0l0r

    # https://stackoverflow.com/questions/2627002/whats-the-pythonic-way-to-use-getters-and-setters
    # http://docs.python.org/library/functions.html?highlight=property#property
    @property
    def ID(self):
        return self.key
    
    @property
    def status(self):
        return self.stat
    @status.setter
    def status(self, value):
        self.stat = value
    # To get values for position and velocity
    @property
    def x(self):
        return self.location[0]
    @property
    def y(self):
        return self.location[1]
    @property
    def vx(self):
        return self.velocity[0]
    @property
    def vy(self):
        return self.velocity[1]
      
    # To set values for position and velocity
    @x.setter
    def x(self, value):
        self.location[0] = value
    @y.setter
    def y(self, value):
        self.location[1] = value
    @vx.setter
    def vx(self, value):
        self.velocity[0] = value
    @vy.setter
    def vy(self, value):
        self.velocity[1] = value
        
        
    def move(self, tik):
        """
        Moves the Person's position forward in time by tik.
        """
        self.location += tik * self.velocity 

    def plot_person(self, sim_graph):
        """
        Plots this Person on sim_graph.
        """
        circle = Circle(xy=self.location, radius=self.r, **self.c0l0r)
        sim_graph.add_patch(circle)
        return circle

    def infected(self):
        """
        Changes color of the infected person to Green
        """
        self.c0l0r = {"edgecolor": "black", "linewidth": 1, "fill": True, "facecolor":"green"}


    def on_top(self, other):
        """
        Checks if this Person is on top of another person
        """
        return np.hypot(*(self.location - other.location)) < self.r + other.r

    
    
class Simulation:
    """
    A class for the Simulation of poeple and graph.
    """

    PersonClass = Person
    healthy_list = []
    infected_list = []
    immune_list = []
    dead_list = []

    def __init__(self, population, infect_probability, recover_probability, death_probability, radius, c0l0r):
        """
        Starts the simulation with all the population with radius radius.
        """
        self.init_particles(population, radius, c0l0r)
        self.tik = 0.01
        self.num_healthy = 99
        self.num_infected = 1
        self.num_immune = 0
        self.num_dead = 0
        self.x1, self.listOFhealthy, self.listOFinfected, self.listOFimmune, self.listOFdead = [],[],[],[],[]
        #self.infected_list
        self.timer = 0
        self.timeTOsave = 0
        self.infect_probability = infect_probability
        self.recover_probability = recover_probability
        self.death_probability = death_probability
        
        
        
    def place_Person(self, radius1, c0l0r, key):
        """
        Positions and velocities are chosen randomly, if a generated position overlaps
        with another person on the gird a new position is generated.
        """
        
        # Generates random x, y so that the person is inside the grid
        x = radius1 + (1 - 2*radius1) * np.random.random()
        y = radius1 + (1 - 2*radius1) * np.random.random()
        # Generates a random velocity for the Person (low enough so the players dont merge into each other or move out of the gird between frames).
        constant = 0.05 + (np.sqrt(np.random.random())*0.1)
        #constant = 0.1 * np.sqrt(np.random.random()) + 0.1  for faster movement
        random_hypo = (np.random.random()*6)
        # Using the Hypotenuse generates x and y velocities
        vx = constant * np.cos(random_hypo)
        vy = constant * np.sin(random_hypo)
        stat = "healthy"
        player = self.PersonClass(key, x, y, vx, vy, stat, radius1, c0l0r)
        # Check that the person doesn't overlap with one that"s already been placed.
        #print(f"Location:({x},{y})")
        #print(f"Velocity{player.vx}, {player.vy}")
        for person in self.people:
            if person.on_top(player):
                break
        else:
            self.people.append(player)
            return True
        return False

    def init_particles(self, population, radius, c0l0r):
        """
        Generates the people for the simulation.
        """

        self.population = population
        self.people = []
        for i, radius1 in enumerate(radius):
            key = i
            # Try to find a random initial position for this person.
            while not self.place_Person(radius1, c0l0r, key):
                #print("person added")
                pass
        self.start_infection()


    def calculate_V(self, p1, p2):
        """
        Changing the person"s velocity when they touch another person"
        """
        
        mass1 = p1.mass
        total_mass = mass1*2
        location1, location2 = p1.location, p2.location
        velocity1, velocity2 = p1.velocity, p2.velocity
        d = np.linalg.norm(location1 - location2)**2
        final_V1 = velocity1 - total_mass /total_mass* np.dot(velocity1-velocity2, location1-location2) / d * (location1 - location2)
        final_V2 = velocity2 - total_mass /total_mass* np.dot(velocity2-velocity1, location2-location1) / d * (location2 - location1)
        p1.velocity = final_V1
        p2.velocity = final_V2
        #p1.velocity, p2.velocity = p2.velocity ,p1.velocity
        
    def start_infection(self):
        """
        Clears the lists and infects a random person in the simulation
        """
        
        self.healthy_list.clear()
        self.infected_list.clear()
        self.immune_list.clear()
        self.dead_list.clear()
        
        for i in self.people:
            self.healthy_list.append(i)
            # i.status = "healthy"
        # Infects a random person
        
        c = np.random.randint(1,self.population)
        self.people[c].infected()
        self.people[c].status = "infected"
        self.healthy_list.remove(self.people[c])
        self.infected_list.append(self.people[c])
        
    def infect_others(self, p1, p2):
        """
        If one of the person is infected the other person has a chance of getting infected
        and updates the numbers accordingly to plot the line graph
        """
        if p1.status != p2.status:
            if ((p1.status) == "infected") or ((p2.status) == "infected"):
                random_prob = np.random.random()
                if ((p1.status) == "infected") and ((p2.status) == "healthy"):
                    if self.infect_probability > random_prob:
                        self.circles[p2.key].set_facecolor("green")
                        self.healthy_list.remove(p2)
                        # self.num_infected = self.num_infected + 1
                        # self.num_healthy = self.num_healthy - 1
                        self.infected_list.append(p2)
                        p2.status = "infected"
                        # print(f"person ID {p2.key} and status is {p2.status}")
                elif ((p2.status) == "infected") and ((p1.status) == "healthy"):
                    if self.infect_probability > random_prob:
                        self.circles[p1.key].set_facecolor("green")
                        self.healthy_list.remove(p1)
                        # self.num_infected = self.num_infected + 1
                        # self.num_healthy = self.num_healthy - 1
                        self.infected_list.append(p1)
                        p1.status = "infected"
                        # print(f"person ID {p1.key} and status is {p1.status}")

                    
    def change_status(self):
        """
        We are checking if 2 players collide and pairing them up 
        to change their status accordingly
        """ 
        pairs = combinations(range(self.population), 2)
        for a,b in pairs:
            if self.people[a].on_top(self.people[b]):
                self.infect_others(self.people[a], self.people[b])
        if self.timer == 10:
            # print(f"after {self.timer} frames")
            self.timer = 0
            # Every day picks random people from the infected list to recover and/or kill them
            #  (10 frames = 1 day)
            if len(self.infected_list) > 10:
                if self.recover_probability > np.random.random():
                    random_num = np.random.randint(1,3)
                    for i in range(random_num):
                        recovered_person = np.random.choice(self.infected_list)
                        # print("A person recovered")
                        self.infected_list.remove(recovered_person)
                        self.immune_list.append(recovered_person)
                        self.circles[recovered_person.key].set_facecolor("blue")
                        recovered_person.status = "immune"
                        # self.num_infected = self.num_infected - 1
                        # self.num_immune = self.num_immune + 1
                if self.death_probability > np.random.random():
                    random_num = np.random.randint(1,3)
                    for i in range(random_num):
                        dead_person = np.random.choice(self.infected_list)
                        # print("A person dead")
                        self.infected_list.remove(dead_person)
                        self.dead_list.append(dead_person)
                        self.circles[dead_person.key].set_facecolor("red")
                        dead_person.status = "dead"
                        # self.num_infected = self.num_infected - 1
                        # self.num_dead = self.num_dead + 1

                        
    def p2p_contact(self):
        """
        We are checking if 2 players collide and pairing them up 
        to change their velocities accordingly
        """ 
        pairs = combinations(range(self.population), 2)
        for a,b in pairs:
            if self.people[a].on_top(self.people[b]):
                self.calculate_V(self.people[a], self.people[b])

    def p2b_contact(self, person):
        """
        Making the people stay inside the grid
        by changing their velocities when they touch the boundaries of the grid
        """

        if person.x - person.r < 0:
            person.x = person.r
            person.vx = -person.vx
        if person.x + person.r > 1:
            person.x = 1-person.r
            person.vx = -person.vx
        if person.y - person.r < 0:
            person.y = person.r
            person.vy = -person.vy
        if person.y + person.r > 1:
            person.y = 1-person.r
            person.vy = -person.vy
        

    def update_line_graph(self):
        """
        Updates and return the lines to plot line graph
        """

        self.listOFhealthy.append(len(self.healthy_list))
        self.listOFinfected.append(len(self.infected_list))
        self.listOFimmune.append(len(self.immune_list))
        self.listOFdead.append(len(self.dead_list))
        
        # self.listOFhealthy.append(self.num_healthy)
        # self.listOFinfected.append(self.num_infected)
        # self.listOFimmune.append(self.num_immune)
        # self.listOFdead.append(self.num_dead)
        
        self.hline.set_data(self.x1, self.listOFhealthy)
        self.inline.set_data(self.x1, self.listOFinfected)
        self.imline.set_data(self.x1, self.listOFimmune)
        self.dline.set_data(self.x1, self.listOFdead)
        return self.hline, self.inline, self.imline, self.dline
        



    def advance_animation(self):
        """
        Moves the animation by tik, returning the updated Circles list.
        """
        for a, b in enumerate(self.people):
            b.move(self.tik)
            self.p2b_contact(b)
            self.circles[a].center = b.location

        self.p2p_contact()
        self.change_status()
        return self.circles


    def init(self):
        """
        Draws the Matplotlib animation.
        """
        self.circles = []
        for particle in self.people:
            self.circles.append(particle.plot_person(self.sim_graph))
        return self.circles


    def setup_animation(self):
        """
        Draws the simulation grid, the line graph and opens the tkinter window
        """
        #Figure with 2 subplots
        self.fig = plt.figure(figsize=(8, 4))
        self.sim_graph = self.fig.add_subplot(1, 2, 1)
        self.line_graph = self.fig.add_subplot(1, 2, 2)
        
        # Simulation Graph 
        self.sim_graph.spines["top"].set_linewidth(3)
        self.sim_graph.spines["bottom"].set_linewidth(3)
        self.sim_graph.spines["left"].set_linewidth(3)
        self.sim_graph.spines["right"].set_linewidth(3)
        self.sim_graph.set_aspect("equal", "box")
        self.sim_graph.set_xlim(0, 1)
        self.sim_graph.set_ylim(0, 1)
        self.sim_graph.xaxis.set_ticks([])
        self.sim_graph.yaxis.set_ticks([])
        
        #Line 
        self.line_graph.set_xlim([0, 100])
        self.line_graph.set_ylim([0, 100])
        self.line_graph.set_xlabel("Days")
        self.line_graph.set_ylabel("Number of People")
        self.hline, = self.line_graph.plot([0], [self.num_healthy],color="grey", label = "Healthy") 
        self.inline, = self.line_graph.plot([0], [self.num_infected],color="green", label = "Infected")
        self.imline, = self.line_graph.plot([0], [self.num_immune],color="blue", label = "Immune")
        self.dline, = self.line_graph.plot([0], [self.num_dead],color="red", label = "Dead")
        self.line_graph.legend()
        
        # Creates new window 
        self.root = Tk.Tk()
        self.root.title("Covid Simulator")
        self.root.resizable(0, 0)
        self.label = Tk.Label(self.root,text="COVID Simulation").grid(column=0, row=0)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().grid(column=0,row=1)
        self.fig.tight_layout()


    def animate(self, i):
        """
        FuncAnimation loop.
        """
        self.advance_animation()
        self.timer = self.timer + 1
        self.timeTOsave = self.timeTOsave + 1
        # i/10 because 10 frames = 1 day
        self.x1.append(i/10)
        self.update_line_graph()
        # After a 1000frames/100 days save an image of the simulation and grapg
        if self.timeTOsave == 1000:
            self.save_file(self.anime)
            #Stops animation after 1000 frames 
            self.anime.event_source.stop()
            #print("It has been 100 days")

        lines = [self.hline, self.inline, self.imline, self.dline]
        self.patches = lines + list(self.circles)
        # if self.timeTOsave == 0 :
        #     for x in self.patches:
        #         x.clear()      
        return self.patches


    

    
    def save_file(self, anima):
        """
        Saves the image of the simulation and the line graph
        """
        self.fig.savefig("image.png")
        #anima.save("video.gif")
        print("saving file")


    def do_animation(self, interval=1):
        """
        Set up and carry out the simulation
        """
        self.setup_animation()
        self.anime = FuncAnimation(self.fig, self.animate, save_count = 1000,
                                      interval=1, blit=True, init_func=self.init, repeat=False)
        Tk.mainloop()
        #self.anime.save("video.gif")
   

#Numbers and sizes
# people = 100
# grid size = 1X1
# radius = 0.03

def percentage_to_probability(x):
    z = (x/100)
    return z

numberOFpeople = 100
radius = np.array([0.03 for i in range(numberOFpeople)])

#The is passed when creating the players to make all the players healthy/grey
c0l0r = {"edgecolor": "black", "linewidth": 1, "fill": True, "facecolor":"grey"}

# #Values for the Probabilities
# infect_percentage = 90
# infect_probability = percentage_to_probability(infect_percentage)
# recover_percentage = 70
# recover_probability = percentage_to_probability(recover_percentage)
# death_percentage = 1
# death_probability = percentage_to_probability(death_percentage)

