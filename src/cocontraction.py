#!/usr/bin/env python
from bitalino import BITalino
import rospy
from std_msgs.msg import Float32
import numpy as np

global device


def clean_shutdown():
    global device
    # Stop acquisition
    device.stop()

    # Close connection
    device.close()


if __name__=="__main__":
    global device
    rospy.init_node("bitalino")
    coco_data_pub = rospy.Publisher("/bitalino/cocontraction", Float32, queue_size=10)
    dir_data_pub = rospy.Publisher("/bitalino/direction", Float32, queue_size=10)
    macAddress = "20:16:07:18:15:11"

    # Bitalino setup
    batteryThreshold = 30
    acqChannels = [2, 3]
    samplingRate = 1000
    nSamples = 50
    device = BITalino(macAddress)
    device.battery(batteryThreshold)
    rospy.loginfo(device.version())

    device.start(samplingRate, acqChannels)
    msg = Float32()
    cocontract_data = 0
    direction_data = 0
    rospy.on_shutdown(clean_shutdown)
    rospy.loginfo("Finding neutral direction signal")
    max_cnt = 100
    for i in range(0, max_cnt):
        # Read samples
        data = device.read(nSamples)
        # data = data[:]
        data = np.transpose(data)
        data = data[-2:]

        direction = (np.std(data[0]) - np.std(data[1]))
        direction_data = direction_data + direction

    neutral_dir = direction_data/(max_cnt)
    direction_data = neutral_dir
    rospy.loginfo("Set to "+str(neutral_dir))


    while not rospy.is_shutdown():
            # Read samples
            data = device.read(nSamples)
            # data = data[:]
            data = np.transpose(data)
            data = data[-2:]
            # cocontract = min(np.mean(data[0]), np.mean(data[1]))
            # bandpass also useful
            cocontract = np.std(data[0]-data[1])
            cocontract_data = (cocontract_data*(nSamples/4) + cocontract)/ ((nSamples/4)+1)
            msg.data = cocontract_data
            coco_data_pub.publish(msg)
            # sign of difference for direction

            direction = (np.std(data[0]) - np.std(data[1]))
            direction_data = (direction_data * (nSamples / 4) + direction) / ((nSamples / 4) + 1)

            direction_data2 = direction_data - neutral_dir

            msg.data = direction_data2
            dir_data_pub.publish(msg)



