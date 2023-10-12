'''goals3democode.py

   Demo code for Goals 3
'''

# Import useful packages
import hebi
import numpy as np              # For future use
import matplotlib.pyplot as plt

from math import pi, sin, cos, asin, acos, atan2, sqrt
from time import sleep, time


#
#  HEBI Initialization
#
#  Create the motor group, and pre-allocate the command and feedback
#  data structures.  Remember to set the names list to match your
#  motor.
#
names = ['3.2']
group = hebi.Lookup().get_group_from_names(['robotlab'], names)
if group is None:
  print("Unable to find both motors " + str(names))
  raise Exception("Unable to connect to motors")

command  = hebi.GroupCommand(group.size)
feedback = hebi.GroupFeedback(group.size)


#
#  Pre-allocate the storage.
#
T = 5.0                     # 5 seconds
N = int(100 * T)            # 100 samples/second.

Time = [0.0] * N
PAct = [0.0] * N
PCmd = [0.0] * N
VAct = [0.0] * N
VCmd = [0.0] * N


#
#  Execute the movement.
#
# Initialize the index and time.
index = 0
t     = 0.0
while True:
    # Read the actual data. This blocks (internally waits) 10ms for the data.
    feedback = group.get_next_feedback(reuse_fbk=feedback)
    pact = feedback.position[0]
    vact = feedback.velocity[0]

    # Compute the commands for this time step.
    if t < 2.5:
        pcmd = 1.0
        vcmd = 0.0
    else:
        pcmd = 0.0
        vcmd = 0.0

    # Send the commands.  This returns immediately.
    command.position = [pcmd]
    command.velocity = [vcmd]
    group.send_command(command)

    # Store the data for this time step (at the current index).
    Time[index] = t
    PAct[index] = pact
    PCmd[index] = pcmd
    VAct[index] = vact
    VCmd[index] = vcmd

    # Advance the index/time.
    index += 1
    t     += 0.01

    # Break (end) the loop, if we run out of storage or time.
    if index >= N or t >= T:
        break


#
#  Plot.
#
# Create a plot of position and velocity, actual and command!
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

ax1.plot(Time[0:index], PAct[0:index], color='blue', linestyle='-',  label='Act')
ax1.plot(Time[0:index], PCmd[0:index], color='blue', linestyle='--', label='Cmd')
ax2.plot(Time[0:index], VAct[0:index], color='blue', linestyle='-',  label='Act')
ax2.plot(Time[0:index], VCmd[0:index], color='blue', linestyle='--', label='Cmd')

ax1.set_title('Robot Data - Change to label what this is')
ax1.set_ylabel('Position (rad)')
ax2.set_ylabel('Velocity (rad/s)')
ax2.set_xlabel('Time (s)')

ax1.grid()
ax2.grid()
ax1.legend()
ax2.legend()

plt.show()
