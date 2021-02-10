import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time

def rotate(velocity_publisher, angular_speed_degree,relative_agular_degree,clockwise):
    velocity_message= Twist()
    
    angular_speed= math.radians(abs(angular_speed_degree))
    
    if(clockwise):
        velocity_message.angular.z=abs(angular_speed)
    else:
        velocity_message.angular.z=-abs(angular_speed)
    
    loop_rate= rospy.Rate(10)
    t0=rospy.Time.now().to_sec()

    while True:
        rospy.loginfo('Turtlesim is rotating')
        velocity_publisher.publish(velocity_message)

        t1=rospy.Time.now().to_sec()
        current_angle_degree=(t1-t0)*angular_speed_degree
        loop_rate.sleep()

        if(current_angle_degree>relative_agular_degree):
            rospy.loginfo('Reached.')
            break
    
    velocity_message.angular.z=0
    velocity_publisher.publish(velocity_message)