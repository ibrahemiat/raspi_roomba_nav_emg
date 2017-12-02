#!/usr/bin/env python
from __future__ import print_function
import rospy
from smach import State,StateMachine
from pycreate2 import Create2
import time

from std_msgs.msg import Int32,String
#define the display text
port = '/dev/ttyUSB0'
baud = {
    'default': 115200,
    'alt': 19200  # shouldn't need this unless you accident$
}
bot = Create2(port=port, baud=baud['default'])

bot.start()

bot.full()

bot.drive_straight(-35)
time.sleep(2)
#read the battery percentage
chargeb = 0;
capacityb=0;
chargeb = bot.get_sensors().battery_charge
capacityb= bot.get_sensors().battery_capacity
battery_state=chargeb/capacityb*100


def callback(data):
  #difine state when normal which is state one
  class one(state):
    def _init_(self):
        state._init_(self, outcomes=['emergency'])
    
    def execute(self, userdata):
        rospy.loginfo('Executing state normal')
        if battery_state>10:
            m = data.data.split()
            print(m)
            if (int(m[0])>100):
                bot.drive_direct(-35, 35)
            elif (int(m[1])>100):
                bot.drive_direct(-35, 35)
            elif (int(m[2])>100):
                bot.drive_direct(-35, 35)
            elif (int(m[3])>100):
                bot.drive_direct(35, -35)
            elif (int(m[4])>100):
                bot.drive_direct(35, -35)
            elif (int(m[5])>100):
                bot.drive_direct(35, -35)
            else:
                bot.drive_straight(35)
        else:
            return 'emergency'
  class two(state):
    #difine state when emergancy which is state two
    def __init__(self):
        State.__init__(self, outcomes=['normal'])

    def execute(self, userdata):
        rospy.loginfo('Executing state emergency')
        bot.drive_straight(0)
        if battery_state>10:
            return 'normal'        
  if __name__=='__main__':
        # Create a SMACH state machine
        sm = StateMachine(outcomes=['normal','emergency'])

        # Open the container
        with sm:
            # Add states to the container
            StateMachine.add('ONE', one(), transitions={'emergency':'TWO'})
            StateMachine.add('TWO', two(), transitions={'normal':'ONE'})

        # Execute SMACH plan
        sm.execute()

#define the subscriber
def random_subscriber():
    rospy.init_node('wheel_subscriber')
    rospy.Subscriber('sensor_values',String, callback)
    rospy.spin()

if __name__=='__main__':
    random_subscriber()
