#!/usr/bin/env python3

from package_name.srv import AddTwoInts
from package_name.srv import AddTwoIntsRequest
from package_name.srv import AddTwoIntsResponse
import sys
import time
import rospy

def add_two_ints_client(x,y):
    rospy.wait_for_service('add_two_ints')
    try:
        add_two_ints=rospy.ServiceProxy('add_two_ints',AddTwoInts)
        resp1=add_two_ints(x,y)
        return resp1.sum
    except rospy.ServiceException as e:
        print("Hata böyle diyor"+str(e))

def usage():
    return

if __name__ == "__main__":
    if len(sys.argv)==3:
        x=int(sys.argv[1])
        y=int(sys.argv[2])
    else:
        print("%s [x y]"%sys.argv[0])
        sys.exit(1)
    print("Requestion %s+%s"%(x,y))
    s=add_two_ints_client(x,y)
    print("%s+%s=%s"%(x,y,x+y))


