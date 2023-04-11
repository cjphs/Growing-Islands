import numpy as np
import matplotlib.pyplot as plt
import time

point = plt.plot(0, 0, "g^")[0]
plt.ylim(0, 5)
plt.xlim(0, 5)
plt.ion()
plt.show()

start_time = time.time()
t = 0
while t < 4:
    end_time = time.time()
    t = end_time - start_time
    print(t)
    plt.plot(t, t, "g^")[0]
    plt.pause(1e-10)