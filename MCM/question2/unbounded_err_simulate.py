from array import array
from cmath import tan
import numpy as np
import matplotlib.pyplot as plt
import random

from test import angle

#计算不限定误差率情况下正确率

MaxTestNum = 100

# 夹角计算函数
def angle1(b, a, c):
    res = np.arccos(np.dot((b-a), (c-a)) /
                    (np.sqrt(np.sum((b-a)*(b-a)))*np.sqrt(np.sum((c-a)*(c-a)))))
    return round(res, 3)

def coordinate(t,alpha,beta,gamma):
    A = np.zeros((4, 1))
    x = np.zeros((4, 1))
    y = np.zeros((4, 1))
    a = [alpha,alpha,-alpha,-alpha]
    b = [beta,-beta,beta,-beta]
    for i in range(4):
        A[i] = (np.cos(t)/np.tan(b[i]) - np.sin(t) - 1/np.tan(a[i]))/(np.cos(t)+np.sin(t)/np.tan(b[i])-1)
        y[i] = (A[i] - 1/np.tan(a[i]))/(A[i]*A[i]+1)
        x[i] = A[i]*y[i]
    O = np.array([0,0])
    A = np.array([1,0])
    B = np.array([np.cos(t),np.sin(t)])
    for i in range(4):
        C = np.array([x[i],y[i]])
        if abs(angle1(A,C,O)-alpha) < 1e-5 and abs(angle(B,C,O)-beta)<1e-5 and abs(angle(A,C,B)-gamma) < 1e-5 :
            xx = x[i]
            yy = y[i]
    return np.array([xx,yy])

def normal_distribution(mu1,mu2,sigma1,sigma2,row):
    mean = [mu1,mu2]
    cov =  [[sigma2**2,-row*sigma1*sigma2],[-row*sigma1*sigma2,sigma1**2]]
    x,y = np.random.multivariate_normal(mean,cov,size=1)
    return x,y

# 初始化
def init(i):
    # 固定发射无人机编号i
    # TransimitNo = [0, 1, i]
    TransimitPoint = [np.array([0, 0]), np.array([1, 0]), np.array([np.cos((i-1)*np.pi/4.5), np.sin((i-1)*np.pi/4.5)])]
    # 随机接受无人机编号并且以error误差确定其坐标
    AccNo = random.randint(3, 9)
    while AccNo == i:
        AccNo = random.randint(3, 9)
    CorrectPoint = np.array([np.cos((AccNo-1)*np.pi/4.5),np.sin((AccNo-1)*np.pi/4.5)])
    # 正态分布
    x,y = normal_distribution(CorrectPoint[0],CorrectPoint[1],0.1,0.1,1)
    AccPoint = np.array([x,y])
    # 计算获得的三个角度 顺序为 0-j-1,0-j-i,1-j-i
    Angle = np.array([angle1(TransimitPoint[0], AccPoint, TransimitPoint[1])])
    Addarr = np.array([angle1(TransimitPoint[0], AccPoint, TransimitPoint[2]), angle1(TransimitPoint[1], AccPoint, TransimitPoint[2])])
    # 前两者为接受无人机收到的信息，AccPoint为绘图信息
    return AccNo, Angle, AccPoint , CorrectPoint

def getdistance(pt1,pt2):
    return 

# 其他根据角度信息Coordinate
def CompareWithOtherPointCoordinate(distance,Angles,Except,TruePt):
    for i in range(2,10):
        if i != Except[0] and i != Except[1]:
            CoordinatePt = coordinate((i-1)*np.pi/4.5,Angles[0],Angles[1],Angles[2])
            Comparedistance = getdistance(CoordinatePt,TruePt)
            if Comparedistance < distance:
                return False
    return True

def trans(i):
    if i == 0:
        return [0, 0]
    if i == 1:
        return [1, 0]
    if i == 2:
        return [0, 1]
    if i == 3:
        return [1, 1]


def run_simulation():
    CorrectPoint = [np.array([0, 0])]
    for point in range(1, 10):
        CorrectPoint.append(np.array([np.cos((point-1)*np.pi/4.5), np.sin((point-1)*np.pi/4.5)]))

    # 使支持中文
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 绘制子图
    plt.figure()
    fig, axs = plt.subplots(2, 2 ,figsize=(12,12))

    for i in range(2, 6):
        for _ in range(MaxTestNum):
            No, Angles, AccPoint,CorrectPoint = init(i)
            TrueCoordinate = coordinate((i-1)*np.pi/4.5,Angles[0],Angles[1],Angles[2])
            distance = getdistance(TrueCoordinate,CorrectPoint)
            reliable = CompareWithOtherPointCoordinate(distance,Angles,[i,No],CorrectPoint)
            if reliable:
                axs[trans(i-2)[0], trans(i-2)[1]].scatter(AccPoint[0],AccPoint[1],s=10,c='r')
            else:
                axs[trans(i-2)[0], trans(i-2)[1]].scatter(AccPoint[0],AccPoint[1],c='b')
    plt.show()