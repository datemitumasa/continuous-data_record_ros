#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 12:02:07 2016

@author: robocup
"""
import os
import sys
import numpy as np
import rospy
import pickle
import numpy as np
import os
from continuous_data_record_ros.srv import RosbagPlay
from continuous_data_record_ros.srv import RosbagPlayRequest

BAG = os.getenv("BAG_FOLDA")
if BAG == None:
    BAG = ""


def typesirialize(messagetype):
    message_list = [messagetype]
    message_sirialize = pickle.dumps(message_list)
    sirialize_list= np.array(message_sirialize.split("\n"))
    message_point = [".msg" in ss for ss in sirialize_list]
    message_select = np.select([message_point],[sirialize_list])
    messages = message_select[message_select != '0']
    type_point = np.where(message_point)[0] + 1
    types = sirialize_list[type_point]
    return messages ,types

def desirialize(data, messagetype):
    messages, types = typesirialize(messagetype)
    code = data.module_code
    sirial_message = data.pickle_message
    sirial_array = np.array(sirial_message.split("\n"),dtype = '|S256')

    bool_type = []
    for t in range(len(types)):
        find_type = types[t]
        ff = np.array([find_type in sirial for sirial in sirial_array])
        bool_type.append(ff)

    for t in range(len(types)):
        find_type = types[t]
        for i in range(len(types)):
            check_type = types[i]
            if check_type in find_type:
                continue
            ch = np.where(bool_type[i])
            bool_type[t][ch] = False

    for t in range(len(types)):
        type_point = np.where(bool_type[t])[0]
        sirial_array[type_point] = types[t]
    sirial_code = "(c" + code
    n = len(messages)
    code_point = np.where(sirial_array == sirial_code)[0]
    code_length = np.arange(len(code_point))
    s_a = sirial_array
    for nn in range(n):
        mes = messages[nn]
        s_a[code_point[code_length[code_length % n == nn]]] = mes 
    silialize_message = "\n".join(s_a)
    topics = pickle.loads(silialize_message)
    return topics


class JointBagReader(object):
    def __init__(self):
        self.srv = rospy.ServiceProxy("rosbag_play", RosbagPlay)

    def data_get(self, req, mes_type):
        req.folda_path = BAG

        data = self.srv.call(req)
        if not data.success:
            rospy.logwarn("error read bag joint")
            return None, None, None

        topics = desirialize(data, mes_type)
        return topics


