import numpy as np
import matplotlib.pyplot as plt
import os, time

class Queue:
    def __init__(self, timedelta_sec, arrival_rate, process_h, time_total_h):
        self.sec_resolution = 3600/timedelta_sec
        self.arrival_freq = arrival_rate/self.sec_resolution
        self.process_h = process_h
        self.process_sec = int(pow(process_h/self.sec_resolution,-1))
        self.time_total = int(time_total_h*self.sec_resolution)
        self.time_total_h = time_total_h
    
    def simulate(self):
        # Sequential simulation
        buffer = 0
        occupied = False
        timestart = -1
        pl = np.zeros(self.time_total)
        enter_queue = np.zeros(self.process_h*self.time_total_h)
        enter_server = np.zeros(self.process_h*self.time_total_h)

        # Random Poisson process
        mos = np.random.poisson(self.arrival_freq, size=int(self.time_total))

        # two pointers
        process = 0
        last = 0

        for step in range(self.time_total):
            buffer += mos[step]
            
            # waiting time calc
            enter_queue[last:(last+mos[step])] = step
            last += mos[step]
            
            # case if server empty
            if (not occupied) and (buffer > 0):
                
                # queue logic
                occupied = True
                timestart = step
                buffer -= 1
                
                # waiting time calc
                enter_server[process] = step 
                process += 1
                
            # case if server finishes
            elif occupied and ((step-timestart) == self.process_sec):
                occupied = False
                
            pl[step] = buffer
            
        # waiting time (Nx1)
        waiting_time = enter_server - enter_queue
        waiting_time = waiting_time[:process]
        # queue number (Nx4)
        step_in = np.arange(0,self.time_total/self.sec_resolution,1/self.sec_resolution)
        queue_number = np.array([step_in, pl])
        
        # Export data
        path = os.getcwd()
        n_folder = os.path.join(path,'exports', str(int(time.time())))
        wt = os.path.join(n_folder,'waiting_time.csv')
        qn = os.path.join(n_folder,'queue_number.csv')

        os.makedirs(n_folder)
        np.savetxt(wt, waiting_time, delimiter=",")
        np.savetxt(qn, queue_number, delimiter=",")
        
if __name__ == "__main__":
    # Simulation variables
    timedelta_sec = 1        # resolution for one sec ie. steps for one sec
    arrival_h = 5.8          # ratio of arrival per hour
    process_h = 6            # ratio of processing per hour
    time_total_h = 10000     # hours of simulation
    
    # Class init
    q = Queue(timedelta_sec, arrival_h, process_h, time_total_h)
    
    for _ in range(1000):
        q.simulate()
        print(f'Simulation #{_} completed!')
    
    print("Everything done")
    
    