
#这个函数用于输出某个grid被数据点击中时的密度结果，lam是lambda值，num是连续的点数,gap是间隔，如果是连续击中则gap=1
def denseTest(lam,num,gap):
    pre = 1
    for i in range(2, num + 1):
        cur = pre * lam ** gap + 1
        pre = cur
        print('cur ', i, '  dense=', cur)

a=[(1,1,1),(60,3,30),(3,3,3)]
for tu in a:
    print(tu)