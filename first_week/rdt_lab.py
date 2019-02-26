class packet:
    def __init__(self, seq_num, ack_num, checknum, data):
        self.seq_num = seq_num
        self.ack_num = ack_num
        self.checknum = checknum
        self.data = data

    def get_seq(self):
        return self.seq_num
    def change_seq(self, new_seq):
        self.seq_num = new_seq
        print("Change seq_num complete")
        
    def get_act(self):
        return self.ack_num
    def change_act(self, new_ack):
        self.ack_num = new_ack
        print("Change ack_num complete")
        
    def get_checknum(self):
        return self.checknum
    def change_checknum(self, new_checknum):
        self.checknum = new_checknum
        print("Change checknum complete")
        
    def get_data(self):
        return self.data
    def change_data(self, new_data):
        self.data = new_data
        print("Change new_data complete")


if __name__ == "__main__":
    s = packet(4, 5, 6, 7)
    print(s.get_seq())
    print(s.get_act())
    print(s.get_checknum())
    print(s.get_data())
