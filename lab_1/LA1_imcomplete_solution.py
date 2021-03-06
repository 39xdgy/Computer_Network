"""
Author: Sikde Huq
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


    def enqueue(self, sim, packet, isACK):
        global packetHistory
        print ('enqueue', sim.now, self.name, packet.seq_num, end = ' ')        
        isDropped = False

        packetHistory[packet.seq_num-1].append(sim.now)
        if len(self.queue) == 0:
            self.queue.append(packet)
            print('packet enqueued, QueueSize %d' % len(self.queue))
            if self.outgoing_link != None:                
                sim.schedule_event(self.transmit, None, sim.now, False)
            
            packetHistory.append([x for x in packetHistory[packet.seq_num-1] + ['Yes']])
            
        #Complete this function
        elif len(self.queue) == self.queueSize:
            isDropped = True
            print("packet dropped, queue is full")

        else: #x.queue is neither empty nor full
            self.queue.append(packet)
            print('packet enqueued, Queue Size %d' % len(self.queue))

        if (packet.lastSender is not None): # and (self.name is not 'e'):
            #print(self.outgoing_link)
            sim.schedule_event(packet.lastSender.transmit, None, sim.now + packet.lastSender.outgoing_link.delay, not isDropped)

        
        
        

    def transmit(self, sim, packet, isACK):
        print ('transmit', sim.now, self.name,  isACK, end = ' ')        
        if isACK:
            self.queue.pop(0)
            
        if len(self.queue) > 0:
            print (' transmitting packet ' + str(self.queue[0].seq_num))

            self.queue[0].lastSender = self
            
            sim.schedule_event(self.outgoing_link.dst.enqueue, self.queue[0], sim.now + self.outgoing_link.delay, self.queue[0].seq_num)
        else:
            print(' empty queue, no packet to transmit')


            
        #complete this function
        

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
            packetHistory.append([packetSeqN,'A', i])
            packetSeqN += 1            
            sim.schedule_event(nodeA.enqueue, packet, i, None)
    for i in range(0, 10000, 500):
        for j in range(5):
            packet = Packet(packetSeqN, None)
            packetHistory.append([packetSeqN, 'B', i])
            packetSeqN += 1            
            sim.schedule_event(nodeB.enqueue, packet, i, None)
    sim.run(10000)

    for i in packetHistory:
        ls = i.split(',')
        print(len(ls))

    # writeing on the output file 
    
    f = open('simTrace.csv','w') 
    f.write('SeqN, Src, Q@src, Trn@src, Rcv@C, Drp@C, Trn@C, Rcv@D, Drp@D, Trn@D, Rcv@E \n')
    for rowIndex in range(len(packetHistory)):
        #print(packetHistory[rowIndex])
        #write code to write on the output file
        #print(rowIndex)
        pass
