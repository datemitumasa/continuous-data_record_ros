# continuous_data_record_ros

##  1. <a name='Overview'></a>Overview
連続情報の保存と出力を,ROSbagベースに行うためのプログラム
##  2. <a name='TableofContents'></a>Table of Contents
<!-- vscode-markdown-toc -->
* 1. [Overview](#Overview)
* 2. [Table of Contents](#TableofContents)
* 3. [Requirements](#Requirements)
* 4. [Dependences](#Dependences)
* 5. [Code Structure](#CodeStructure)
* 6. [Installation](#Installation)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->


##  3. <a name='Requirements'></a>Requirements
- ROS indigo/kinetic/melodic
##  4. <a name='Dependences'></a>Dependences
* None

```bash  
# 連続データのpublish  
$ rosrun continuous_data_record_ros continuous_data_publisher.py  
```

```bash
# ROSbag保存用プログラムの実行
$ rosrun continuous_data_record_ros rosbag_database.py  
```

```bash
# ROSbag保存開始
$ rosrun continuous_data_record_ros record_start.py  
# ROSbag保存終了
$ rosrun continuous_data_record_ros record_stop.py  
```

```bash
# 保存したROSbagの抽出
$ rosrun continuous_data_record_ros read_sample.py  
```

```bash
# TransformStamped型で物体情報を保存した場合の抽出のサンプル
$ rosrun continuous_data_record_ros read_objectdata.py  
```


##  5. <a name='Code Structure'></a>Code Structure
### rostopic
## Subscriber
* None  
## Publisher
* geometry_msgs/JointState : continuous_topic : エンドエフェクタの位置情報  
### rosservice
* continuous_data_record_ros/RosbagRecord : rosbag_record : rosbag によるtopicの保存開始  
* continuous_data_record_ros/RosbagStop : rosbag_record_stop : rosbag によるtopicの保存終了  
* continuous_data_record_ros/RosbagPlay : rosbag_play : rosbag による保存データの出力,専用のreaderとセットで使用  
## remap
* None  
## Parameter
* config/parametor.yaml:  
    - continuous_publish:  
        - topic_name    : 'continuous_data_publisher'で発行する連続情報のTopicName  
        - base_frame_id : 'continuous_data_publisher'で発行する連続情報の親Tf  
        - child_frame_id: 'continuous_data_publisher'で発行する連続情報のTf  
        - publish_hz    : 'continuous_data_publisher'で発行する連続情報の発行周期  
    - record_topic: 'record_start'で保存するTopicName  

##  6. <a name='Installation'></a>Installation

```bash
# 準備   
$ cd ~/catkin_ws/src
$ git clone https://github.com/datemitumasa/continuous_data_record_ros.git
$ cd ~/catkin_ws
$ catkin_make && source devel/setup.bash
```
