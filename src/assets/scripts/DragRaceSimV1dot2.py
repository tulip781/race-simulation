# -*- coding: utf-8 -*-
"""
UROP Kart Drag Race Simulator

This tool was created by Dimitrios Panagiotopoulos as part of a 2021 UROP with Dr. Alexis Ihracska.
The purpose of the tool is to help students intuitively understand the effects of various transmission
and vehicle parameters (most importantly the Gear Ratio) on the performance of a kart. 

(!) This script is for the interactive game component, where you try to figure out
what gear ratio is needed for a random track length
"""

#import the libraries needed for this script

import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as sc
import os
import random


#simulation function
#inputs are gear ratio, time domain, parameters dictionary, and drag race distance

#for simplicity, this version assumes an initial velocity of zero (i.e. standing start)

def simulate(GR, t, parameters, distance, initialVel = 0):
    #intiliaze simulated data arrays
    
    # for loop to calculate acceleration in time domain
    v = np.zeros(len(t)) #initialize car speed
    c = np.zeros(len(t))
    Fr = np.zeros(len(t))
    Fd = np.zeros(len(t))
    Ft = np.zeros(len(t))
    a = np.zeros(len(t))
    d = np.zeros(len(t))
    
    #input and output shaft speed
    w1 = np.zeros(len(t))
    w2 = np.zeros(len(t))
    
    eng = np.zeros(len(t))
    
    #initial kart velocity in m/s
    #assumed 0 in this version
    v[0] = initialVel*(1000/(60*60)) #m/s
    
    #use initial kart velocity to set an initial output shaft rotation speed
    w2[0] = v[0]/(0.2794*0.5) * (60/(2*3.14))
    w1[0] = w2[0] * GR
        
    #idling engine speed (RPM)
    eng[0] = 2200
    
    #set engine speed maximum limit (based on experimental data)
    maxRpm = 6960
    
    #iterate over the time domain to solve the differential equation
    #(force balance in each time step to figure out the acceleration of the kart)

    for i in range(0,len(t)-1):
        
        #calculate rolling resistance (speed in km/h)
        c[i+1] = 0.005 + (1/parameters['p'])*(0.01+0.0095*((v[i]*3.6)/100)**2)
        Fr[i+1] = c[i]*parameters['m'] * parameters['g']
        Fd[i+1] = 0.5*parameters['rho']*parameters['Cd']*parameters['A']*(v[i]**2)
        
        #torque for each engine speed using engine power curves
        Teng = Tinterp(eng[i])

        #torque on rear axle sprocket multiplied by the gear ratio
        Tout = Teng * parameters['tEff'] * GR
        
        #force transmitted to the rear wheels via rear axle
        Ft[i+1] = Tout/parameters['wheelr']
        
        #calculate instantaneous acceleration
        #engine speed cannot exceed its maximum limit
        #at max engine speed the car is assumed to stop accelerating
        if w1[i] < maxRpm:
            a[i+1] = 1/(parameters['lm']*parameters['m']) * (Ft[i+1] - Fr[i+1] - Fd[i+1])
        else:
            a[i+1] = 0
        
        #calculate instantaneous speed change (over dt)
        v[i+1] = v[i] + a[i+1]*dt
        
        #calculate distance travelled (over dt)
        d[i+1] = d[i] + v[i+1]*dt
        
        #calculate rear axle rpm based on vehicle travel speed
        w2[i+1] = v[i+1]/(wheelr) * (60/(2*3.14))
        w1[i+1] = (w2[i+1])*GR
        
        #update new engine speed based on increase in output shaft speed
        #parameter that was tuned to reflect real life behaviour
        alpha = 0.40
        newEngSpeed = eng[i] + alpha*(w1[i+1]-w1[i])
        
        #ensure that engine speed cannot go above max limit
        if newEngSpeed >= maxRpm or w1[i+1] >= maxRpm:
            eng[i+1] = maxRpm
            w1[i+1] = maxRpm
        #if engine speed below maximum, update the engine speed
        else:
            #if clutch not engaged, update the engine RPM as a function
            #proportional to the change in input shaft RPM
            if newEngSpeed > w1[i+1]:
                eng[i+1] = newEngSpeed
            #if clutch is engaged, update the engine RPM with the new
            #input shaft RPM
            else:
                eng[i+1] = w1[i+1]
            
    km = v*3.6
    gs = a/g
    
    #calculate times that car took to travel certian distances
    def find(val, a, b):
        overindex = np.where(a > val) #because it may not be exactly that distance
        firstindex = overindex[0][0]
        return firstindex, b[firstindex] #return first of these indices
    
    #time needed for the distance inputted
    try:
        firstindex, timeDist = find(distance, d, t)
    except:
        print('Time domain not sufficient for a distance of ', str(distance), 'm, increase T_end')
        timeDist = 0
    
    #return time, engine rpm, vehicle speed (km/h), vehicle acceleration (g's),
    #distance (m) and the times taken for each distance (100, 250, 500)
    results = {}
    results['time'] = t
    results['enginerpm'] = eng
    results['speed'] = km
    results['acc'] = gs
    results['dist'] = d
    results['timeDist'] = timeDist
    results['firstIndex'] = firstindex
    results['w1'] = w1
    results['w2'] = w2
    results['Fr'] = Fr
    results['Fd'] = Fd
    results['Ft'] = Ft
    
    return results
    

#vehicle characteristics
#you can experiment changing these as well if you want!

#mass of kart + driver
m = 96.5 + 85 #kg
g = 9.81 #m/s^2 (gravity)
#tyre pressure (not including differences due to tyre temp change)
p = 2.48211 #bar (36 psi)
Cd = 0.5 #coefficient of drag
A = 0.4 #frontal area
wheelr = 0.2794/2 #m #wheelradius

#define gear ratio
G1 = 20 #teeth
G2 = 71 #teeth
GR = G2/G1

#mass factor (approximation, source: ADM yr. 3 course notes)
lm = 1 + 0.04 + 0.0025*(GR**2)

#density of air
rho = 1.23 #kg/m^3

#these are irrelevant to this model
#clutch engagement speed
engagedSpeed = 2000 #RPM
#total drivetrain efficiency (not including clutch) (constant)
tEff = 0.93

#parameters dictionary
parameters = {'m': m, 'g': g, 'p': p, 'Cd': Cd, 'A': A, 'wheelr': wheelr, 'lm': lm, 'rho': rho,
              'engagedSpeed': engagedSpeed, 'tEff': tEff}


#initialize torque curves
rpm = [2000, 2600, 3000, 3500, 4000, 5000, 6000, 6200, 6960]
rpm = np.array(rpm)
trq = [5.0, 13.8, 14.88, 13.7, 12.5, 10.35, 7.3, 6.1, 1.0] #data based on gx160
trq = [5.0, 13.8, 15.0, 14.0, 13.0, 10.35, 7.0, 6.0, 1.0] #data modified to fit track data
trq = np.array(trq)
trq = 2*trq #multiply by 2 cause we have two engines

trq = 1.03*trq #multiplication factor because we are using gx160 data not gx200

#create interpolation function for engine torque to be used in simulate()
minrpm = rpm[0]
maxrpm = rpm[-1]
drpm = 1
irpm = np.arange(minrpm, maxrpm+drpm, drpm)
Tinterp = sc.interp1d(rpm, trq, kind='cubic')
T = Tinterp(irpm)

# #initialize a random track length
# randInt = random.randint(2, 20)
# distance = randInt * 50

#or choose a manual distance, and try different gear ratios
distance = 500
print("Your given drag race distance is: " + str(distance) + "m")

print("Choose a gear ratio to try:")
GR = input()
# #in case you want to manually set a gear ratio
# GR = 3
GR = float(GR)

#initialize domain of simulation
dt = 0.01 #seconds
tend = 50 #seconds
t = np.arange(0,tend+dt,dt)


results = simulate(GR, t, parameters, distance)

#plot results
gridsize = (16, 2)
fig = plt.figure(figsize=(9, 20))
ax1 = plt.subplot2grid(gridsize, (0, 0), colspan=2, rowspan=4)
ax2 = plt.subplot2grid(gridsize, (5, 0), colspan=1, rowspan=2)
ax3 = plt.subplot2grid(gridsize, (5, 1), colspan=1, rowspan=2)
ax4 = plt.subplot2grid(gridsize, (8, 0), colspan=2, rowspan=3)

ax1.minorticks_on()
ax1.grid(which='both', axis='both', alpha=0.3)
ax1.set_title('Kart Speed (km/h) vs Time (s) for a Gear Ratio of ' + str(GR), fontsize=12)
ax1.plot(results['time'], results['speed'])
ax1.set_ylabel('Speed (km/h)')
ax1.set_xlabel('Time (s)')
ax1.plot([results['timeDist'], results['timeDist']], [0, results['speed'][results['firstIndex']]], 
          color='r', linestyle='-', linewidth=2)
ax1.scatter(results['timeDist'], results['speed'][results['firstIndex']], marker='X', s=100, color='r')
ax1.set_ylim([0,results['speed'][-1] + 10])
ax1.set_xlim([0,results['time'][-1] + 2])
ax1.text(35, 40, "Time taken to travel " + str(distance) + "m: ", bbox=dict(facecolor='white', alpha=1, edgecolor='white'))
ax1.text(38, 30, str(np.round(results['timeDist'], 2)) + "s", fontsize=20, bbox=dict(facecolor='white', alpha=1, edgecolor='white'))

ax2.plot(results['time'], results['acc'])
ax2.set_title("Longitudinal Acceleration (G's)")
ax2.set_xlabel('Time (s)')

ax3.plot(results['time'], results['w1'], label="Rear Axle Sprocket")
ax3.plot(results['time'], results['w2'], label="Clutch Sprocket")
ax3.plot(results['time'], results['enginerpm'], label="Engine Speed")
ax3.set_title('Engine and Sprocket Speeds (RPM)')
ax3.legend(framealpha=0.5, fontsize='small', loc='right')
ax3.set_xlabel('Time (s)')

# ax4.plot([0,tend], [0, 0], c='k', alpha=0.2)
ax4.minorticks_on()
ax4.set_xlim([-2,tend+2])
ax4.grid(which='major', axis='both', alpha=0.3)
ax4.plot(results['time'], -1*results['Fr'], label='Rolling Resistance')
ax4.plot(results['time'], -1*results['Fd'], label='Aerodynamic Drag')
ax4.plot(results['time'], results['Ft'], label='Traction Force (Engine)')
ax4.plot(results['time'], results['Ft'] - results['Fr'] - results['Fd'], label='Net Force')
ax4.set_title('Kart Rear Wheel Forces (N)')
ax4.set_xlabel('Time (s)')
ax4.legend(loc="upper right")


# # save plots
# fname = 'demonstrationapp.png'
# pre = os.path.dirname(os.path.realpath(__file__))
# path = os.path.join(pre,fname)
# fig.savefig(path, dpi=300, format='png')



