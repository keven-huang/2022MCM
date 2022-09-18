clc;clear;clf;
rng(sum(100*clock));
D1 = 0.2*rand;
d1 = 0.2*rand;
Flag = 1;
st = 0;
while Flag == 1 && st<100
    st = st+1;
    x1 = 3*rand()-1;
    x2 = 3*rand();
    x3 = 3*rand();
    y1 = 3*rand();
    y2 = 3*rand()-1;
    y3 = 3*rand();

    tx = [x1 x2 x3 x1];
    ty = [y1 y2 y3 y1];
    A = [x1 y1 0]; 
    B = [x2 y2 0]; 
    C = [x3 y3 0]; 
    plot(tx,ty);
    hold on;
    % x,y是O
    for i = 1:32
        x = x1 + cos(i*pi/16);
        y = y1 + sin(i*pi/16);
        O = [x y 0]; 
        AB = A-B;
        AP = A-O;
        AC = A-C;
        BA = B-A;
        BP = B-O;
        BC = B-C;
        BABP = cross(BA,BP);
        BPBC = cross(BP,BC);
        ABAP = cross(AB,AP);
        APAC = cross(AP,AC);
        if BABP(3)*BPBC(3) > 0 &&  ABAP(3)*APAC(3) > 0
            plot(x,y,'ro');
            [res, conver_rate] = caculate(A,B,C,O);
            disp(triangle_inner_point_method(res,D1,d1))
            disp(conver_rate)
            Flag = 0;
            break
        else
            continue
        end
    end
    if Flag == 1
        hold off
        disp("未找到");
    end
end
 

 

 
 
 