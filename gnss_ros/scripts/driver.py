#!/usr/bin/env python3

import rospy
import rosbag
import serial
import utm
from std_msgs.msg import Float64, Float32
from gnss_ros.msg import gps_msg
import sys
import time

if _name_ == '_main_':
    if len(sys.argv) > 1:
        rospy.loginfo(sys.argv[1])

        
        rospy.init_node("gps_driver")
        name_port = sys.argv[1]
        serial_port = rospy.get_param('gps_driver/port','name_port')
        serial_baud = rospy.get_param('~baudrate', 57600)
        sampling_rate = rospy.get_param('~sampling_rate', 20.0)

        port = serial.Serial(serial_port, serial_baud, timeout=3.)
        gps = gps_msg()
        SENSOR_NAME = 'gps'  
        gps_pub = rospy.Publisher(SENSOR_NAME, gps_msg, queue_size=5)
        gps_bag = rosbag.Bag('gps_data.bag', 'w')

        gps = gps_msg()
        gps.header.frame_id = 'GPS1_Frame'

        sleep_time = 1 / sampling_rate - 0.025
        #print('hi')

        try:
            while not rospy.is_shutdown():
                line_puck = port_of_selection.readline()
                line_selection = str(line_puck)
                #rospy.loginfo(line_selection)
                line1 = line_selection.split(",")


                if line1[2] == '':
                    rospy.logwarn("No data")
                else:
                    if line_selection.startswith("b'$GNGGA"):
                        coordinate = utm.from_latlon(float(line1[2]) / 100, float(line1[4]) / 100)
                        timestamp = str(line1[1])
                        second = (int(timestamp[0:2]) * 3600) + (int(timestamp[2:4]) * 60) + int(timestamp[4:6])
                        nsecond = int(float(line1[1][6:]))
                        latd = int(float(line1[2])) // 100
                        latm = float(line1[2]) - (100 * latd)
                        lat = latd + (latm / 60)
                        lat = float(lat)

                        lond = int(float(line1[4])) / 100
                        lonm = float(line1[4]) - (100 * lond)
                        lon = lond + (lonm / 60)
                        if line1[5] == 'W':
                            lon *= -1
                        lon = float(lon)

                        alt = float(line1[9]) / 100
                        ind = float(line1[6])

                        utme = float(coordinate[0] / 100)
                        utmn = float(coordinate[1] / 100)
                        zone = float(coordinate[2])
                        letter = coordinate[3]

                        gps.header.stamp.secs = second
                        gps.header.stamp.nsecs = nsecond
                        gps.latitude = lat
                        gps.longitude = lon
                        gps.altitude = alt
                        gps.indicator = ind
                        gps.utm_easting = utme
                        gps.utm_northing = utmn
                        gps.zone = zone
                        gps.letter = letter
                        gps_list = [timestamp, lat, lon, alt, utme, utmn, zone, letter]

                        rospy.loginfo(gps_list)

                        gps_pub.publish(gps)

                rospy.sleep(sleep_time)

        except rospy.ROSInterruptException:
            port_of_selection.close()

        except serial.serialutil.SerialException:
            rospy.loginfo("Shutting down paro_depth node...")
