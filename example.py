#!/usr/bin/env python
from bitalino import BITalino
import time
# This example will collect data for 5 sec.
macAddress = "20:16:07:18:15:11"
running_time = 10

batteryThreshold = 30
acqChannels = [0, 1]
samplingRate = 1000
nSamples = 10
# digitalOutput = [1,1]

# Connect to BITalino
device = BITalino(macAddress)

# Set battery threshold
device.battery(batteryThreshold)

# Read BITalino version
print(device.version())

# Start Acquisition
device.start(samplingRate, acqChannels)

start = time.time()
end = time.time()
while (end - start) < running_time:
        # Read samples
        print(device.read(nSamples))
        end = time.time()

# Turn BITalino led on
# device.trigger(digitalOutput)

# Stop acquisition
device.stop()

# Close connection
device.close()