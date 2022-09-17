import numpy as np


def angle(b, a, c):
    return np.arccos(np.dot((b-a), (c-a))/(np.sqrt(np.sum((b-a)*(b-a)))*np.sqrt(np.sum((c-a)*(c-a)))))


def angle1(b, a, c):
    res = np.arccos(np.dot((b-a), (c-a)) /
                    (np.sqrt(np.sum((b-a)*(b-a)))*np.sqrt(np.sum((c-a)*(c-a)))))
    return round(res, 3)


mylist = np.zeros((336, 9))
t = 0
Ori = np.array([0, 0])
A = np.array([1, 0])
for k in range(8):
    for i in range(8):
        for j in range(i+1,8):
            if i != j and i != k and j != k:
                mylist[t, 0] = int(i) + 2
                mylist[t, 1] = int(j) + 2
                mylist[t, 2] = int(k) + 2
                # X3接受
                X1 = np.array([np.cos((i+1)*np.pi/4.5),
                              np.sin((i+1)*np.pi/4.5)])
                X2 = np.array([np.cos((j+1)*np.pi/4.5),
                              np.sin((j+1)*np.pi/4.5)])
                X3 = np.array([np.cos((k+1)*np.pi/4.5),
                              np.sin((k+1)*np.pi/4.5)])
                addArr = np.array([angle1(Ori,X3,A)])
                tmp = np.array([angle1(Ori,X3, X1), angle1(Ori,X3,X2),angle1(A,X3,X1),angle1(A,X3,X2),angle1(X1,X3,X2)])
                tmp = np.sort(tmp)
                addArr = np.append(addArr,tmp)
                mylist[t, 3:] = addArr
                t = t + 1
mydic = {}
for k in range(168):
    if tuple(list(mylist[k, 3:])) in mydic.keys():
        mydic[tuple(list(mylist[k, 3:]))].append(tuple(list(mylist[k, 0:3])))
    else:
        mydic[tuple(list(mylist[k, 3:]))] = [tuple(list(mylist[k, 0:3]))]
