# continuous_data_record_ros

##  1. <a name='Overview'></a>Overview
連続情報の保存と出力を,ROSbagベースに行うためのプログラム
##  2. <a name='TableofContents'></a>Table of Contents
<!-- vscode-markdown-toc -->
* 1. [Overview](#Overview)
* 2. [Table of Contents](#TableofContents)
* 3. [Status](#Status)
* 4. [Quick Start](#QuickStart)
* 5. [API](#API)
* 6. [Artifacts](#Artifacts)
* 7. [Developer Information](#DeveloperInformation)
* 8. [Citations](#Citations)
* 9. [License](#License)
* 10. [Code Structure](#CodeStructure)
* 11. [Requirement](#Requirement)
* 12. [Dependences](#Dependences)
* 13. [Installation](#Installation)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->


##  3. <a name='Status'></a>Status
2020/03/12: repositry made  
### TODO
- [ ] コード整理
- [ ] ドキュメント作成
- [ ] Docker 化
##  4. <a name='QuickStart'></a>Quick Start

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


##  5. <a name='API'></a>API
### rostopic
## Subscriber
* None  
## Publisher
* None  
### rosservice
* None  
## remap
* None  
## Parametor
* config/parametor.yaml:  
    - continuous_publish:  
        - topic_name    : 'continuous_data_publisher'で発行する連続情報のTopicName  
        - base_frame_id : 'continuous_data_publisher'で発行する連続情報の親Tf  
        - child_frame_id: 'continuous_data_publisher'で発行する連続情報のTf  
        - publish_hz    : 'continuous_data_publisher'で発行する連続情報の発行周期  
    - record_topic: 'record_start'で保存するTopicName  
##  6. <a name='Artifacts'></a>Artifacts
- None
### 

##  7. <a name='DeveloperInformation'></a>Developer Information


##  8. <a name='Citations'></a>Citations


##  9. <a name='License'></a>License
このコードはHSR専用のコードを含むため,外部への公開は厳禁です.

---
以下オプション

##  10. <a name='CodeStructure'></a>Code Structure

##  11. <a name='Requirement'></a>Requirement

##  12. <a name='Dependences'></a>Dependences

##  13. <a name='Installation'></a>Installation

```bash
# 準備   
$ cd ~/catkin_ws/src
$ git clone https://github.com/datemitumasa/continuous_data_record_ros.git
$ cd ~/catkin_ws
$ catkin_make && source devel/setup.bash
```
