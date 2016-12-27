from Header import RawData
import random

class TestHelper:
    @staticmethod
    def randomLegalRawData():
        pw=random.random(0,200)
        rf=random.random(1,15)
        doa=random.random(0,360)
        return RawData(pw,rf,doa)
