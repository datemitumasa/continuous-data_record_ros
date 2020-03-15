#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import numpy as np
from sensor_msgs.msg import Joy
from sensor_msgs.msg import JointState
import time
import tf2_ros
from continuous_data_record_ros.srv import RosbagStop
from continuous_data_record_ros.srv import RosbagStopRequest
import os
import yaml

if __name__ == '__main__':
    rospy.init_node('rosbag_record_start')
    srv_record_stop = rospy.ServiceProxy("rosbag_record_stop", RosbagStop)
    _path =  __file__.split("/")[:-1]
    path  = "/".join(_path) + "/"
    f = open(path + "../config/parameter.yaml", "r+")
    param = yaml.load(f)
    f.close()
    bs_req = RosbagStopRequest()
    bs_req.node_name = param["record_info"]["record_node_name"]
    res = srv_record_stop.call(bs_req)
    if res.success:
        rospy.loginfo("record stop")
    else:
        rospy.logwarn("plase check database console, if no error, record start compleate")
