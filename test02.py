import seaborn as sns
import scipy.stats as stats
from pylab import *

arr1 = plt.arrow(0,0, 3,1, head_width=0.2, color='r', length_includes_head=True)
arr2 = plt.arrow(0,0, 1,3, head_width=0.2, color='g', length_includes_head=True)
arr3 = plt.arrow(0,0, 4,4, head_width=0.2, color='b', length_includes_head=True)

plt.xlim(0,5)
plt.ylim(0,5)

plt.legend([arr1, arr2, arr3], ['u','v','u+v'])
plt.show()