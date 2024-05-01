# Package List
## camera_pack
The package activating the camera as a sensor: 

| Node | Function | Topics |
| ----- | -----  | :------:  |
| cam_Nano | publishes the found person to the topic "Cam_Detections" | Cam_Detections |
| cam_sub | subscribes to the topic "Cam_Detections" and prints out the data published. | Cam_Detections |

## pubsub
This is a development Package, pubsub is the development package before the camera_pack iteration and consist of 3 nodes
| Node | Function | Topics |
| ----- | -----  | :------:  |
| rd_Ros | publishes the found person to the topic | topic |
| rd_Nano | publishes the found person to the topic "Cam_Detections" | Cam_Detections |
| Sub | subscribes to the topic "Cam_Detections" and prints out the data published. | Cam_Detections |

## bones
This is a development Package
| Node | Function | Topics |
| ----- | -----  | :------:  |
| doggy | Standard Hello World Function | hello_world_topic |
