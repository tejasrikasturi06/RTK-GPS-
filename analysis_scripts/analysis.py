#!/usr/bin/env python3

import rosbag
import matplotlib.pyplot as plt
import matplotlib
import numpy as np


stationary_bag = rosbag.Bag('stationary_data.bag')
walking_bag = rosbag.Bag('walking_data_circle.bag')
stationary_occ =rosbag.Bag('stationary_data_occ.bag')
walking_occ = rosbag.Bag ('walking_data_occ.bag')

stationary_easting = []
stationary_northing = []
stationary_occ_easting =[]
stationary_occ_northing =[]
stationary_timestamps = []
stationary_occ_timestamps =[]

walking_easting = []
walking_northing = []
walking_occ_easting =[]
walking_occ_northing =[]
walking_timestamps = []
walking_occ_timestamps =[]

for topic, msg, t in stationary_bag.read_messages(topics=['/GPS']):
    stationary_easting.append(msg.utm_easting)
    stationary_northing.append(msg.utm_northing)
    stationary_timestamps.append(msg.header.stamp.secs)
    

for topic, msg, t in walking_bag.read_messages(topics=['/GPS']):
    walking_easting.append(msg.utm_easting)
    walking_northing.append(msg.utm_northing)
    walking_timestamps.append(msg.header.stamp.secs)

for topic,msg,t in stationary_occ.read_messages (topics=['/GPS']):
    stationary_occ_easting.append(msg.utm_easting)
    stationary_occ_northing.append(msg.utm_northing)
    stationary_occ_timestamps.append(msg.header.stamp.secs)

for topic, msg, t in walking_occ.read_messages(topics=['/GPS']):
    walking_occ_easting.append(msg.utm_easting)
    walking_occ_northing.append(msg.utm_northing)
    walking_occ_timestamps.append(msg.header.stamp.secs)


stationaryeasting = sum(stationary_easting)/len(stationary_easting)
stationarynorthing = sum(stationary_northing)/len (stationary_northing)
walkingeasting = sum(walking_easting) / len(walking_easting)
walkingnorthing = sum(walking_northing)/ len (walking_northing)

avg_easting_stationary = [e - min(stationary_easting) for e in stationary_easting]
avg_northing_stationary = [n - min(stationary_northing) for n in stationary_northing]
avg_easting_walking = [e - min(walking_easting) for e in walking_easting]
avg_northing_walking = [n - min(walking_northing) for n in walking_northing]
avg_easting_occ_stationary = [e - min(stationary_occ_easting) for e in stationary_occ_easting]
avg_northing_occ_stationary = [n - min(stationary_occ_northing) for n in stationary_occ_northing]
avg_easting_occ_walking = [e - min(walking_occ_easting) for e in walking_occ_easting]
avg_northing_occ_walking = [n - min(walking_occ_northing) for n in walking_occ_northing]


plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
plt.plot(stationary_occ_timestamps, avg_easting_occ_stationary, 'r', label='UTM-Easting')
plt.plot(stationary_occ_timestamps, avg_northing_occ_stationary, 'b', label='UTM-Northing')
plt.title("Stationary Data with Occulusion")
plt.ylabel("UTM-Easting, UTM-Northing")
plt.xlabel("Time")
plt.show()

plt.subplot(2, 2, 2)
plt.hist2d(stationary_occ_easting, stationary_occ_northing, 100,norm = matplotlib.colors.LogNorm())
plt.title("Stationary Data with Occulusion")
plt.ylabel("UTM-Northing")
plt.xlabel("UTM-Easting")
plt.show()

plt.subplot(2, 2, 3)
plt.plot(walking_occ_timestamps, avg_easting_occ_walking, 'r', label='UTM-Easting')
plt.plot(walking_occ_timestamps, avg_northing_occ_walking, 'b', label='UTM-Northing')
plt.title("Walking Data with Occulusion")
plt.ylabel("UTM-Easting, UTM-Northing")
plt.xlabel("Time")
plt.show()


plt.subplot(2, 2, 4)
plt.hist2d(walking_occ_easting, walking_occ_northing,100,norm=matplotlib.colors.LogNorm())
plt.title("Walking Data with Occulusion")
plt.xlabel("UTM-Easting")
plt.ylabel("UTM-Northing")
plt.show()

#stationary data without occulusion
plt.plot(stationary_timestamps,avg_easting_stationary,'r',label= 'UTM-Easting')
plt.plot(stationary_timestamps,avg_northing_stationary,'b',label= 'UTM-Easting')
plt.title("Stationary Data without occlusion")
plt.ylabel("Error in meters")
plt.xlabel("Time")
plt.show()

#Stationary Data Northing without occlusion
plt.axhline(stationary_easting[0])
plt.plot(stationary_timestamps,stationary_easting,'g',label='UTM-Easting')
plt.title("Stationary Data without occlusion")
plt.ylabel("Error in meters")
plt.xlabel("Time")
plt.show()

#Stationary Data Northing without occlusion
plt.axhline(stationary_northing[0])
plt.plot(stationary_timestamps,stationary_northing,'r',label='UTM-Easting')
plt.title("Stationary Data without occlusion")
plt.ylabel("Error in meters")
plt.xlabel("Time")
plt.show()


#Stationary Data Easting vs Northing without occlusion
plt.hist2d(stationary_easting,stationary_northing,100,norm=matplotlib.colors.LogNorm())
plt.title("Stationary Data without occlusion")
plt.ylabel("UTM-Northing")
plt.xlabel("UTM-Easting")
plt.show()


## 
plt.plot(walking_timestamps,avg_easting_walking,'r',label='UTM-Easting')
plt.plot(walking_timestamps,avg_northing_walking,'b',label='UTM-Northing')
plt.xlim(57100,57450)
plt.title("Walking Data without occlusion")
plt.ylabel("UTM-Easting, UTM-Northing")
plt.xlabel("Time")
plt.show()

###
plt.hist2d(walking_easting,walking_northing,100,norm=matplotlib.colors.LogNorm())
plt.title("Walking Data without occlusion")
plt.xlabel("UTM-Easting")
plt.ylabel("UTM-Northing")
plt.show()


#plt.tight_layout()
#plt.show()

stationary_bag.close()
walking_bag.close()
stationary_occ.close()
walking_occ.close
