from Header import RawData
import random

class TestHelper:
    @staticmethod
    def randomLegalRawData():
        pw=random.random()*200
        rf=random.random()*14+1
        doa=random.random()*360
        return RawData(pw,rf,doa)


    #给定一个key值，得到这个key值的任意rawData
    def anotherKeyRawdataFromKey(rawData):
        if rawData.PW+2>200:
            rawData.PW-=2
        else:
            rawData.PW+=2
        return rawData


