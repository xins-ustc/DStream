from HelperForTest import *
from Helper import *
from operator import attrgetter

array=[]
for i in range(1,100):
    raw=RawData(1,1,random.randint(1,360))
    array.append(raw)

newarr=sorted(array,key=attrgetter('toa'))
for raw in newarr:
    print(raw.PW,raw.RF,raw.DOA,raw.toa,raw.cluster)