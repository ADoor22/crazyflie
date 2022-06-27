import logging
import time
# import socket, pickle


import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.syncLogger import SyncLogger
from cflib.positioning.motion_commander import MotionCommander
from cflib.positioning.position_hl_commander import PositionHlCommander
from cflib.utils import uri_helper
import Leap, sys


URI = 'radio://0/80/2M'
print('receiver loading')
# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)
print('logging error check')

# # websocket initialisation
# HOST = 'localhost'
# PORT = 50007
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((HOST, PORT))
# print('connected to socket')
# print('starting main')

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
        global up, right, forward, land
        # Get the most recent frame and report some basic information
        frame = controller.frame()
        loopCount = 0
        if frame.id % 1 == 0:

            hands = frame.hands
            numHands = len(hands)
            if numHands == 0:
                up = 0
                right = 0
                forward = 0
                land = 0

            for hand in frame.hands:
                handType = "Left Hand" if hand.is_left else "Right Hand"
                if hand.is_right :
                    if hand.grab_strength > 0.8:
                        up = 0
                        right = 0
                        forward = 0
                    else:
                        #right = float("{:.2f}".format(-(hand.palm_velocity[0])/ 400))
                        up = float("{:.2f}".format(hand.palm_velocity[1] / 500))
                        # forward = float("{:.2f}".format(-(hand.palm_velocity[2]) / 500))
                        right = float("{:.2f}".format(hand.palm_normal.roll))
                        forward = float("{:.2f}".format(-(hand.direction.pitch)))

                    v = [right, up, forward]
                    #print("The velocity is: ", v)
                if hand.is_left:
                    print("Left hand detected!")
                    # print(hand.grab_strength)
                    if hand.grab_strength > 0.8:
                        land = 1;



                    #print(up)

                    # var = float("{:.2f}".format(hand.grab_strength))
                    # data = json.dumps({"a": hand.palm_velocity, "c": var})
                    # conn.send(data.encode())
if __name__ == '__main__':
    global up, right, forward, land
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=False)
    print('initialised drivers')

    lg_stab = LogConfig(name='Stabilizer', period_in_ms=10)
    lg_stab.add_variable('kalman.stateX', 'float')
    # # lg_stab.add_variable('stabilizer.pitch', 'float')
    # # lg_stab.add_variable('stabilizer.yaw', 'float')

    cf = Crazyflie(rw_cache='./cache')

    with SyncCrazyflie(URI) as scf:
        # We take off when the commander is created
        print('takeoff')
        with SyncLogger(scf, lg_stab) as logger:
            with MotionCommander(scf) as mc:
                with PositionHlCommander(scf) as pc:
                    while True:
                        for log_entry in logger:
                            timestamp = log_entry[0]
                            data = log_entry[1]
                            logconf_name = log_entry[2]
                            mc.start_linear_motion(forward, right, up, rate_yaw=0.0)
                            print(forward)
                            # print('[%d][%s]: %s' % (timestamp, logconf_name, data))
                            #print(log_entry[1])

                        # mc.start_right(velocity=right)
                        # mc.start_forward(velocity=forward)
                        # mc.start_up(velocity=up)


                        if land == 1:
                            break

                        # time.sleep(1)
                        # mc.turn_left(180)
                        # time.sleep(1)
                        # mc.turn_left(180)
                        time.sleep(0.1)

                # We land when the MotionCommander goes out of scope
                print('Landing!')

    # Keep this process running until Enter is pressed
    print("Press Enter to quit...")
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass

    # Remove the sample listener when done
    controller.remove_listener(listener)


