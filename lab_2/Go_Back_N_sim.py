"""
Author: Sikde Huq 
"""
import random

#******************************************************
#******** Simulation parameters  **********************
#******************************************************
global MSS, lossProb, delayProb, N

MSS = 1024  #maximum number of bytes in a segment
#seqNSpaceSize = 3  #size of the packet sequence number space
#For simplicity, we assume that the size of sequence number space is infintely large
lossProb = 10 #packet loss probability in %
delayProb = 10 #packet delay probability in %
N = 5 #window size

global DEBUG
DEBUG = False
#******************************************************

class Packet:
    """
    This stores the information associated with a packet
    """
    def __init__(self, seqN, isACK, payload):
        self.seqN = seqN
        self.isACK = isACK
        self.payload = payload
        
# channel to simulate packet loss and delay        
class Channel:
    def __init__(self,lp,dp, sender, receiver, RTT):
        self.lossProb = lp #packet loss probability in %
        self.delayProb = dp #packet delay probability in %
        self.sender = sender
        self.receiver = receiver
        self.RTT = RTT
        
    # Function to simulate loss and delay in channel
    def toChannel (self, sim, packet):
        #randomly drop the packet
        randVar = random.randint(1,100) 
        if randVar <= self.lossProb:
            sim.log(str(int(sim.now)) + '\tChannel: dropping packet ' + str(packet.seqN) + ' isACK:' + str(packet.isACK))            
            
        else:            
            delay = self.RTT/2
            #randomly delay some packets
            randVar = random.randint(1,100) 
            if randVar <= self.delayProb:  
                delay *= 3 
                sim.log(str(int(sim.now)) + '\tChannel: delaying packet ' + str(packet.seqN) + ' isACK:' + str(packet.isACK))
            
            if packet.isACK == True:
                # deliver the packet to the sender
                sim.schedule_event(sender.recvACK, packet,sim.now + delay)    
            else: #deliver the packet to the receiver
                sim.schedule_event(receiver.recvPacket, packet, sim.now + delay)    
        
    
    
#the class for sender and receiver
class Node:
    
    def __init__(self, timeoutPrd):
        self.currSeqNum = -1 #this is also the expected sequence number for receiver
        self.channel = None
        self.data = [] #data to send (for sender) or data received (for received)
        self.activeTimer = None
        self.timeoutPrd = timeoutPrd
        self.windowSize = N
        self.base = 0
        
        
    

    # Function to generate the sequence number of the next packet
    #def getNextSeqN (self, currSeq):
        #return (currSeq+1)% seqNSpaceSize
    
    
    #*******************************************************
    #*******   methods to simulate sender's action  ********
    #*******************************************************
    # sender sends a packet to channel
    def sendPacket (self, sim, packet):
        #send the packet and start timer
        sim.schedule_event(self.channel.toChannel, packet,sim.now)
        sim.log(str(int(sim.now)) + '\tSender: sending packet ' + str(packet.seqN))
        if self.base == self.currSeqNum:
            self.activeTimer = self.base
            sim.schedule_event(self.timeout, packet,sim.now + self.timeoutPrd)
        self.currSeqNum+=1
            
    # sender receives an ACK from channel
    def recvACK (self, sim, packet):    
        sim.log(str(int(sim.now)) + '\tSender: receiving ACK ' + str(packet.seqN))
        if self.base <= packet.seqN:
            self.base = packet.seqN+1
            #activate timer
            self.activeTimer = self.base
            sim.schedule_event(self.timeout, packet,sim.now + self.timeoutPrd)       
            #send packets
            for i in range(self.currSeqNum, min(self.base+ self.windowSize,len(self.data))):                
                packet = Packet(self.currSeqNum, False, self.data[self.currSeqNum])  
                sim.log(str(int(sim.now)) + '\tSender: packeting segment ' + str(self.currSeqNum))
                sim.schedule_event(sender.sendPacket, packet,sim.now) 
        else:
            sim.log(str(int(sim.now)) + '\tSender: ignoring duplicate ACK '+ str(packet.seqN)) 
    
    #timeout at sender
    def timeout (self, sim, packet):
        #return if the event was scheduled by an inactive timer
        if self.activeTimer != self.base:
            return
        sim.log(str(int(sim.now)) + '\tSender: timeout, base = ' + str(self.base))
        
        #send packets in pipeline from base           
        self.currSeqNum = self.base
        for i in range(min(self.windowSize,len(self.data)-self.base)):            
            packet = Packet(self.base+i, False, self.data[self.base+i])  
            sim.log(str(int(sim.now)) + '\tSender: packeting segment ' + str(self.base+i))
            sim.schedule_event(sender.sendPacket, packet,sim.now+i)
               
        #Activate the timer
        self.activeTimer = self.base
        
    
    #*********************************************************
    #*******   methods to simulate receiver's action  ********
    #*********************************************************
    # receiver sends an ACK 
    def sendACK (self, sim, packet):
        sim.log(str(int(sim.now)) + '\tReceiver: sending ACK ' + str(packet.seqN))      
        sim.schedule_event(channel.toChannel, packet,sim.now)
        
    # receiver receives a packet from channel
    def recvPacket (self, sim, packet):
        sim.log(str(int(sim.now)) + '\tReceiver: receiving packet ' + str(packet.seqN))    
        #check if packet the packet has the expected seq number
        if self.currSeqNum != packet.seqN-1:
            sim.log(str(int(sim.now)) + '\tReceiver: discarding packet ' + str(packet.seqN))                       
            
        else:    
            #deliver the payload to application layer if not duplicate
            self.data.append(packet.payload)            
            sim.log(str(int(sim.now)) + '\tReceiver: delivering segment ' + str(len(self.data)-1))
            self.currSeqNum+= 1
        #create ACK
        packACK = Packet(self.currSeqNum, True, None)         
        #send ACK    
        sim.schedule_event(self.sendACK, packACK,sim.now)
        
    
    
    
    
    
    #*****************************************************************
    #*******   methods for segmenting and reassmebling data   ********
    #*****************************************************************        
    
    #read the file and split the file data into segments (simulates sender's application layer)
    def load(self, fileName):
        f = open(fileName,'rb')
        fData = f.read()
        f.close()
        count = 0
        while count < len(fData):
            nextCount = count + MSS-1
            if nextCount > len(fData):
                self.data.append(fData[count:].decode('iso-8859-1'))
            else:
                self.data.append(fData[count:nextCount].decode('iso-8859-1'))
            count = nextCount   
            
    #reassemble all the segments received and write to a file (simulates receiver's application layer)        
    def reassemble(self, fileName):
        f = open(fileName,'wb')         
        for segment in self.data:
            f.write(str.encode(segment, 'iso-8859-1'))
        f.close()   
        
        
# the class for simulation events
class Event:
    """
    This class holds all the information associated with the event
    -- fh      -- is the function handler that will be invoked when the event fires
    -- packet   -- header and payload
    -- time    -- the absolute time when the event should be executed
    -- seq_num -- the sequence number of the event
    """
    seq_num = 0

    def __init__(self, fh, packet, time, seq_num):
        self.fh = fh
        self.packet = packet
        self.time = time
        self.seq_num = seq_num
        

    def __str__(self):
        return 'id=%d @%.1f' % (self.seq_num, self.time)


# the class to manage simulation
class Simulator:
    """
    Simulator maintains a queue of events that are sorted by time (and seq_num)
    The event at the HOQ will be executed by calling the function handler that is associated with it.
    New events may be added using the schedule_event function.
    The simulator also help connect together the nodes via links.
    """
    def __init__(self):
        self.queue = []
        self.now = 0
        self.totalSimTime = 0
        self.seqN = 1
        self.logFile = 'GoBackNLog.txt'
        self.initLog()
        self.trace = []
        
    def initLog(self):
        logF = open(self.logFile,'w')
        logF.close()  
        
        

    def log(self,line):
        if DEBUG:
            #write in append mode for debugging
            logF = open(self.logFile,'a')        
            logF.write (line+ '\n')
            logF.close() 
        else:
            sim.trace.append(line)
        
    def generateLogFile(self):
        # generate log file with simulation trace (only if not in DEBUG mode)
        if not DEBUG:
            logF = open(self.logFile,'w')        
            for line in sim.trace:
                logF.write (line+ '\n')
            logF.close()       
        
    def schedule_event(self, fh, packet, time):
        
        event = Event(fh, packet, time, self.seqN)
        self.seqN += 1
        self.queue.append(event)

    def run(self):
        while True:
            self.queue.sort(key=lambda e: (e.time, e.seq_num))
            if len(self.queue) == 0: 
                self.totalSimTime = sim.now
                break
            hoq = self.queue.pop(0)
            self.now = hoq.time
            hoq.fh(self, hoq.packet)


# A fucntion to verify the correctness of the reliable data transfer protocol.
# This function compares each of the segments received by the receiver with the
# corresponding sengment sent by the sender. The function reports the segments
# that do to match.

def compareData(s,r):
    for i in range(min(len(s),len(r))):
        if s[i] != r[i]:
            print ('Mismatch segment ' + str(i))
                

if __name__ == "__main__":
    
    #create sender, receiver and channel 
    sender = Node(15) #timeout period 15 for sender
    receiver = Node(0)    
    channel = Channel(lossProb, delayProb, sender, receiver, 10) #RTT = 10 
    
    #link the sender and receiver
    sender.channel = channel
    receiver.channel = channel    
    
   #Make the sender read the file and split data into segments
    sender.load('Cornell.jpg')
        
    #initialize the simulator
    sim = Simulator()
    
    #schedule to send packets to the channel from sender
    sender.currSeqNum = 0
    for i in range(min(N,len(sender.data))):
        #create the packet for sender        
        packet = Packet(i, False, sender.data[i])         
        sim.schedule_event(sender.sendPacket, packet,i) 
        sim.log(str(int(sim.now)) + '\tSender: packeting segment ' + str(i))
    #run the simulator
    sim.run()   
        
    #reassemble the file with packets/payloads received by the receiver
    receiver.reassemble('outputFile_GoBackN.JPG')
      
    #compare data in sender and receiver
    compareData(sender.data, receiver.data)
            
    
    #report results
    sim.generateLogFile()
    print ('Number of segments to send: ', len(sender.data))     
    print ('Number of packets received by the receiver: ', len(receiver.data))
    print ('Total simulation time: ', int(sim.totalSimTime))           
            

        
