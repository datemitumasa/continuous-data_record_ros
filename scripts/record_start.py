#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import numpy as np
from sensor_msgs.msg import Joy
from sensor_msgs.msg import JointState
import time
import tf2_ros
from continuous_data_record_ros.srv import RosbagRecord
from continuous_data_record_ros.srv import RosbagRecordRequest
import os
import yaml

if __name__ == '__main__':
    rospy.init_node('rosbag_record_start')
    srv_record_start = rospy.ServiceProxy("rosbag_record", RosbagRecord)
    _path =  __file__.split("/")[:-1]
    path  = "/".join(_path) + "/"
    f = open(path + "../config/parameter.yaml", "r+")
    param = yaml.load(f)
    f.close()
    record_req = RosbagRecordRequest()
    record_req.node_name= param["record_info"]["record_node_name"]
    record_req.save_name= param["record_info"]["record_name"]
    record_req.split_duration_str = str(param["record_info"]["record_split_time"])
    record_req.record_topic_list = param["record_info"]["record_topic"]
    res = srv_record_start.call(record_req)
    if res.success:
        rospy.loginfo("record_start")
    else:
        rospy.logwarn("plase check database console, if no error, record start compleate")
