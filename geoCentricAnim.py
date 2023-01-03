import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter

# Basic gravitational prediction engine
# By Avram Silberztein

import math

import matplotlib.pyplot as plt
import numpy as np


#Initial objects
#x, y, z, velocity, mass
class Planet:
    def __init__(self, name, x, y, z, v_x, v_y, v_z, mass, r):
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.v_x = v_x
        self.v_y = v_y
        self.v_z = v_z
        self.mass = mass
        self.r = r
    
    def update_position(self, Δpositions): 
        self.x = Δpositions[0]
        self.y = Δpositions[1]
        self.z = Δpositions[2]    # 
    def update_velocity(self, Δvelocities): 
        self.v_x = Δvelocities[0]
        self.v_y = Δvelocities[1]
        self.v_z = Δvelocities[2]
time_year = 365.25*24*3600
# v_y_earth = (2*math.pi * 1.9891*10**30 )/(time_year)**2
# v_y_moon = (2*math.pi * 384 * 10**6 )/(27*24*3600 + 7*3600 + 43*60 )**2 + v_y_earth 
# v_y_earth = 20000
# v_y_moon = v_y_earth 
v_y_earth = (2 * math.pi * 149 * 10**9)/time_year 
# v_y_moon = v_y_earth  + (2 * math.pi * 384 * 10**6)/(27*24*3600 + 7*3600 + 43*60)

#intial_v_y(5.9736 * 10**24, time_year)

def intial_v_y(R, T):
   return (2 * math.pi * R)/T


    #       name     x          y         z        v_x     v_y     v_z     mass      radius
p_sun = Planet("sun"  , 0          , 0       , 0      , 0     , 0    , 0      , 1.9891*10**30  ,  1 )
p_jupyter = Planet("jupyter"  , 483600000 * 1.60934 * 1000         , 0       , 0      , 0     , intial_v_y(   483600000 * 1.60934 * 1000, 142*(time_year/12))  , 0      , 1.8986*10**27  ,  1 )
p_saturn = Planet("saturn"  , 886500000 * 1.60934 * 1000          , 0       , 0      , 0     , intial_v_y( 886500000 * 1.60934 * 1000, 354*(time_year/12))     , 0      , 5.6846 * 10**26  ,  1 )
    # Planet("neptune"  , 0          , 0       , 0      , 0     , 0     , 0      , 10.243 * 10**25  ,  1 )
    # Planet("uranus"  , 0          , 0       , 0      , 0     , 0     , 0      , 8.6810 * 10**25  ,  1 )
p_earth = Planet("earth"  , 149 * 10**9          , 0       , 0      , 0     , intial_v_y(149 * 10**9, time_year)      , 0      , 5.9736 * 10**24  ,  1 )
    # Planet("venus"  , 0          , 0       , 0      , 0     , 0     , 0      , 4.8685 * 10**24  ,  1 )
    # Planet("mars"  , 0          , 0       , 0      , 0     , 0     , 0      , 6.4185 * 10**23  ,  1 )
    # Planet("mercury"  , 0          , 0       , 0      , 0     , 0     , 0      , 3.3022 * 10**23  ,  1 )
p_moon = Planet("moon"  , (149 * 10**9) + (384.4 * 10**6)       , 0       , 0      , 0, intial_v_y(149 * 10**9, time_year) + intial_v_y(384.4 * 10**6, 27*24*3600 + 7*3600 + 43*60)      , 0      , 7.34767309 * 10**22 ,  1 )


c_30 = math.cos(math.radians(30))
c_60 = math.cos(math.radians(60))
dist_3b  = 10**4
m_3b = 10**8
p_3b_1 = Planet("3b_1", 0, dist_3b, 0, 0, 0, 0, m_3b, 1)
p_3b_2 = Planet("3b_2", c_30*dist_3b, -c_60*dist_3b, 0, 0, 0, 0, m_3b, 1)
p_3b_3 = Planet("3b_3", -c_30*dist_3b, -c_60*dist_3b, 0, 0, 0, 0, m_3b, 1)







planet_list = [p_sun, p_earth]
time_step =  10**4
final_time = 2 * 10**7 
anime_time = 10 #sec
resolution_factor = 100
anime_bool = True
anime_name = "Anim_Sun_Earth"
normal_plot = False
frame_rate = 60












times = list(np.linspace(0, final_time, math.floor(final_time/time_step)+1))
#print(list(np.linspace(0, 100, 1+1)))

time_list_len = len(times)
# 
times_2 = []

G = 6.67408 * 10**(-11)

def newVelocity(t, current_velocity, acceleration):
    return (current_velocity + acceleration*t)
def newPosition(t, position, velocity, acceleration):
  return (position + velocity*t + (acceleration/2)*t**2)

def distBodies(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2)
    
    
def gAcceleration(M, R):
    #G = 6.67408 * 10**(-11) 
    G = 6.67 * 10**(-11) 
    if R == 0:
        return 0
    else:
        if R > 0:
            return (G * M) / R**2
        elif R < 0:
            return -(G * M) / R**2



num_bodies = len(planet_list)

# for planet in planet_list:
#    plt.plot(planet.x, planet.y, "ro")



graph_planet = "earth"

graph_x, graph_y, graph_z, graph_v_x, graph_v_y, graph_v_z = [], [], [], [], [], []
pos_all = []
vel_all = []
acc_all = [] #looks like: {t1 : [[p1,x, p1.y, p1.z], [p2.x, p2.y, p2.z], ...], t2 : [p1, p2, ...], ...  ]}

for i in range(len(planet_list)):
   pos_all.append([])
   vel_all.append([])
   acc_all.append([])
# print(pos_all)
# print(vel_all)
# print(acc_all)

temp_x_list = []
exploded = False

for t in times:
    #print("AAAAAAAAAA", t)
    
    if exploded:
        
        break
    new_info_dict = {}
    for mainPlanet in planet_list:
        #print("start of", mainPlanet.name)
        new_info_dict[mainPlanet.name] = []
        acceleration_net_x = 0 
        acceleration_net_y = 0 
        acceleration_net_z = 0 
        for planet in planet_list:
            if mainPlanet.name == planet.name:
                continue
            #print("calculation of planet:", planet.name)

            R = math.sqrt((planet.x - mainPlanet.x)**2 + (planet.y - mainPlanet.y)**2 + (planet.z - mainPlanet.z)**2)

            acceleration_net_temp = gAcceleration( planet.mass, R)
            acceleration_net_x_temp = acceleration_net_temp * (abs(planet.x - mainPlanet.x)/R) 
            acceleration_net_y_temp = acceleration_net_temp * (abs(planet.y - mainPlanet.y)/R) 
            acceleration_net_z_temp = acceleration_net_temp * (abs(planet.z - mainPlanet.z)/R) 

            # print("accel test  PppPppPppPppPppPppPppPppPppPppPpp")
            # print(acceleration_net_temp)
            # print(acceleration_net_x_temp + acceleration_net_y_temp + acceleration_net_z_temp)

            if planet.x  < mainPlanet.x:
               acceleration_net_x_temp = -acceleration_net_x_temp
            if planet.y < mainPlanet.y:
               acceleration_net_y_temp = -acceleration_net_y_temp
            if planet.z  <  mainPlanet.z:
               acceleration_net_z_temp = -acceleration_net_z_temp

            acceleration_net_x += acceleration_net_x_temp
            acceleration_net_y += acceleration_net_y_temp
            acceleration_net_z += acceleration_net_z_temp



            # if abs(planet.x - mainPlanet.x) < (planet.r + mainPlanet.r):
            #     print("x explosion")

            # print("planet distance", abs(planet.x - mainPlanet.x), "radius sum ",(planet.r + mainPlanet.r))
     
            # if abs(planet.y - mainPlanet.y) < (planet.r + mainPlanet.r):
            #     print("y explosion")
            # if abs(planet.z - mainPlanet.z) < (planet.r + mainPlanet.r):
            #     print("z explosion")

            # if abs(planet.x - mainPlanet.x) < (planet.r + mainPlanet.r):
            #     if abs(planet.y - mainPlanet.y) < (planet.r + mainPlanet.r):
            #         if abs(planet.z - mainPlanet.z) < (planet.r + mainPlanet.r):
            #             print("EXPLOSION")
            #             exploded = True



        #     print("ACCEL from ", planet.name)
        #     print("total accel x", acceleration_net_x)
        # print("total accel x", acceleration_net_x)
        # print("y", acceleration_net_y)
        # print("z", acceleration_net_z)
            

        v_x_new = newVelocity(time_step, mainPlanet.v_x, acceleration_net_x)
        v_y_new = newVelocity(time_step, mainPlanet.v_y, acceleration_net_y)
        v_z_new = newVelocity(time_step, mainPlanet.v_z, acceleration_net_z)

        new_velocities_list = [v_x_new, v_y_new, v_z_new]


        x_new  = newPosition(time_step, mainPlanet.x, mainPlanet.v_x, acceleration_net_x)
        y_new  = newPosition(time_step, mainPlanet.y, mainPlanet.v_y, acceleration_net_y)
        z_new  = newPosition(time_step, mainPlanet.z, mainPlanet.v_z, acceleration_net_z)

        new_positions_list = [x_new, y_new, z_new]

        
       
        index = 0

        for i in range(len(planet_list)):

         if planet_list[i].name == mainPlanet.name:
            index = i
            break 
         

        
        pos_all[index].append(new_positions_list)
        vel_all[index].append(new_velocities_list)


    for i in range(len(planet_list)):
        #print("updating", planet_list[i].name, i)
        # print(pos_all)
        # print(vel_all)
        
        planet_list[i].update_position(pos_all[i][-1])
        planet_list[i].update_velocity(vel_all[i][-1])
    times_2.append(t)

#print("velocities list", vel_all)
 
x_times_graph = []
for h in pos_all[0]:
   x_times_graph.append(h[0])

y_times_graph = []
for h in pos_all[0]:
   y_times_graph.append(h[1])

v_x_times_graph = []
for h in vel_all[0]:
   v_x_times_graph.append(h[0])
   

v_y_times_graph = []
for h in vel_all[0]:
   v_y_times_graph.append(h[1])

#print("x_times_graph", x_times_graph)
# print("--------")
# print(times_2)
# print("--------")


# plt.show()
# plt.plot(v_x_times_graph, v_y_times_graph)

if normal_plot:
    for i in range(len(planet_list)):
        print(i)
        plt.plot([h[0] for h in pos_all[i]], [h[1] for h in pos_all[i]])
    plt.show()
   



if anime_bool == False:
    print("yo")
    exit()






#!PLOTTING
color_list = ['k', 'b', 'g', 'y', 'r', 'p']
fig = plt.figure()
# l, = plt.plot([], [], 'k-')
# l2, = plt.plot([], [], 'm--')
# p1, = plt.plot([], [], 'ko')
# p2, = plt.plot([], [], 'mo')

plt_list = []


 


#! REMOVE TEMP
#num_bodies = 1


for i in range(num_bodies):
    plt_temp, = plt.plot([], [], color_list[i] + '-')
    plt_list.append(plt_temp)

plt.xlabel('x')
plt.ylabel('y')
plt.title('Gravity Simulation')

x_lim_low = min([min([x[0] for x in pos_all[i]]) for i in range(num_bodies)])
x_lim_high =  max([max([x[0] for x in pos_all[i]]) for i in range(num_bodies)])
y_lim_low = min([min([x[1] for x in pos_all[i]]) for i in range(num_bodies)])
y_lim_high =  max([max([x[1] for x in pos_all[i]]) for i in range(num_bodies)])

v_lim_low = min(x_lim_low, x_lim_high) -  abs(min(x_lim_low, x_lim_high) * 0.05)
v_lim_high = max(x_lim_low, x_lim_high) + abs(max(x_lim_low, x_lim_high) * 0.05)


plt.xlim(v_lim_low, v_lim_high)
plt.ylim(v_lim_low, v_lim_high)


num_of_frames = frame_rate * anime_time
# mod_num = time_list_len/num_of_frames
# print("MOD NUM", mod_num)
# mod_num = int(mod_num)
choosen_frame_list = list(np.linspace(0, time_list_len, num_of_frames))
choosen_frame_list = [int(x) for x in choosen_frame_list]

metadata = dict(title='Movie')
writer = PillowWriter(fps=frame_rate, metadata=metadata)


xlist = []
xlist2 = []
ylist = []
ylist2 = []

with writer.saving(fig, anime_name + ".gif", resolution_factor):

    # Plot the first line and cursor
    #for j in range(len(planet_list)):
    x_list = []
    y_list = []
    for i in range(num_bodies):
        x_list.append([])
        y_list.append([])
    f_c = 0
    for j in range(time_list_len):
        for i in range(num_bodies):
            plt_tM = plt_list[i]
            x_list[i].append(pos_all[i][j][0])
            y_list[i].append(pos_all[i][j][1])

            plt_tM.set_data(x_list[i],y_list[i])

        if j in choosen_frame_list: 
            f_c += 1
            print("f_c", f_c)   
            writer.grab_frame()
        print("anime", j)

    # plot the second line and cursor
    # for xval in np.linspace(-5,5,100):
    #     xlist2.append(xval)
    #     ylist2.append(func2(xval))

    #     l.set_data(xlist,ylist)
    #     l2.set_data(xlist2,ylist2)

    #     p2.set_data(xval,func2(xval))

    #     writer.grab_frame()