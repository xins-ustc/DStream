from enum import Enum

#DensityStatus=Enum('status',('NORMAL','SPORADIC'))


#Sparse的两个子状态
class SparseStatus(Enum):
    NORMAL = 0
    SPORADIC = 1



class DensityStatus(Enum):
    SPARSE = 0
    TRANSITIONAL = 1
    DENSE = 2




#原始数据，三维向量
class RawData:
    #DOA：0~360 单位是度，且可以把0看成360，互相循环
    DOA=0
    #RF，载频，常规雷达范围是1G~15GHz
    RF=0
    #脉宽，0.1μs~200μs 测量精度是50ns
    PW=0
    def __init__(self,DOA,RF,PW):
        self.DOA=DOA
        self.RF=RF
        self.PW=PW