# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 09:40:27 2019

@author: e.handford
"""
from time import sleep
import matplotlib.pyplot as plt
#The purpose of this script is to calculate the operating temperature of wire
#for use in STM-P0
#DC CURRENTS ONLY

#assumptions:
#ambient air flow at 2ms^-1
#wire surface area >> wire cross sectional area
#wire used is copper
#wire used will not be lower than 0 awg


# user input
awg                            = 20# awg of wire
voltage                        = 50 # voltage (V)
current                        = 8 # current (A)


cruise_current                 = 8


length                         = 10  # length (m)
time                           = 1000 # time (s) - flight time total
takeoff_time                   = 0 # time(s)
# second_takeoff_time            = 15  
max_allowable_temperature_rise = 60 # max allowable temperature rise of wire (K)




# fixed parameters
density                 = 8960          # Kg/m^3 - density of copper
specific_heat_capacity  = 385           # J/Kg.K - specific heat capacity of copper
resistivity             = 1.72*10**-8   # ohm*m  - resistivity of copper

thermal_transmittance   = 40         #thermal transmittance (W)/((m^2)*(K))
#note - a value of 25 is approx a 2ms^-1 ambient air flow of dry air - worst case
#a value of 40 is what is used by RAYCHEM for internal wiring

#calculated parameters
wire_diameter               = 0           #wire diameter in mm
wire_area                   = 0           #wire area in mm^2
resistance_of_wire_per_km   = 0           #wire resistance per km
resistance_of_wire          = 0           #wire resistance in ohms
volume_of_wire              = 0           #wire volume in m^3
mass_of_wire                = 0           #wire mass in Kg
power_loss                  = 0           #power loss through in Watts
wire_circumference          = 0           #wire circumference in m
wire_surface_area           = 0           #wire surface area (m^2)
instantaneous_temp_rise     = 0           #temp rise of wire in a single instance (K)
thermal_dissapation         = 0           #heat dissapation of wire (j)
delta_t                     = 0           #temperature rise of wire (K)


takeoff_current = current



def wire_diameter_cal(awg):
    return 0.127*(92**((36-awg)/39))
        
def wire_area_cal(awg):
    return (0.127*(92**((36-awg)/39)))*(0.127*(92**((36-awg)/39)))*3.14159/4

def resistance_of_wire_per_km_cal(resistivity , wire_area ):
    return 10**9*(resistivity)/wire_area

def resistance_of_wire_cal(resistivity , wire_area , length):
    return length*(10**9*(resistivity)/wire_area)/1000
    
def volume_of_wire_cal(length , wire_area):
    return length*wire_area/1000000

def mass_of_wire_cal(density , volume_of_wire):
    return density*volume_of_wire

def power_loss_cal(resistance_of_wire , current):
    return current*current*resistance_of_wire
    
def wire_circumference_cal(wire_diameter):
    return wire_diameter*3.14159/1000

def wire_surface_area_cal(length , wire_circumference):
    return length*wire_circumference

def instantaneous_temp_rise_cal(time , specific_heat_capacity , mass_of_wire , power_loss):
    return power_loss*time/(specific_heat_capacity*mass_of_wire)

def thermal_dissapation_cal(wire_surface_area , thermal_transmittance , delta_t ):
    return wire_surface_area*thermal_transmittance*delta_t
    
    
wire_diameter = wire_diameter_cal(awg)
print("wire_diameter = " , wire_diameter)

wire_area = wire_area_cal(awg)
print("wire_area = " , wire_area)

resistance_of_wire_per_km = resistance_of_wire_per_km_cal(resistivity , wire_area)
print("resistance of wire per km = " , resistance_of_wire_per_km)

resistance_of_wire = resistance_of_wire_cal(resistivity , wire_area , length)
print("resistance_of_wire" , resistance_of_wire)

volume_of_wire = volume_of_wire_cal(length , wire_area)
print("volume of wire" , volume_of_wire)

mass_of_wire = mass_of_wire_cal(density, volume_of_wire)
print("mass of wire" , mass_of_wire)


power_loss = power_loss_cal(resistance_of_wire , current)
print("power loss" , power_loss)

wire_circumference = wire_circumference_cal(wire_diameter)
print("wire circumference" , wire_circumference)

wire_surface_area = wire_surface_area_cal(length , wire_circumference)
print("wire_surface_area" , wire_surface_area)

instantaneous_temp_rise = instantaneous_temp_rise_cal(time , specific_heat_capacity , mass_of_wire , power_loss)
print("un-adjusted instantaneous_temp_rise" , instantaneous_temp_rise)

thermal_dissapation = thermal_dissapation_cal(wire_surface_area , thermal_transmittance , instantaneous_temp_rise)
print("un-adjusted thermal dissapation" , thermal_dissapation)




time_step = 0.01
time_sum = 0
wire_temp = 0
i = 0
temp_list =  []
time_list = []


while i < (time-time_step):
    if i >= takeoff_time:
       current = cruise_current
##    if i >= second_takeoff_time:
 ## //      current = takeoff_current
        
#    if i <= 15:
#        current = 235.3
#    if 15 < i < 115:
#        current = 0
#    if 115 < i < 130:
#        current = 235.3
#    if 130 < i < 230:
#        current = 0
#    if 230< i < 245:
#        current = 235.3
#    if 245 < i < 345:
#        current = 0
#    if 345< i < 360:
#        current = 235.3
#    if 360 < i < 460:
#        current = 0
#    if 460< i < 475:
#        current = 235.3
#    if 475 < i < 575:
#        current = 0
#    if 575< i < 590:
#        current = 235.3
#    if 590< i < 690:
#        current = 0
        
        
    power_loss = power_loss_cal(resistance_of_wire , current)
    thermal_dissapation = thermal_dissapation_cal(wire_surface_area , thermal_transmittance , wire_temp)
    power_in_wire = power_loss - thermal_dissapation
    instantaneous_temp_rise = instantaneous_temp_rise_cal(time_step , specific_heat_capacity , mass_of_wire , power_in_wire)
    wire_temp = wire_temp + instantaneous_temp_rise
    i = i + time_step
    temp_list.append(wire_temp)
    time_list.append(i)


plt.plot(time_list , temp_list)
plt.xlabel("Time (s)")
plt.ylabel("Temperature rise (K)")
title_string = 'Temperature rise over time for ' , awg , 'wire'
plt.title(title_string)

plt.rcParams["figure.figsize"] = (10,10)
plt.show()
                          


    

