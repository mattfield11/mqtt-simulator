
# mqtt-simulator
A python mqtt device simulator for testing mosquitto and others

Requires previous installation of the mqtt paho library for python.

#Installation

Edit the first few lines of the simulator so that the file points at your MQTT server.  

#Use

Run from terminal prompt, you can control the simulation by publishing numerical data on the topics
tank/1/fillRate
tank/1/emptyRate

If you publish nothing, the tank level will gradually increase until a maximum level is reached.
At this point the tank will gradually empty until a minimum level is reached.  Then the valve will open and the tank will fill again.

The tank level is published at a given frequency on 

tankOut/1/level
