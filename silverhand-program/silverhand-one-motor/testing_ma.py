import random
import matplotlib.pyplot as plt

# Global Constants
MOVING_AVERAGE_BUFFER = 16
DEFAULT_RELAXTHRESH = 275
SMOOTH_READS = 16

rand_nums = []


def gen_random_nums():
    """Imitiates an Arduino sensor by generating numbers.
    Process:
    1. 
    """
    i = 0
    curr_num = 200
    while i < 1000:
        if i %100 == 0: # simulate spikes
            curr_num += random.randint(300, 600)
            curr_num = max(0, curr_num)
            curr_num = min(curr_num, 1023)
        else:
            num = random.randint(-15, 10)
            curr_num += num
            curr_num = max(0, curr_num)
            curr_num = min(curr_num, 1023)
            if curr_num == 0:
                curr_num = 15
            elif curr_num == 1023:
                curr_num = 1023 - 15
        i += 1
        rand_nums.append(curr_num)
    plt.plot(range(0, 1000), rand_nums, label="rand")


class Moving_Average:
    """
        The Moving Average class serves as a different way of reading a numbers.
    """
    def __init__(self):
        self.values = [275] * MOVING_AVERAGE_BUFFER
        self.counter = 0
        self.sum = DEFAULT_RELAXTHRESH * MOVING_AVERAGE_BUFFER
        self.results = []

    # Returns one data point and updates average
    def read_val(self, current_pt):
        # Take out oldest value from sum
        self.sum -= self.values[self.counter]

        # Read in newest value and overwrite oldest
        self.values[self.counter] = rand_nums[current_pt] 
        # print(self.values[self.counter])
        
        # Update sum to reflect new value
        self.sum += self.values[self.counter]

        # Increment counter and do modulo to make sure it wraps around
        self.counter += 1
        self.counter %= MOVING_AVERAGE_BUFFER

        # get average
        avg = self.sum / MOVING_AVERAGE_BUFFER

        # append avg to results for future plotting
        self.results.append(avg)

        # return avg
        return avg
    
    
class Smooth_Read:
    def __init__(self):
        self.results = []

    def read_val(self, current_beginning):
        # instantiate necessary variables
        sum = 0
        print("curr_begin = ", current_beginning)
        # read in vals
        for i in range(SMOOTH_READS):
            sum += rand_nums[current_beginning + i]

        # compute avg
        avg = sum / SMOOTH_READS

        # append avg to results for future plotting
        self.results.append(avg)

        # return avg
        return avg

if __name__ == '__main__':
    # create one plot
    plt.figure()

    # create randon nums (this function also hads a plot line)
    gen_random_nums()
    
    # instantiate class variables
    ma = Moving_Average()
    sr = Smooth_Read()

    # test moving average
    for i in range(1000):
        ma.read_val(i)
    
    # plot values
    plt.plot(range(0, 1000), ma.results, label="ma")
    
    # test smooth read
    for i in range(0, 1000, SMOOTH_READS):
        sr.read_val(i)

    # print array lengths
    print("MA.results.length", len(ma.results))
    print("SR.results.length", len(sr.results))

    
    # plot values
    #sr.results.pop()
    
    plt.plot(range(MOVING_AVERAGE_BUFFER, 1000 + MOVING_AVERAGE_BUFFER, MOVING_AVERAGE_BUFFER), sr.results, label="sr")

    
    plt.legend()
    plt.savefig("outputs.png")
