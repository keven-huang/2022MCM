from importlib.resources import path
import numpy as np
from cmath import *
import matplotlib.pyplot as plt
import random

# 计算误差率和算法正确率的关系

# 常数
MaxTestNum = 100        # 最大测试数量

# 夹角计算函数
def angle1(b, a, c):
    res = np.arccos(np.dot((b-a), (c-a)) /
                    (np.sqrt(np.sum((b-a)*(b-a)))*np.sqrt(np.sum((c-a)*(c-a)))))
    return round(res, 3)


def caculateV(v1, v2, kind):
    # 去除最大的计算范数
    a = np.delete(v1, np.argmax(v1))
    b = np.delete(v2, np.argmax(v2))
    # 计算范数
    if kind == 1: 
        return V1(a, b)
    elif kind == 2:
        return V2(a, b)
    else:
        return V3(a, b)


# 1-范数
def V1(a, b):
    return np.sum(np.abs(a-b))


# 2-范数
def V2(a, b):
    return np.sum(np.dot(a-b, a-b))


# 无穷范数
def V3(a, b):
    return np.max(np.abs(a-b))

# 计算所有三元数个数
def create_three_element_tuple():
    mylist = np.zeros((56, 5))
    k = 0
    Ori = np.array([0, 0])
    A = np.array([1, 0])
    for i in range(8):
        for j in range(8):
            if j != i:
                mylist[k, 0] = int(i+2)
                mylist[k, 1] = int(j+2)
                X1 = np.array([np.cos((i+1)*np.pi/4.5),
                              np.sin((i+1)*np.pi/4.5)])
                X2 = np.array([np.cos((j+1)*np.pi/4.5),
                              np.sin((j+1)*np.pi/4.5)])
                mylist[k, 2] = angle1(A, X2, Ori)
                tmp = np.array([angle1(X1, X2, Ori), angle1(A, X2, X1)])
                mylist[k, 3:] = np.sort(tmp)
                k = k + 1
    mydic = {}
    for k in range(56):
        if tuple(list(mylist[k, 2:])) in mydic.keys():
            mydic[tuple(list(mylist[k, 2:]))].append(
                tuple(list(mylist[k, 0:2])))
        else:
            mydic[tuple(list(mylist[k, 2:]))] = [tuple(list(mylist[k, 0:2]))]
    return mydic

def polar2cart(p):
    z = polar(p)
    print(z)
    return

# 初始化
def init(i,AccNo,AccPoint):
    # 固定发射无人机编号i
    # TransimitNo = [0, 1, i]
    TransimitPoint = [np.array([0, 0]), np.array([1, 0]), np.array([np.cos((i-1)*np.pi/4.5), np.sin((i-1)*np.pi/4.5)])]

    # 计算获得的三个角度
    Angle = np.array([angle1(TransimitPoint[0], AccPoint, TransimitPoint[1])])
    Addarr = np.array([angle1(TransimitPoint[0], AccPoint, TransimitPoint[2]), angle1(TransimitPoint[1], AccPoint, TransimitPoint[2])])
    Addarr = np.sort(Addarr)
    Angle = np.append(Angle, Addarr)

    # AccNo, Angle为接受无人机收到的信息
    return AccNo, Angle

# 对照三元数表推断
def compare(angles, No, kind):
    # 第一步比较 -> 找出8个
    firstSelect = {}
    min01 = 100
    Fittest01 = 10
    for key in dict.keys():
        if abs(key[0] - angles[0]) < min01:
            min01 = abs(key[0] - angles[0])
            Fittest01 = key[0]
    for key in dict.keys():
        if key[0] == Fittest01:
            firstSelect[key] = dict[key]
    # 计算范式找出最小的
    min = 100
    SelectAngles = (0, 0, 0)
    for key in firstSelect.keys():
        res = caculateV(angles, key, kind)
        if res < min:
            min = res
            SelectAngles = key
    # 得到SelectAngles
    for tuple in dict[SelectAngles]:
        if tuple[1] == No:
            return tuple[0]
    return -1

# polar
# 返回相应的正确率
def run_simulate(kind,AccRangeErr):
    Correctency = 0
    theta = np.linspace(0,2*np.pi,8,endpoint=False)
    for i in range(2, 6):
        for j in range(2, 10):
            if j != i:
                for k in range(8):
                    AccPoint = np.array([np.cos((j-1)*np.pi/4.5), np.sin((j-1)*np.pi/4.5)]) + \
                        AccRangeErr *np.array([np.cos(theta[k]),np.sin(theta[k])])
                    No, Angles  = init(i, j, AccPoint)
                    Caculate = compare(Angles, No, kind)
                    # 算法推断正确
                    if Caculate == i:
                        Correctency = Correctency + 1
                    # 计算错误
                    else:
                        continue
    return round(float(Correctency)/224,3)

dict = create_three_element_tuple()
for kind in range(1,4):
    plt.figure()
    AccRangeErrs = [0.06,0.08,0.1,0.12,0.14,0.16,0.18,0.2]
    for AccRangeErr in AccRangeErrs:
        Correctency = run_simulate(kind,AccRangeErr)
        print('kind = {kind},AccRangErr={err},Correctency={c}'.format(kind=kind,err=AccRangeErr,c=Correctency))
        plt.scatter(AccRangeErr,Correctency,s=20,c='r')
    path = './err-Correntency-{kind}.png'.format(kind=kind)
    plt.savefig(path,dpi=400)