#!/usr/bin/env python
# encoding: utf8
#from __future__ import unicode_literals
import numpy as np
import os
import rospy
import pandas as pd

from sensor_msgs.msg import JointState , Joy
from geometry_msgs.msg import PoseStamped, WrenchStamped


from rosbag_database.srv import RosbagPlay, RosbagPlayRequest
from joint_sampler import JointBagReader
import objects_from_db
from audio_module_msg.msg import AudioSentence


import sys

FILE = "bag_raw_data/handai"
TIME=60


def mkdir(name):
    try:
        os.mkdir(FILE)
    except:
        pass
    try:
        os.mkdir(FILE+"/"+name)
    except:
        pass
            
if __name__=="__main__":
    rospy.init_node("get_bag_raw_data")
    args = sys.argv
    file_name = args[1]
    try:
        cl_num = int(args[5])
    except:
        cl_num = 0
    data = np.loadtxt(file_name, dtype=np.str)
    s = rospy.Time.now()
    jbr = JointBagReader()
    C = 0
    print len(data.shape)
    for i in range(len(data)):
        if len(data.shape) > 1:
            name = data[i][0]
            count = int(data[i][1])
        elif len(data.shape)==1:
            name = data[0]
            count = int(data[1])            
        print name
        req = RosbagPlayRequest()
        req.name = name
        req.count_number = count
        req.duration = 600
        ##        
        req.topics = "/hsr7/hand_states"
        j = jbr.data_get(req, JointState())
        csvs = []
        timers = []
        for joint in j :
            csvs.append(joint.position)
            timers.append(joint.header.stamp.to_sec())
        names = j[0].name
        csvs = np.array(csvs)
        nn = name.split("/")
        ns = nn[-1]
        mkdir(ns)
        np_csv = np.array(csvs)
        np_time = np.array(timers)
        npt_csv = np_csv.T
        npt_time = np_time.T
        df = pd.DataFrame()
        for n in range(len(names)):
            nn = names[n]
            df[nn]=npt_csv[n]
        df["time"]= npt_time
        df.to_csv(FILE+"/"+ns+"/"+ns+"_hand_state.csv")


        req.topics = "/hsrb/joint_states"
        j = jbr.data_get(req, JointState())
        csvs = []
        csvs_v=[]
        csvs_e=[]
        timers = []
        for joint in j :
            csvs.append(joint.position)
            csvs_e.append(joint.velocity)
            csvs_v.append(joint.effort)
            timers.append(joint.header.stamp.to_sec())
        names = j[0].name
        nn = name.split("/")
        ns = nn[-1]
        mkdir(ns)
        np_csv = np.array(csvs)
        np_time = np.array(timers)
        npt_csv = np_csv.T
        npt_time = np_time.T
        np_csv_v = np.array(csvs_v)
        npt_csv_v = np_csv_v.T
        np_csv_e = np.array(csvs_e)
        npt_csv_e = np_csv_e.T
        df = pd.DataFrame()
        df_v = pd.DataFrame()
        df_e = pd.DataFrame()
        for n in range(len(names)):
            nn = names[n]
            df[nn]=npt_csv[n]
            df_e[nn]=npt_csv_e[n]
            df_v[nn]=npt_csv_v[n]
        df["time"]= npt_time
        df_e["time"]= npt_time
        df_v["time"]= npt_time
        df.to_csv(FILE+"/"+ns+"/"+ns+"_joint_position.csv")
        df_e.to_csv(FILE+"/"+ns+"/"+ns+"_joint_effort.csv")
        df_v.to_csv(FILE+"/"+ns+"/"+ns+"_joint_velocity.csv")
        ##

