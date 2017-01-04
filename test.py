from enum import Enum
import math
from Header import DensityStatus
from Helper import  *
import unittest
from Grid import *
#这个函数用于输出某个grid被数据点击中时的密度结果，lam是lambda值，num是连续的点数,gap是间隔，如果是连续击中则gap=1
def denseTest(lam,num,gap):
    pre = 1
    for i in range(2, num + 1):
        cur = pre * lam ** gap + 1
        pre = cur
        print('cur ', i, '  dense=', cur)


def densityThreshold(Cl,lamb,tg,t,N):
    return (Cl*(1-(lamb**(t-tg+1))))/N*(1-lamb)

def fun1():
    raise Exception("hehe")

class Testtest(unittest.TestCase):
    def test_raise(self):
        with self.assertRaisesRegex(ValueError,'pw'):
            Helper.getKey(-1,13,180)
            Helper.getKey(150,13,370)

doa=335.50149417699987
pw=7.85932657958579
rf=12.50335808421012
print(Helper.getKey(pw,rf,doa))
print(Helper.getKeyFromRawData(RawData(PW=pw,RF=rf,DOA=doa)))
