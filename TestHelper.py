from Header import RawData
import random

class TestHelper:
    @staticmethod
    def randomLegalRawData():
        pw=random.random(0,200)
        rf=random.random(1,15)
        doa=random.random(0,360)
        return RawData(pw,rf,doa)


    #给定一个key值，得到这个key值的任意rawData
    def anotherKeyRawdataFromKey(rawData):
        if rawData.pw+2>200:
            rawData.pw-=2
        else:
            rawData.pw+=2


