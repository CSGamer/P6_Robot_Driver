# Package List
## camera_pack
The package activating the camera as a sensor: 

| Node | Function | Topics |
| ----- | -----  | :------:  |
| cam_Nano | publishes the found person to the topic "Cam_Detections" | Cam_Detections |
| cam_sub | subscribes to the topic "Cam_Detections" and prints out the data published. | Cam_Detections |

## py_Driver
| Node | Function | Topics |
| ----- | -----  | :------:  |
|wheely | makes the robot drive at a set speed for each subscribtion point | Cam_Detections|
|wheely2 | The robot controller drives to a given distance from the LiDAR subscribtion | distance |

## lidar
| Node | Function | Topics |
| ----- | -----  | :------:  |
|talker | publishes all distances from -30 to 30 degrees with visualization | distance |
|center_pub | publishes only the center distance  -30 to 30 degrees with visualization | distance |
|test_sens | makes 5 iterations for the distances from  | none
|listener | prints what is published to the topic | distance

## pubsub
This is a development Package, pubsub is the development package before the camera_pack iteration and consist of 3 nodes
| Node | Function | Topics |
| ----- | -----  | :------:  |
| rd_Ros | publishes the found person to the topic | topic |
| rd_Nano | publishes the found person to the topic "Cam_Detections" | Cam_Detections |
| Sub | subscribes to the topic "Cam_Detections" and prints out the data published. | Cam_Detections |

