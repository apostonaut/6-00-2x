###########################
# 6.00.2x Problem Set 1: Space Cows 

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """

    cow_dict = dict()

    f = open(filename, 'r')
    
    for line in f:
        line_data = line.split(',')
        cow_dict[line_data[0]] = int(line_data[1])
    return cow_dict


# Problem 1
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """


    def searchCows(cowNameWeight, weightList, currentLoad):
        """
        Searches the cows for cows that have weights in the weightList. Starts with largest, and
        iterates through list until a cow is found that fits into the currentLoad

        :param cowNameWeight: list of (name, weight) tuples
        :param weightList: a decreasing list of possible weights for cows, beginning with largest
        :param currentLoad: the current load of cows being filled
        :return: updated currentLoad with
        """
        for weight in weightList:  # start at largest weight, go down to 1
            for item in cowNameWeight:
                if item[1] == weight:
                    currentLoad.append(item[0])  # appends name of cow with desiredWeight
                    cowNameWeight.remove(item)
                    return currentLoad, cowNameWeight
        return None

    # create list of tuples from dictionary: (cow_name, cow_weight)
    cowsKeys = cows.keys()
    cowNameWeight = []
    for key in cowsKeys:
        cowNameWeight.append((key, cows[key]))

    trips = []
    while cowNameWeight:
        current_load = []
        weightLimit = limit

        while weightLimit >= 0:
            desiredWeight = weightLimit
            #if cowNameWeight: #check to make sure that there are cows left

            #create a decreasing list of weights to search cows for
            weightList = [weight for weight in range(1, desiredWeight + 1)]
            weightList.reverse()

            #search cows for next cow that fits in current_load, assign new current_load. If no
            # cow is found that fits into current_load, output of searchCows will be None
            output = searchCows(cowNameWeight, weightList, current_load)
            if output is not None:
                current_load = output[0]
                cowNameWeight = output[1]
                # decrement limit by weight of last cow added to current_load
                weightLimit-= cows[current_load[-1]]

            # none of the remaining cows fit into current_load
            elif output is None:
                trips.append(current_load)
                break
    return trips





# Problem 2
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    valid_partitions = []
    for partition in get_partitions(cows):
        # find all partitions which contain trips which do not exceed weight limit
        is_valid_partition = True
        for trip in partition:
            # confirm that weight of cows in trip is <= limit
            trip_weight = 0
            for cow in trip:
                trip_weight += cows[cow]
            #exit partition if weight limit exceeded in trip
            if trip_weight > limit:
                is_valid_partition = False
                break
        if is_valid_partition:
            valid_partitions.append(partition)
    #find partition with least number of trips
    shortest_partition = []
    for partition in valid_partitions:
        if shortest_partition == []:
            shortest_partition = partition
        elif len(partition) < len(shortest_partition):
            shortest_partition = partition
    return shortest_partition




        
# Problem 3
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    cows = load_cows("ps1_cow_data.txt")
    limit = 10
    start = time.time()
    brute_force_cow_transport(cows, limit)
    end = time.time()
    print('brute force time', (end - start))

    start = time.time()
    greedy_cow_transport(cows, limit)
    end = time.time()
    print('greedy time', (end-start))


"""
Here is some test data for you to see the results of your algorithms with. 
Do not submit this along with any of your answers. Uncomment the last two
lines to print the result of your problem.
"""

cows = load_cows("ps1_cow_data.txt")
limit=10
print(cows)

print(greedy_cow_transport(cows, limit))
print(brute_force_cow_transport(cows, limit))

print(compare_cow_transport_algorithms())



