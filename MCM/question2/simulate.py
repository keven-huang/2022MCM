import numpy as np
import matplotlib.pyplot as plt
import random

# 常数
MaxTestNum = 100        # 最大测试数量
AccRangeErr = 0.1       # 和当前位置的偏移误差


# 夹角计算函数
def angle1(b, a, c):
    res = np.arccos(np.dot((b-a), (c-a)) /
                    (np.sqrt(np.sum((b-a)*(b-a)))*np.sqrt(np.sum((c-a)*(c-a)))))
    return round(res, 3)

#计算范数+处理
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

def init_re(i, AccNo, AccPoint):
    # 固定发射无人机编号i
    # TransimitNo = [0, 1, i]
    TransimitPoint = [np.array([0, 0]), np.array([1, 0]), np.array([np.cos((i-1)*np.pi/4.5), np.sin((i-1)*np.pi/4.5)])]
    # 计算获得的三个角度
    Angle = np.array([angle1(TransimitPoint[0], AccPoint, TransimitPoint[1])])
    Addarr = np.array([angle1(TransimitPoint[0], AccPoint, TransimitPoint[2]), angle1(TransimitPoint[1], AccPoint, TransimitPoint[2])])
    Addarr = np.sort(Addarr)
    Angle = np.append(Angle, Addarr)

    # 前两者为接受无人机收到的信息，AccPoint为绘图信息
    return AccNo, Angle, AccPoint


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

def trans(i):
    if i == 0:
        return [0, 0]
    if i == 1:
        return [1, 0]
    if i == 2:
        return [0, 1]
    if i == 3:
        return [1, 1]


# 模拟算法 -- 改版
# kind = 1 1-范数 kind = 2 2-范数 kind = 3 无穷范数
def runSimulation_re(kind):
    x = np.linspace(-0.2, 0.2, 11)
    y = np.linspace(-0.2, 0.2, 11)
    xx, yy = np.meshgrid(x, y)
    xx = np.reshape(xx, (len(x)**2,))
    yy = np.reshape(yy, (len(x)**2,))
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
        for j in range(2, 10):
            if j != i:
                AccNo = j
                for k in range(len(xx)):
                    AccPoint = np.array([np.cos((j-1)*np.pi/4.5), np.sin((j-1)*np.pi/4.5)]) + np.array([xx[k], yy[k]])
                    No, Angles, AccPoint = init_re(i, AccNo, AccPoint)
                    Caculate = compare(Angles, No, kind)
                    # 算法推断正确
                    if Caculate == i:
                        p2 = axs[trans(i-2)[0], trans(i-2)[1]].scatter(AccPoint[0], AccPoint[1], c='r',s = 10)
                    # 计算错误
                    else:
                        
                        p3 = axs[trans(i-2)[0], trans(i-2)[1]].scatter(AccPoint[0], AccPoint[1], c='b',s = 10)
        x = [point[0] for point in CorrectPoint]
        y = [point[1] for point in CorrectPoint]
        TranMitX = [CorrectPoint[0][0],CorrectPoint[1][0],CorrectPoint[i][0]]
        TranMitY = [CorrectPoint[0][1],CorrectPoint[1][1],CorrectPoint[i][1]]
        p1_2 = axs[trans(i-2)[0], trans(i-2)[1]].scatter(x, y, c='g',s = 10)
        p1_1 = axs[trans(i-2)[0], trans(i-2)[1]].scatter(TranMitX, TranMitY, c='k',s = 10)
    fig.legend([p1_1,p1_2,p2,p3], [u'发射机',u'接受机正确位置',u'接收机偏移有效定位位置',u'接收机偏移出错定位位置'])
    path = './{kind}.png'.format(kind = kind)
    plt.savefig(path,dpi = 400)

dict = create_three_element_tuple()
for kind in range(1,4):
    runSimulation_re(kind)
