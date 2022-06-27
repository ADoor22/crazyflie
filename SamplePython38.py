################################################################################
# Copyright (C) 2012 Leap Motion, Inc. All rights reserved.                    #
# NOTICE: This developer release of Leap Motion, Inc. software is confidential #
# and intended for very limited distribution. Parties using this software must #
# accept the SDK Agreement prior to obtaining this software and related tools. #
# This software is subject to copyright.                                       #
################################################################################

import Leap, sys


class SampleListener(Leap.Listener):
    def __init__(self):
        super().__init__()
        
    def on_init(self, controller):
        print("Initialized")

    def on_connect(self, controller):
        print("Connected")

    def on_disconnect(self, controller):
        print("Disconnected")

    def on_exit(self, controller):
        print("Exited")

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()
        if frame.id % 1 == 0 :

            hands = frame.hands
            numHands = len(hands)
            for hand in frame.hands:
                handType = "Left Hand" if hand.is_left else "Right Hand"
                if hand.is_right:
                    up = hand.palm_velocity[1]
                    left = hand.palm_velocity[0]
                    forward = hand.palm_velocity[2]
                    print("{:.2f}".format(-hand.palm_normal.roll))
                    #testing values

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print("Press Enter to quit...")
    try :
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass

    # Remove the sample listener when done
    controller.remove_listener(listener)


if __name__ == "__main__":
    main()

