from Header import *
import random
from operator import  attrgetter
from DStream import *
dstream=D_Stream()
#生成三组数据

array=[]

time=0
for i in range(1,1000):
    pw=random.random()*5+20
    raw=RawData(PW=pw,RF=3,DOA=10)
    time=time+random.randint(1,10)
    raw.toa=time
    raw.cluster=1
    array.append(raw)

time=0
for i in range(1,10000):
    pw=random.random()*3+15
    raw=RawData(PW=pw,RF=4,DOA=15)
    time=time+random.randint(1,10)
    raw.toa=time
    raw.cluster=2
    array.append(raw)

time = 0
for i in range(1, 10000):
    pw = random.random() * 3 + 15
    raw = RawData(PW=pw, RF=5, DOA=12)
    time = time + random.randint(1, 10)
    raw.toa = time
    raw.cluster=3
    array.append(raw)


#打乱三组数据
newarr = sorted(array, key=attrgetter('toa'))
# for raw in newarr:
#     print(raw.toa,raw.cluster)
print(len(newarr))
#TODO:rawData数组，模拟的数据流，输入给dstream
for raw in newarr:
    dstream.do_DStream(raw)





#TODO：由DStream返回多个cluser，分别将各个cluster的各个grid的数据输出到文本
manager=dstream.cluster_manager
clusters=manager.getAllCluster()

print("cluster num:",len(clusters))
print("grid left:",dstream.grid_list.size())