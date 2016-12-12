#一个工具类
class Helper:
    @staticmethod
        #根据原始数据得出它所属grid的key值
    def getKeyFromRawData(rawData):
        # PW：0.1~200 精度选0.1
        #RF：1~15 精度选0.05
        # DOA方向角0~360，精度0.5
        pw = rawData.PW
        rf = rawData.RF
        doa=rawData.DOA
        #哈希值以三个维度的最大值来排列
        #2000(pw)300(rf)720（doa），故最大值是2000300720。key=（pw/0.1）*1000000+（rf/0.05）*1000+doa/0.5
        return Helper.getKeyFromRawData(pw,rf,doa)
        #return str(round((pw/0.1))*1000000+round((rf/0.05))*1000+round(doa/0.5))


    def getKeyFromRawData(pw,rf,doa):
        return str(round((pw/0.1))*1000000+round((rf/0.05))*1000+round(doa/0.5))


    def getNeighborKeys(key):
        key=int(key)
        ret=[]
        accuracy=[1000000,1000,1]

        #根据neighbor的定义，3个维度分别加减1即可得到对应的neighbor的key
        index=0
        for a in accuracy:
            ret[index]=str(key+accuracy[index])
            index+=1
            ret[index]=str(key+accuracy[index])
            index+=1
        return ret

    def getN():
        return 2000300720


