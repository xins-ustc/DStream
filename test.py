from enum import Enum
import math
from Header import DensityStatus
from Helper import  *
import unittest

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
        with self.assertRaises(ValueError):
            fun1()


class A:
    __pri=1
    c=2

a=A()
b=a.__getattribute__("c")
print(b)