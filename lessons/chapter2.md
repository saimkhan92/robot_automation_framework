## Chapter 2 - Testing Junos Device using Robot framework

Now that we have covered how to write a simple test case using Robot framework, let's use our knowledge to form testcases that verify the state of Juniper devices.

### Learning Objectives
1.  Understand the environment used for communicating with Junos devices
2.  Use keywords from junos private library
3.  Passing command line arguments to robot, and accessing them from inside the test case
3.  Passing arguments for private functions/keywords


### Topology & Environment
For our next example, we have a vSRX (virtual SRX) which is our state-of-the-art firewall, connected to a linux machine. We will run our test-cases using Robot on the linux machine, and talk to the vSRX to fetch information like its modelname, OS verison, hostname, and serial number.

The Robot framework will use PyEZ library to communicate with Junos devices. The PyEZ library is a wrapper written in Python, and has APIs that can be used to communicate with devices running Junos. PyEZ can be installed on Linux based machines using the command  `pip install junos-eznc`

Similar to the example in our previous chapter, we will create a python file, where we will define functions that use PyEZ library to open a connection to our device, fetch the necessary information, and close the conenction to our device.

Execute the below command to open the file *JunosDevice.py*
```
cat JunosDevice.py
```

Lets examine the file *JunosDevice.py* and understand the different function. The main functions we will use are the below:

| Function | Description |
| ------ | ----------- |
| `connect_device`   | Initiates connection to the Juniper device.|
| `gather_device_info` | Fetches device facts from the Juniper device, and returns the serial number, model, hostname and the OS version of the device. |
| `close_device`    | Gracefully closes the PyEZ connection, once an operation is completed. |
| `get_hostname`    | Fetch hostname from the device.    |
|   `get_model` | Fetch model name from the device.  |

If you do not understand the implementation of these functions, do not worry! You only need to understand the functionality to use them in the Robot Framework. 

*We also have a PyEZ primer tutorial on NRE-Labs which you can refer, in case you would like to learn more about the awesome PyEZ library.*