function [res, conver_rate] = caculate(A,B,C,O)
    a1 = angle(O,A,B);
    b1 = angle(O,A,C);
    a2 = angle(O,B,C);
    b2 = angle(O,B,A);
    a3 = angle(O,C,A);
    b3 = angle(O,C,B);

    OB = O-B;
    OC = O-C;
    L2 = sqrt(OB(1)^2+OB(2)^2);
    L1 = sqrt(OC(1)^2+OC(2)^2);
    conver_rate = (cot(b3)-cot(b1))/(cot(a1)+cot(b3))*(cot(a2)-cot(a1))/(cot(a2)+cot(b1));
    res = [a1,b1,a2,b2,a3,b3,L1,L2]; 
end