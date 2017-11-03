from __future__ import division
import sys
#import matplotlib.pyplot as plt
import numpy as np
import numpy.matlib
import Queue

# Create a queue or switch port buffer swBuf [] using a bounded list (say 100 packets)
# implement a simple queue, where all packet sizes are the same say, 1500B, and the packets
# in the queue are named as according to the flowID i.e. [1,1,1,1,2,2,2,2,3,3,3,1,1,..]
# packets are removed from the head of the queue at a constant rate, and consequtive packets are 
# added at the end of the queue.
swBufQ = Queue.Queue()
swBufSize = 100

class tcpFlow:
  
  def __init__(self, flowID, totalDataSz, ssthresh, rtt, btlNckRate, sTime):
    self.flowID = flowID
    self.totalDataSz = totalDataSz
    self.ssthresh = ssthresh
    self.rtt = rtt
    self.btlNckRate = btlNckRate
    self.sTime = sTime
    self.curTime = self.sTime
    self.cwnd = 1
    self.txCwnd = 0
    self.txData = 0
    self.pktsDrop = 0
    self.cumPktsDrop = 0
    self.dataToSend = self.totalDataSz - self.txData + self.cumPktsDrop
   
  #TODO: use simPy for this schedule(simTime + tcpFlow.rtt) 
  def processFlow(self):
    if(self.dataToSend < 1):
      return;

    if(self.cwnd > self.dataToSend):
      self.cwnd = self.dataToSend

    #add to swBuf queue [self.flowID packets of self.cwnd worth]a
    #check to see if the queue has space, if not fill it with the 
    #number of packets it can be filled, and then update self.pktsDrop 
    if(swBufQ.qsize() >= swBufSize):
      self.pktsDrop = self.cwnd
      self.txCwnd = 0
    elif(swBufQ.qsize() < swBufSize):
      if((swBufSize - swBufQ.qsize()) >= self.cwnd):
        self.txCwnd = self.cwnd
        self.pktsDrop = 0
      else:
	self.txCwnd = (swBufSize - swBufQ.qsize())
	self.pktsDrop = self.cwnd - self.txCwnd

    print str(self.curTime) + "," + str(self.cwnd)

    if(self.txCwnd > 0):
      for i in xrange(self.txCwnd):
        swBufQ.put(self.flowID)

    print "Buf occupied: " + str(swBufQ.qsize())
    #adjust window due to packet drop, or congestion control
    if(self.pktsDrop > 0):
      self.cwnd = int(self.cwnd/2)
      self.ssthresh = self.cwnd
      print "Pkts dropped: " + str(self.pktsDrop) + " cwnd: " + str(self.cwnd) + " ssthresh: " + str(self.ssthresh)
    

    self.txData = self.txData + self.txCwnd
    self.cumPktsDrop = self.cumPktsDrop + self.pktsDrop
    self.dataToSend = self.totalDataSz - self.txData + self.cumPktsDrop
    self.curTime = self.curTime + self.rtt


    if(self.cwnd < self.ssthresh):
      #the flow is in slow start, double cwnd every rtt
      self.cwnd = 2*self.cwnd
    else:
      #congestion avoidance
      self.cwnd = self.cwnd + 1
    



#time to write the main program, create a for loop and fill the queue, and dequeue every rtt of a single tcpFlow connection.
#hopefully the tcp flow cwnd will show a sawtooth curve and adjust to the link rate. Lets say it schedules out 20 pkts every RTT,
#for an RTT of 10ms, and that the swBufQ has a size of 100 packets

numRtts = 100
dQueRate = 20 #20 pkts per rtt
f1 = tcpFlow(1, 2000, 5000, 10, 1000, 0)

for i in range(numRtts):

  #1.generate data from the flow, which fills up the buffer
  f1.processFlow()

  #2.dequeue from the buffer, at a constant rate
  for i in xrange(dQueRate):
    if(swBufQ.qsize() < 1):
      break;
    swBufQ.get()
     

