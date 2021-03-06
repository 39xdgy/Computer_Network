"""
Authors: Sikde Huq & Huyen Le
"""
from collections import deque

global packetHistory
packetHistory = []
seqN = 0 # seq. number for events

class Packet:
    """
    This stores the information associated with a packet
    """
    def __init__(self, seq_num, lastSender):
        self.seq_num = seq_num
        self.lastSender = lastSender
        

    def __str__(self):
        return str(self.seq_num)


class Node:
    """
    This manages the state of a node and handle the events
    """
    

    def __init__(self, name, queueSize):
        self.name = name
        self.outgoing_link = None
        self.queue = []
        self.queueSize = queueSize


    # simulation of enqueue as given in the pseudocode 
    def enqueue(self, sim, packet, isACK):
        global packetHistory
        print ('enqueue', sim.now, self.name, packet.seq_num, end = '')
        isDropped = False
        
        packetHistory[packet.seq_num-1].append(sim.now)
        if len(self.queue) == 0:
            self.queue.append(packet)
            print(' packet enqueued, QueueSize ' + str(len(self.queue)))              
            if self.outgoing_link != None:                
                sim.schedule_event(self.transmit, None, sim.now, False)
                
        elif len(self.queue) == self.queueSize:
            isDropped = True
            print (' packet dropped, queue is full')
            
            #add a new row in the history with isDropped = 'Yes'
            packetHistory.append([x for x in packetHistory[packet.seq_num-1]+ ['Yes']])
            packetHistory[packet.seq_num-1].pop()
            packetHistory[packet.seq_num-1].pop()
            
        else:
            self.queue.append(packet)
            print (' packet enqueued, QueueSize ' + str(len(self.queue)))
            
        if not isDropped and self.queueSize != float('inf'):
            packetHistory[packet.seq_num-1].append('No')
            
        if packet.lastSender != None:
            sim.schedule_event(packet.lastSender.transmit, None, packet.lastSender.outgoing_link.delay + sim.now, not isDropped)
        


    # simulation of transmit as given in the pseudocode 
    def transmit(self, sim, packet, isACK):
        global packetHistory
        print ('transmit', sim.now, self.name, isACK, end = '')
            
        if isACK:
            self.queue.pop(0)
            
        if len(self.queue) > 0:    
            print (' transmitting packet ' + str(self.queue[0].seq_num))
            packetHistory[self.queue[0].seq_num-1].append(sim.now)
            
        else:
            print(' empty queue, no packet to transmit')
            
        if self.outgoing_link != None and len(self.queue) > 0:
            self.queue[0].lastSender = self
            sim.schedule_event(self.outgoing_link.dst.enqueue, self.queue[0], sim.now + self.outgoing_link.delay, None)

    def __str__(self):
        return '%s' % self.name


class Link:
    def __init__(self, src, dst, delay):
        self.src = src
        self.dst = dst
        self.delay = delay

class Event:
    """
    This class holds all the information associated with the event
    -- fh      -- is the function handler that will be invoked when the event fires
    -- data    -- isACK
    -- time    -- the absolute time when the event should be executed
    -- seq_num -- the sequence number of the event
    """
    seq_num = 0

    def __init__(self, fh, packet, time, data, seq_num):
        self.fh = fh
        self.packet = packet
        self.time = time
        self.data = data
        self.seq_num = seq_num
        

    def __str__(self):
        return 'id=%d @%.1f' % (self.seq_num, self.time)


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
        

    def connect(self, src, dst, delay):
        link = Link(src, dst, delay)
        src.outgoing_link = link
        

    def schedule_event(self, fh, packet, time, data):
        global seqN
        event = Event(fh, packet, time, data, seqN)
        seqN += 1
        self.queue.append(event)

    def run(self, duration):
        while self.now < duration:
            self.queue.sort(key=lambda e: (e.time, e.seq_num))
            if len(self.queue) == 0: 
                break
            hoq = self.queue.pop(0)
            self.now = hoq.time
            hoq.fh(self, hoq.packet, hoq.data)


if __name__ == "__main__":
    # create the network
    nodeA = Node('a', float('inf'))
    nodeB = Node('b', float('inf'))
    nodeC = Node('c', 35)
    nodeD = Node('d', 35)
    nodeE = Node('e', float('inf'))    

    sim = Simulator()
    sim.connect(nodeA, nodeC, 11)
    sim.connect(nodeB, nodeC, 11)
    sim.connect(nodeC, nodeD, 11)
    sim.connect(nodeD, nodeE, 25)

    #intial enqueues for nodes A and B
    packetSeqN = 1
    for i in range(0, 10000, 1000):
        for j in range(20):  
            packet = Packet(packetSeqN, None)
            packetHistory.append([packetSeqN,'A'])
            packetSeqN += 1            
            sim.schedule_event(nodeA.enqueue, packet, i, None)
    for i in range(0, 10000, 500):
        for j in range(5):
            packet = Packet(packetSeqN, None)
            packetHistory.append([packetSeqN, 'B'])
            packetSeqN += 1            
            sim.schedule_event(nodeB.enqueue, packet, i, None)
    sim.run(10000)


    f = open('simTrace.csv','w') 
    f.write('SeqN, Src, Q@src, Trn@src, Rcv@C, Drp@C, Trn@C, Rcv@D, Drp@D, Trn@D, Rcv@E \n')

    # writeing on the output file 

    for rowIndex in range(len(packetHistory)):
    #print(packetHistory[rowIndex])
        #write on file
        temp_list =[x for x in  packetHistory[rowIndex]]
        while (len(temp_list) != 11):
            temp_list.append('None')
        string = str(temp_list).replace('[', '')
        string = string.replace(']', '')
        string = string.replace('\'', '')
        f.write('%s\n' % string)
    f.close()

    
    #computing average delays for the packets delivered to the destination
    
    e2eDelay = 0
    queueDelay = 0
    deliverCount = 0
    
    for row in packetHistory:
        if len(row) == 11:
            e2eDelay+=  int(row[10]) - int(row[2])
            queueDelay+= (int(row[3]) - int(row[2])) + (int(row[6]) - int(row[4])) + (int(row[9]) - int(row[7]))
            deliverCount += 1
    
    
    print ('average end-to-end delay: ', e2eDelay/deliverCount)
    print ('average queueing delay: ', queueDelay/deliverCount)        

            
                    

