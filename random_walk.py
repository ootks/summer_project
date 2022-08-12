import matplotlib.pyplot as plt
from numpy import polyfit, linspace
import numpy
import random
import math

# Plots for random
def entropy(p):
    return -sum(pi * math.log(pi) if pi != 0 else 0 for pi in p)

data = []
def randomtrial(n, iters):
    a = [0 for i in range(n-1)] + [1]
    distances = []
    entropies = []
    for _ in range(iters):
        x = sorted(a)
        dist = math.log(x[-1] - x[0])
        distances.append(dist)
        entropies.append(entropy(a))

        i = random.randint(0, n-1)
        avg = (a[i] + a[(i+1) % n]) / 2
        a[i], a[(i+1) % n] = avg, avg

    with open("distances_data.txt", "w") as f:
        f.write(str(distances))

    skip = 0
    distances = distances[skip:]
    iterations = [x for x in range(skip+1, iters+1)]
    # Try to get at the linear region of this plot.
    slope, intercept = polyfit(iterations, distances, 1)
    data.append(slope)
    #print(slope)
    #print("slope*iteration + intercept = log(distance)".format(slope))

    #fig, axs = plt.subplots(2)
    ## Plot log-log thing
    #axs[0].set_xlabel("iteration")
    #axs[0].set_ylabel("log(distance)")
    #axs[0].set_title("distance vs iteration")
    #axs[0].plot(iterations, distances,label="data")
    #axs[0].plot(iterations, slope * numpy.array(iterations) + intercept, label="{} * log(distance) + {}".format(slope, intercept))
    #axs[0].legend()
    #axs[1].plot([x for x in range(skip+1, iters+1)], entropies[skip:])
    #axs[1].set_title("entropy vs iteration")
    #plt.show()

def entropy_max_trial(n, iters):
    #a = numpy.array(list(range(n)))
    #a = a/sum(a)
    a = [0 for i in range(n-1)] + [1]
    distances = []
    entropies = []
    for _ in range(iters):
        max_entropy = 0
        max_i = None
        for i in range(n):
            x, y = a[i], a[(i+1) % n]
            avg = (x+y)/2
            a[i], a[(i+1) % n] = avg, avg
            ent = entropy(a)
            if ent >= max_entropy:
                max_entropy = ent
                max_i = i
            a[i], a[(i+1) % n] = x, y
        avg = (a[max_i] + a[(max_i+1) % n]) / 2
        a[max_i], a[(max_i+1) % n] = avg, avg
            
        distances.append(math.log(max(abs(x - 1/n) for x in a)))
        entropies.append(entropy(a))

    skip = 10000
    distances = distances[skip:]
    iterations = [math.log(x) for x in range(skip+1, iters+1)]

    slope, intercept = polyfit(distances, iterations, 1)
    print("Omega(distance^{}) = iterations".format(slope))

    fig, axs = plt.subplots(2)
    # Plot log-log thing
    axs[0].set_xlabel("log(distance)")
    axs[0].set_ylabel("log(iteration)")
    axs[0].set_title("distance vs iteration")
    axs[0].plot(distances, iterations,label="data")
    xs = linspace(min(distances), max(distances))
    axs[0].legend()
    axs[1].plot([x for x in range(skip+1, iters+1)], entropies[skip:])
    axs[1].set_title("entropy vs iteration")
    plt.show()

def distance_min(n, iters):
    #a = numpy.array(list(range(n)))
    #a = a/sum(a)
    a = [0 for i in range(n-1)] + [1]
    distances = []
    for _ in range(iters):
        min_dist = 100000
        min_i = None
        for i in range(n):
            x, y = a[i], a[(i+1) % n]
            avg = (x+y)/2
            a[i], a[(i+1) % n] = avg, avg
            dist = math.log(x[0] - x[-1])
            if dist <= min_dist:
                min_dist = dist
                min_i = i
            a[i], a[(i+1) % n] = x, y
        avg = (a[min_i] + a[(min_i+1) % n]) / 2
        a[min_i], a[(min_i+1) % n] = avg, avg
            
        distances.append(math.log(max(abs(x - 1/n) for x in a)))

    skip = 10000
    distances = distances[skip:]
    iterations = [math.log(x) for x in range(skip+1, iters+1)]

    slope, intercept = polyfit(iterat, iterations, 1)
    print("Omega(distance^{}) = iterations".format(slope))

    fig, axs = plt.subplots(2)
    # Plot log-log thing
    axs[0].set_xlabel("log(distance)")
    axs[0].set_ylabel("log(iteration)")
    axs[0].set_title("distance vs iteration")
    axs[0].plot(distances, iterations,label="data")
    xs = linspace(min(distances), max(distances))
    axs[0].legend()
    axs[1].plot([x for x in range(skip+1, iters+1)], entropies[skip:])
    axs[1].set_title("entropy vs iteration")
    plt.show()

#n = 20
iters = 10000
for i in range(30, 500, 10):
    randomtrial(i, iters)
mod = 1/(1-numpy.exp(numpy.array(data)))
print(mod)
plt.plot(list(range(len(data))), mod)
plt.show()
#entropy_max_trial(100, 30000)
