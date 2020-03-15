#!/usr/bin/env python
# -*- coding: sjis -*-

#import os
import rospy
import numpy as np
import yaml

from sensor_msgs.msg import JointState
import tf2_ros

class PublishContinuousData(object):
    def __init__(self):
        _path =  __file__.split("/")[:-1]
        path  = "/".join(_path) + "/"
        f = open(path + "../config/parameter.yaml", "r+")
        self.param = yaml.load(f)["continuous_publish"]
        f.close()

        self.buf = tf2_ros.Buffer()
        self.lis = tf2_ros.TransformListener(self.buf)
        self.pub = rospy.Publisher(self.param["topic_name"], JointState, queue_size=10)
        self.rate = rospy.Rate(self.param["publish_hz"])
        rospy.loginfo("init success")

    def data_publish(self):
        while not rospy.is_shutdown():
            joint = JointState()
            try:
                base2hand = self.buf.lookup_transform(self.param["base_frame_id"], self.param["child_frame_id"],rospy.Time(0),rospy.Duration(3.0))
                position = [base2hand.transform.translation.x, base2hand.transform.translation.y, base2hand.transform.translation.z,
                            base2hand.transform.rotation.x, base2hand.transform.rotation.y, base2hand.transform.rotation.z, base2hand.transform.rotation.w,]
                joint.name = self.param["continuous_data_name"]
                joint.position = position
                joint.effort = [0.,] * len(position)
                joint.velocity = [0.,] * len(position)
                joint.header.stamp = rospy.Time.now()
                joint.header.frame_id = self.param["base_frame_id"]
            except:
                pass
            self.pub.publish(joint)
            self.rate.sleep()


if __name__ == "__main__":
    rospy.init_node("continuous_publisher")
    pub = PublishContinuousData()
    pub.data_publish()
