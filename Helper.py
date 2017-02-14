import math
from Header import *
#一个工具类


class Helper:
    N = 2000 * 300 * 720  # 根据三个维度的值域得到
    Cl = 0.8  # 这个是聚类参数里的常数，取值范围0~1，作者选了0.8，在这里仿照一下，后期在调整
    Cm = 111456000  # 这个是聚类参数里的常数，取值范围>1 根据《参数密度调查得出》
    lamb = 0.998  # λ是聚类参数里的常数，取值范围0~1
    beta = 0.3 #paper中解释是用于sporadic判断的度量，

    Dm = Cm/(N*(1-lamb))
    Dl = Cl/(N*(1-lamb))
    #===============实现单例==================
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Helper, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance


    #==========获得gap=================
    def gap(self):
        return math.floor(math.log(max(self.Cl / self.Cm, (self.N - self.Cm) / (self.N - self.Cl)), self.lamb))

    def getDensityStatus(self,density_value):
        ret = None
        if density_value >= Helper().Dm:
            return DensityStatus.DENSE
        elif density_value<= Helper().Dl:
            return DensityStatus.SPARSE
        else:
            # 注意：paper里说这个应该是闭区间，但是我觉得开区间比较准确
            return DensityStatus.TRANSITIONAL



    @staticmethod
        #根据原始数据得出它所属grid的key值
    def getKeyFromRawData(rawData):
        # PW：0.1~200 精度选0.1(值域0~2000)
        #RF：1~15 精度选0.05（至于0-300）
        # DOA方向角0~360，精度0.5（值域0-720）
        pw = rawData.PW
        rf = rawData.RF
        doa=rawData.DOA

        #哈希值以三个维度的最大值来排列
        #2000(pw)300(rf)720（doa），故最大值是2000300720。key=（pw/0.1）*1000000+（rf/0.05）*1000+doa/0.5
        return Helper.getKey(pw,rf,doa)
        #return str(round((pw/0.1))*1000000+round((rf/0.05))*1000+round(doa/0.5))
   # def isKey

    def getKey(pw,rf,doa):
        if pw >200 or pw<0:
            raise ValueError("Helper.getKeyFromRawData:pw数据超出范围",pw)
        if rf>15 or rf<0:
            raise ValueError("Helper.getKeyFromRawData:rf数据超出范围",rf)
        if doa<0 or doa >360:
            raise ValueError("Helper.getKeyFromRawData:doa数据超出范围",doa)
        return str(round((pw/0.1))*1000000+round((rf/0.05))*1000+round(doa/0.5))


    def getNeighborKeys(key):
        #TODO:需要判断边界条件来处理key处在边界不能完全返回6个neighbor的情况
        key=int(key)
        ret=[]

        #根据neighbor的定义，3个维度分别加减1即可得到对应的neighbor的key
        pw=round(key/1000000)
        if pw!=2000:
            ret.append(str(key+1000000))
        if pw!=0:
            ret.append(str(key-1000000))

        rf=round((key%1000000)/1000)
        if pw!=300:
            ret.append(str(key+1000))
        if pw!=0:
            ret.append(str(key-1000))

        doa=key%1000
        if doa!=720:
            ret.append(str(key+1))
        if doa!=0:
            ret.append(str(key-1))
        return ret



