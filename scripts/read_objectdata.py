#!/usr/bin/env python
# encoding: utf8
#from __future__ import unicode_literals
import numpy as np
import os
import rospy
import yaml
import pandas as pd

from geometry_msgs.msg import TransformStamped
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
    f.close()

    file_names = param["filename"].keys()
    s = rospy.Time.now()
    jbr = JointBagReader()
    C = 0
    dfs = []
    for i in range(len(file_names)):
        name = file_names[i]
        topic_info = param["filename"][name]
        req = RosbagPlayRequest()
        req.name = name
        req.count_number = topic_info["count_number"]
        req.duration = topic_info["record_split_time"]
        ##
        req.topics = "object_data"
        j = jbr.data_get(req, TransformStamped())## msgtypeはTopic似合わせたものを入力してください
        csvs = []
        timers = []
        object_names = []
        for stamp in j :
            pos = stamp.transform.translation
            rot = stamp.transform.rotation
            csvs.append([pos.x, pos.y, pos.z, rot.x, rot.y, rot.z, rot.w])
            timers.append(stamp.header.stamp.to_sec())
            object_names.append(stamp.child_frame_id)
        names = ["x", "y", "z", "qx", "qy", "qz", "qw"]
        csvs = np.array(csvs)
        nn = name.split("/")
        ns = nn[-1]
        mkdir(ns)
        np_csv = np.array(csvs)
        np_time = np.array(timers)
        np_name = np.array(object_names)
        npt_csv = np_csv.T
        npt_time = np_time.T
        npt_name = np_name.T
        df = pd.DataFrame()
        for n in range(len(names)):
            nn = names[n]
            df[nn]=npt_csv[n]
        df["time"]= npt_time
        df["name"]= npt_name
        mkdir(path + "../data")
        mkdir(path + "../data/csv")
        mkdir(path + "../data/csv/{}".format(name))
        df.to_csv(path + "../data/csv/"+"{}/{}.csv".format(name, "object_data"))
        dfs.append(df)
    df = dfs[0]
    for i in range(1, len(dfs)):
        df = pd.concat([df, dfs[i]])
    df.sort_values("time")
    df = df.reset_index()
    del df["index"]
    df["id"] = range(len(df))
    df.to_csv(path + "../data/csv/"+ "marge_objectdata.csv")

