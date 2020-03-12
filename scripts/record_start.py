#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import numpy as np
from sensor_msgs.msg import Joy
from sensor_msgs.msg import JointState
import time
import tf2_ros
from tmc_control_msgs.msg import GripperApplyEffortActionGoal
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

from rosbag_database.srv import RosbagRecord, RosbagRecordRequest
from rosbag_database.srv import RosbagStop, RosbagStopRequest

from geometry_msgs.msg import WrenchStamped

import Utils
import os


class Linear_controll(object):
    def __init__(self):
        self.rate = rospy.Rate(10)
        self.data = Utils.DataBase()
#        self.tf = Utils.Tf()                
        # topics
        self.sub_joint = rospy.Subscriber("/hsrb/joint_states", JointState ,self.now_pose,queue_size=10)
        self.sub = rospy.Subscriber("/hsrb_07/joy", Joy, self.callback, queue_size=10)
        rospy.Subscriber("/hsrb/wrist_wrench/compensated", WrenchStamped, self.cb_wrench_compensated,queue_size=10)
        self.grip_act = rospy.Publisher("/hsrb/gripper_controller/grasp/goal",GripperApplyEffortActionGoal, queue_size=10)
        self.pub_list = rospy.Publisher('/hsrb/gripper_controller/command', JointTrajectory, queue_size=10)

# service
        self.srv_record_start = rospy.ServiceProxy("rosbag_record", RosbagRecord)
        self.srv_record_stop = rospy.ServiceProxy("rosbag_record_stop", RosbagStop)
        self.rosbag_number = 0
        self.record_flag = False
        self.rosbag_time = rospy.Time(0)
        self.record_number = 0
        self.number = 0
        self.date = time.ctime().split(" ")

#
        self.hand_traj = JointTrajectory()
        self.hand_traj.joint_names = ["hand_motor_joint"]
        pp = JointTrajectoryPoint()
        pp.positions = [1.2]
        pp.velocities = [0]
        pp.effort = [0.1]
        pp.time_from_start = rospy.Time(3)
        self.hand_traj.points = [pp]
        self.hand_flug = True



# TF
        self.buf = tf2_ros.Buffer()
        self.lis = tf2_ros.TransformListener(self.buf)

    def cb_wrench_compensated(self,cb):
        self._wrench = cb


    def now_pose(self,data):
        self.now_command = data.position[1]
        self.now_arm_command = data.position[0]
        self.now_arm_roll = data.position[2]
        self.now_pose_command = data.position[11]
        self.now_wrist_command = data.position[12]
        self.now_head_pan_command = data.position[9]
        self.now_head_tilt_command = data.position[10]
        
    def callback(self,data):

        if data.buttons[0] == 1:
            if not self.record_flag:
                bb_req = RosbagRecordRequest()
                bb_req.node_name= "joint_teleope_bag"
                bb_req.save_name= "exp_{0:s}_{1:s}_{2:d}".format(self.date[2], self.date[3],self.number)
                bb_req.split_duration_str = "60"
                bb_req.record_topic_list = ["/hsr7/hand_states", "/hsr7/object_pos_time_marker","/hsr7/object_pos_time","/hsrb/joint_states", "/tf"]
                res = self.srv_record_start.call(bb_req)
                self.rosbag_time = res.record_time
                self.record_number = res.record_number
                self.record_flag = True
            else:
                bs_req = RosbagStopRequest()
                bs_req.rosbag_number = self.record_number
                self.srv_record_stop.call(bs_req)
                self.number += 1
                self.record_flag = False
            rospy.sleep(1.0)

        elif data.buttons[1] == 1:
            grip = GripperApplyEffortActionGoal()
            grip.goal.effort = -0.05
            print "grasp"
            self.grip_act.publish(grip)
            time.sleep(0.1)
            self.hand_flug = False

## 改良            
        elif data.buttons[2] == 1:
            print "open"
            self.pub_list.publish(self.hand_traj)
            time.sleep(0.1)
            self.hand_flug = True



    def wrench_calc(self,):
        wrench = self._wrench
        f = wrench.wrench.force
        f_a = np.sqrt(f.x**2 + f.y**2 + f.z**2)
        return f_a
        

    def run(self):
        while not rospy.is_shutdown():
            self.show_interface()
            self.rate.sleep()
        
    def show_interface(self, ):
        os.system("clear")
        print("L1: base control, (left_joy: rotation, right_joy: move)")
        print("R1: head control, (left_joy"), "pan:", self.now_head_pan_command,", tilt:",self.now_head_tilt_command
        print("R2: arm control, (left_joy: wrist_flex, right_joy: arm_flex"), "lenear:", self.now_command,", flex:",self.now_arm_command
        if self.hand_flug:
            print "hand:open"
        else:
            print "hand:close"

        if self.record_flag:
            print"now save joint and key"
            print rospy.Time.now() - self.rosbag_time

        w = self.wrench_calc()
        print "pressure : ", w
        if w > 30.0:
            print "too much power"

                

if __name__ == '__main__':
    rospy.init_node('joy_interface')
    a = Linear_controll()
    a.run()
