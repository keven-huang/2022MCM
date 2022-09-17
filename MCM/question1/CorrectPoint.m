function point = CorrectPoint(R,i)
% i >= 2 及编号为01-09
if i >= 2 
    x = R*cos(2*pi/9*(i-2));
    y = R*sin(2*pi/9*(i-2));
    point = [x,y];
% i == 1 编号为0
else
    point = [0,0];
end
end
