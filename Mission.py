from Header import *
import random
from operator import  attrgetter
from DStream import *
dstream=D_Stream()
#生成三组数据

print("N:",Helper.N)
print("Cl:",Helper.Cl)
print("lambda:",Helper.lamb)
print("Cm:",Helper.Cm)
print("beta:",Helper.beta)
print("Dm:",Helper.Dm)
print("Dl:",Helper.Dl)
print("gap:",Helper().gap())


array=[]

time=0
for i in range(1,1000):
    pw=random.random()*1+29
    raw=RawData(PW=pw,RF=3,DOA=10)
    time=time+random.randint(1,10)
    raw.toa=time
    raw.cluster=1
    array.append(raw)

time=0
for i in range(1,10000):
    pw=random.random()*3+15
    raw=RawData(PW=10,RF=4,DOA=15)
    time=time+random.randint(1,10)
    raw.toa=time
    raw.cluster=2
    array.append(raw)

time = 0
for i in range(1, 10000):
    pw = random.random() * 3 + 15
    raw = RawData(PW=20, RF=5, DOA=12)
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
for k in clusters:
    cluster=clusters[k]
    print("cluster_key is ",str(k)," cluster_size is ",cluster.size())
    all_grids = cluster.getAllGrids()
    for i in all_grids:
        grid=all_grids[i]
        raw=Helper.getRawFromKey(grid.key())
        print("key is ",grid.key())
        # print("PW:",raw.PW," RF:",raw.RF," DOA:",raw.DOA)
# print("grid left:",dstream.grid_list.size())