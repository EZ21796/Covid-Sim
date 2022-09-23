import argparse
from Simulator import Simulator
import numpy as np
import mapping
import User_Interface
import bar_chart_race

#Creating the parser and adding arguments
parser = argparse.ArgumentParser(prog= 'main',
                                 description= ("""
           ,'/ \`.
          |\/___\/|
          \'\   /`/
           `.\ /,'
              |
              |
             |=|
        /\  ,|=|.  /\
            
     '`.  \/ |=| \/  ,'`.
  ,'    `.|\ `-' /|,'    `.
,'   .-._ \ `---' / _,-.   `.
   ,'    `-`-._,-'-'    `.
  '                       `'
  Controllable -sim Variables (All 0-100)"""),epilog='Happy Infecting!',formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('-UI', action='store_true', help='Opens GUI')
parser.add_argument('-map', action='store_true', help='Creates choropleth map .gif ')
parser.add_argument('-bar', action='store_true', help='Creates bar chart race .mp4')
parser.add_argument('-sim', action='store_true', help='Runs simulation. You can either use defualt values or select them individually using, -contagiousness, -recovery, -deadliness')


parser.add_argument('-con','--contagiousness', type=int,action='store',default=90,
                    dest='infect_percentage',
                    help='(default 90, [0-100])The chance of contracting the virus upon contact',)
parser.add_argument('-rec','--recovery', type=int,action='store',default=50,
                    dest='recover_percentage',
                    help='(default 70, [0-100])The chance a person recovers from the virus, lower values increase the time taken to fight off the virus')
parser.add_argument('-dead','--deadliness', type=int,action='store',default=10,
                    dest='death_percentage',
                    help= '(default 1, [0-100])The chance a person dies as a result of the virus, RIP :(')
args = parser.parse_args()


#Checking if the argument values entered are valid
virus_param_dictionary=vars(args)
virus_param_list = list(virus_param_dictionary.values())
for i in virus_param_list:
    if i<0 or i>100:
        raise argparse.ArgumentTypeError('Make sure the your virus has parameter values in the range 0-100')

def percentage_to_probability(x):
    z = (x/100)
    return z

numberOFpeople = 100
radius = np.array([0.03 for i in range(numberOFpeople)])

#The is passed when creating the players to make all the players healthy/grey
c0l0r = {"edgecolor": "black", "linewidth": 1, "fill": True, "facecolor":"grey"}
def sim_in_arg():
    infect_probability = percentage_to_probability(args.infect_percentage)
    recover_probability = percentage_to_probability(args.recover_percentage)
    death_probability = percentage_to_probability(args.death_percentage)
    Sim = Simulator.Simulation(numberOFpeople, infect_probability, recover_probability, death_probability, radius, c0l0r)
    Sim.do_animation()

#Mutually exclsuive events
while True:
    if (args.sim and (args.map or args.bar or args.UI)) or (args.map and (args.sim or args.bar or args.UI)) or (args.bar and (args.map or args.sim or args.UI) or (args.UI and (args.sim or args.map or args.bar))):
        raise argparse.ArgumentTypeError('Please selct only one of: -UI -sim -map -bar ')
        break
    if args.UI == True:
        User_Interface.runUI()
        break
    if args.sim == True:
        print(vars(args)) #shows values of arguments in command line
        sim_in_arg()
        break
    if args.map == True:
        mapping.create_choropleth()
        break
    if args.bar == True:
        bar_chart_race.genBarChart()
        break
    else:
        raise argparse.ArgumentTypeError('please enter a valid mode')
        break
