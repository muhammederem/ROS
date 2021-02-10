#!/usr/bin/env python3

from package_name.srv import AddTwoInts
from package_name.srv import AddTwoIntsRequest
from package_name.srv import AddTwoIntsResponse

import time
import rospy

def handle_add_two_ints(req):
    print("Returning.."+str(req.a)+" + "+str(req.b)+" = "+str(req.a+req.b))
    time.sleep(5)
    sum_response=AddTwoIntsResponse(req.a+req.b)
    return sum_response

def add_two_ints_server():
    rospy.init_node('add_two_ints_server')
    s=rospy.Service('add_two_ints',AddTwoInts,handle_add_two_ints)
    print("Ready to add two ints...")
    rospy.spin()

if __name__ == "__main__":
    add_two_ints_server()
