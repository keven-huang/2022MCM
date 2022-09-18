import numpy as np
import matplotlib.pyplot as plt
import random



#此程序计算不限定误差率情况下的正确率以及分布图
#并且对正态分布下的标准差变化绘图

MaxTestNum = 100        #每种情形测试数量

#夹角计算
def angle(b, a, c):
    res = np.arccos(np.dot((b-a), (c-a)) /
                    (np.sqrt(np.sum((b-a)*(b-a)))*np.sqrt(np.sum((c-a)*(c-a)))))
    return res

# 夹角计算函数，保留三位小数
def angle1(b, a, c):
    res = np.arccos(np.dot((b-a), (c-a)) /
                    (np.sqrt(np.sum((b-a)*(b-a)))*np.sqrt(np.sum((c-a)*(c-a)))))
    return round(res, 3)

# 定位函数，返回以FY00为原点的笛卡尔坐标系坐标 （若三点一线会报错，无法处理）
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
    Ori = np.array([0,0])
    A = np.array([1,0])
    B = np.array([np.cos(t),np.sin(t)])
    xx = 0
    yy = 0
    for i in range(4):
        C = np.array([x[i][0],y[i][0]])
        if abs(angle(A,C,Ori)-alpha) < 1e-3 and abs(angle(B,C,Ori)-beta)<1e-3 and abs(angle(A,C,B)-gamma) < 1e-3 :
            if xx == 0 and yy == 0:
                xx = x[i][0]
                yy = y[i][0]
            else:
                if abs(xx**2+yy**2-1) > abs(x[i][0]**2+ y[i][0]**2-1):
                    xx = x[i][0]
                    yy = y[i][0]
    return np.array([xx,yy])

def normal_distribution(mu1,mu2,sigma):
    mean = [mu1,mu2]
    cov =  [[sigma**2,0],[0.0,sigma**2]]
    Pt = np.random.multivariate_normal(mean,cov,1)
    return round(Pt[0][0],2),round(Pt[0][1],2)

# 初始化
# 返回四个信息，分别是AccNo, Angle, AccPoint , CorrectPoint
# 前两者为接受无人机收到的信息，AccPoint为绘图信息, CorrectPoint为理想点坐标
def init(i,sigma):
    # 固定发射无人机编号i
    # TransimitNo = [0, 1, i]
    TransimitPoint = [np.array([0, 0]), np.array([1, 0]), np.array([np.cos((i-1)*np.pi/4.5), np.sin((i-1)*np.pi/4.5)])]
    # 随机接受无人机编号并且以error误差确定其坐标
    AccNo = random.randint(2, 9)
    while AccNo == i:
        AccNo = random.randint(2, 9)
    CorrectPoint = np.array([np.cos((AccNo-1)*np.pi/4.5),np.sin((AccNo-1)*np.pi/4.5)])
    # 正态分布
    x,y = normal_distribution(CorrectPoint[0],CorrectPoint[1],sigma)
    AccPoint = np.array([x,y])

    # 计算获得的三个角度 顺序为 0-j-1,0-j-i,1-j-i
    Angle = np.array([angle(TransimitPoint[0], AccPoint, TransimitPoint[1]),angle(TransimitPoint[0], AccPoint, TransimitPoint[2]),\
        angle(TransimitPoint[1], AccPoint, TransimitPoint[2])])

    # 前两者为接受无人机收到的信息，AccPoint为绘图信息,CorrectPoint为理想点坐标
    return AccNo, Angle, AccPoint , CorrectPoint

# 获取两点之间距离
def getdistance(pt1,pt2):
    return np.sum(np.square(pt1-pt2))

# 其他节点根据角度信息Coordinate，和正确坐标进行比较，如果存在距离小于等于distance，返回错误，如果距离都大于distance，返回正确
def CompareWithOtherPointCoordinate(distance,Angles,Except,TruePt):
    for i in range(2,10):
        if i != Except[0] and i != Except[1]:
            CoordinatePt = coordinate((i-1)*np.pi/4.5,Angles[0],Angles[1],Angles[2])
            if CoordinatePt[0] == 0 and CoordinatePt[1] == 0:
                continue
            Comparedistance = getdistance(CoordinatePt,TruePt)
            if Comparedistance <= distance:
                return False
    return True

# 绘制子图信息
def trans(i):
    if i == 0:
        return [0, 0]
    if i == 1:
        return [1, 0]
    if i == 2:
        return [0, 1]
    if i == 3:
        return [1, 1]

# 模拟程序(绘图版本)
def run_simulation():
    CorrectPoints = [np.array([0, 0])]
    for point in range(1, 10):
        CorrectPoints.append(np.array([np.cos((point-1)*np.pi/4.5), np.sin((point-1)*np.pi/4.5)]))

    # 使支持中文
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 绘制子图
    fig, axs = plt.subplots(2, 2 ,figsize=(12,12))

    for i in range(2, 6):
        for _ in range(MaxTestNum):
            No, Angles, AccPoint, CorrectPoint = init(i,0.1)
            TrueCoordinate = coordinate((i-1)*np.pi/4.5,Angles[0],Angles[1],Angles[2])
            if TrueCoordinate[0] == 0 and TrueCoordinate[1] == 0:
                print('---bug---')
            distance = getdistance(TrueCoordinate,CorrectPoint)
            reliable = CompareWithOtherPointCoordinate(distance,Angles,[i,No],CorrectPoint)
            if reliable:
                p2 = axs[trans(i-2)[0], trans(i-2)[1]].scatter(AccPoint[0],AccPoint[1],s=10,c='r')
            else:
                p3 = axs[trans(i-2)[0], trans(i-2)[1]].scatter(AccPoint[0],AccPoint[1],s=10,c='b')
        x = [point[0] for point in CorrectPoints]
        y = [point[1] for point in CorrectPoints]
        TranMitX = [CorrectPoints[0][0],CorrectPoints[1][0],CorrectPoints[i][0]]
        TranMitY = [CorrectPoints[0][1],CorrectPoints[1][1],CorrectPoints[i][1]]
        p1_2 = axs[trans(i-2)[0], trans(i-2)[1]].scatter(x, y, c='g',s = 20)
        p1_1 = axs[trans(i-2)[0], trans(i-2)[1]].scatter(TranMitX, TranMitY, c='k',s = 20)
    fig.legend([p1_1,p1_2,p2,p3], [u'发射机',u'接受机正确位置',u'接收机偏移有效定位位置',u'接收机偏移出错定位位置'])
    path='./unbounded_err_distribution.png'
    plt.savefig(path,dpi=400)

# 模拟程序(无绘图版本)
def run_simulation_WithoutPlot(sigma):
    Correctency = 0
    for i in range(2, 6):
        for _ in range(MaxTestNum):
            No, Angles, AccPoint, CorrectPoint = init(i,sigma)
            TrueCoordinate = coordinate((i-1)*np.pi/4.5,Angles[0],Angles[1],Angles[2])
            # 若三点一线会报错，无法处理
            if TrueCoordinate[0] == 0 and TrueCoordinate[1] == 0:
                print('---Three Point In Line!---')
            distance = getdistance(TrueCoordinate,CorrectPoint)
            reliable = CompareWithOtherPointCoordinate(distance,Angles,[i,No],CorrectPoint)
            if reliable:
                Correctency = Correctency + 1
    return round(float(Correctency)/4/MaxTestNum,3)

# 标准差减少计算正确率曲线
def std_correctency():
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    stds = np.linspace(0.1,0.6,6)
    Correctencys = []
    for sigma in stds:
        Correctency = run_simulation_WithoutPlot(sigma)
        Correctencys.append(Correctency)
    plt.plot(stds,Correctencys,"or-",label="标准差-正确率曲线")
    plt.xlabel("标准差")
    plt.ylabel("正确率")
    plt.legend(loc='best')
    path='./unbounded_err.png'
    plt.savefig(path,dpi=400)

#分布图
# run_simulation()
#描绘出标准差-正确率
std_correctency()
