from enum import Enum

#DensityStatus=Enum('status',('NORMAL','SPORADIC'))





#Sparse的两个子状态
class SparseStatus(Enum):
    #paper中只有NORMAL和SPORADIC。这里我们为了代码逻辑的便利做了修改
    NORMAL = 0 #在judge过程，若符合s1和s2 则转变为TOEDELETE
    TEMP = 1 #在judge过程，符合s1和s2则转为TODELETE，若不符合s1和s2，变为NORMAL
    TODELETE = 2 #在judge过程，看到这个状态一律删除（在Grid的AddNewData里若发现这个状态，把它修改为TEMP）



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
    #脉宽，0.1μs~200μs 测量精度是50ns/
    PW=0
    #======可选参数===========
    #以下参数是程序辅助使用，和算法无关
    toa=0
    cluster=0

    def __init__(self,PW,RF,DOA):
        self.DOA=DOA
        self.RF=RF
        self.PW=PW



