#!/usr/bin/env python
# encoding: utf8
#from __future__ import unicode_literals
import numpy as np
import os
import rospy
import pandas as pd

from sensor_msgs.msg import JointState
from continuous_data_record_ros.srv import RosbagPlayRequest
from rosbag_reader import JointBagReader


import sys

FILE = "bag_raw_data/handai"
TIME=60


def mkdir(name):
    try:
        os.mkdir(name)
    except:
        pass
            
if __name__=="__main__":
    rospy.init_node("get_rosbag_data")
    _path =  __file__.split("/")[:-1]
    path  = "/".join(_path) + "/"
    f = open(path + "../config/bag_read.yaml", "r+")
    param = yaml.load(f)
    f.close()    args = sys.argv

    file_names = param["filename"].keys()
    s = rospy.Time.now()
    jbr = JointBagReader()
    C = 0
    for i in range(len(file_names)):
        name = file_names[i]
        topic_info = param[name]
        req = RosbagPlayRequest()
        req.name = name
        req.count_number = topic_info["count_number"]
        req.duration = topic_info["record_split_time"]
        ##
        req.topics = topic_info["topic_name"]
        j = jbr.data_get(req, JointState())## msgtypeはTopic似合わせたものを入力してください
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
        mkdir(path + "../data")
        mkdir(path + "../data/csv")
        mkdir(path + "../data/csv/{}".format(name))
        df.to_csv(path + "../data/"+"{}/{}.csv".format(name, topic_info["topic_name"]))
