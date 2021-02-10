import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time

def move(velocity_publisher, speed, distance, is_Forward):
#Burada mesajımızın bir twist türünde mesaj olduğunu deklare ettik-
#Yani hız ver direction veriyor
    velocity_message=Twist()
#iletim olacğaından global tanımladık
    global x,y


#başlagıç koordinatları kaydedildi
    x0=x 
    y0=y
#ileri doğru gidiliyorsa gönderilen hız verileri mutlak değer olarak alınır
#Eğer ters yönde ise multak değerin negatifi şeklinde alınır
    if(is_Forward):
        velocity_message.linear.x=abs(speed)
    else:
        velocity_message.linear.x=-abs(speed)

    distance_moved = 0.0
#Burada saniyede 10 kere göndereceğimizi belirtiyoruz
    loop_rate = rospy.Rate(10)     

    while True:
        rospy.loginfo("Turtlesim ileri yönde gidiyor")
        velocity_publisher.publish(velocity_message)
        loop_rate.sleep()
        distance_moved = abs(
            math.sqrt(((x-x0) **2) + ((y-y0)**2))
        )
        print (distance_moved)
        if not (distance_moved<distance):
            rospy.loginfo("Varıldı")
            break
#Yeterli şekilde gidildiğinde kaplumbağayı duruduruyoruz.
    velocity_message.linear.x=0
    velocity_publisher.publish(velocity_message)

def poseCallback(pose_message):
    global x,y, yaw
    x=pose_message.x
    y=pose_message.y
    yaw=pose_message.theta

def rotate(velocity_publisher, angular_speed_degree,relative_agular_degree,clockwise):
    velocity_message= Twist()
    
    angular_speed= math.radians(abs(angular_speed_degree))
    
    if(clockwise):
        velocity_message.angular.z=abs(angular_speed)
    else:
        velocity_message.angular.z=-abs(angular_speed)
    
    loop_rate= rospy.Rate(1) #if you want to rotate faster u need to increase the loo rate
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




def to_Goal(velocity_publisher,x_goal,y_goal):
    global x, y, yaw
    velocity_message= Twist()
    global distance0,desired_angle_goal0

    K_linear= 0.5
    K_i_linear=0.2
    K_d_linear=0.0
    
    K_angular=2
    K_i_angular=0.0003
    K_d_angular=0.003

    t0=rospy.Time.now().to_sec()
   

    distance=abs(math.sqrt(((x_goal-x)**2)+((y_goal-y)**2)))

    linear_speed=distance * K_linear


    desired_angle_goal=math.atan2(y_goal-y,x_goal-x)
    angular_distance0=desired_angle_goal-yaw
    angular_speed=(desired_angle_goal-yaw)*K_angular

    velocity_message.linear.x=linear_speed
    velocity_message.angular.z=angular_speed

    velocity_publisher.publish(velocity_message)
    
    print('x ',x,' y ',y,' distance to goal' ,distance)
    distance0=distance
    desired_angle_goal0=desired_angle_goal    

    print('Time 0......................',t0)
    while True:
        
        t1=rospy.Time.now().to_sec()
        print('Time 1......................',t1)
        distance=abs(math.sqrt(((x_goal-x)**2)+((y_goal-y)**2)))
        print('Distance 0 ............',distance0)
        print('Distance 1 ............',distance)
        linear_speed= K_linear
        linear_speed2= (((distance - distance0) / (t1-t0))*K_d_linear) 
        linear_speed3= ((((distance+distance0)/2)*(t1-t0))*K_i_linear)
        linear_speed=linear_speed+linear_speed2+linear_speed3
        linear_speed=linear_speed*distance


        desired_angle_goal=math.atan2(y_goal-y,x_goal-x)
        angular_distance=desired_angle_goal-yaw
        angular_speed=K_angular 
        angular_speed2= ((angular_distance-angular_distance0) /(t1-t0))*K_d_angular 
        angular_speed3= (((angular_distance+angular_distance0)/2)*(t1-t0))*K_i_angular
        angular_speed=angular_speed+angular_speed2+angular_speed3
        angular_speed=angular_speed*angular_distance


        velocity_message.linear.x=linear_speed
        velocity_message.angular.z=angular_speed

        velocity_publisher.publish(velocity_message)
        
        print('x ',x,' y ',y,' distance to goal' ,distance)
        distance0=distance
        desired_angle_goal0=desired_angle_goal
        t0=t1
        if distance <=0.01 :
            velocity_message.linear.x=0.0
            velocity_message.angular.z=0.0
            velocity_publisher.publish(velocity_message)
            print('Aferin lan')
            break


def spiral(publisher,ar,lr):
    velocity_message=Twist()
    loop_Rate=rospy.Rate(1)
    while lr<10:
        lr+=1
        velocity_message.linear.x=lr
        velocity_message.linear.y=0
        velocity_message.linear.z=0
        
        velocity_message.angular.x=0
        velocity_message.angular.y=0
        velocity_message.angular.z=ar

        velocity_publisher.publish(velocity_message)
        loop_Rate.sleep()
        


    




if __name__ == "__main__":
    try:
        rospy.init_node('turtlesim_motion_pose',anonymous=True)

        #burada velocity publisherı tanıölıyorum
        cmd_vel_topic='/turtle1/cmd_vel'
        velocity_publisher=rospy.Publisher(cmd_vel_topic,Twist,queue_size=10)

        position_topic='/turtle1/pose'
        pose_subscriber=rospy.Subscriber(position_topic,Pose,poseCallback)
        time.sleep(2)
        #rotate(velocity_publisher,45,135,True)
        #time.sleep(2)
        #move(velocity_publisher,10.0,2.0,False)

        #to_Goal(velocity_publisher,4.0,5.0)
        spiral(velocity_publisher,4.0,1.0)
    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")