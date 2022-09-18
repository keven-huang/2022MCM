% 定位算法测试 Test of Coordinate Algorithm
% 失效情况，夹角为0
rng(sum(100*clock))

ErrorRate = 0.2; %误差20%
err = 10^(-5);   %容许测定误差
TestNum = 100;   %测试100个点
R = 1;           %基础半径定义为1
Correct = 0;     %测试正确个数

% 已知发射信号无人机
F00 = [0 0];
F01 = [1 0];

% 发射信号无人人机编号
for j = 2:5
    Correct = 0;

    F0j = [R*cos(pi*(j-1)/4.5) R*sin(pi*(j-1)/4.5)];
    [F00_pT,F00_pR] = cart2pol(F00(1),F00(2));
    [F01_pT,F01_pR] = cart2pol(F01(1),F01(2));
    [F0j_pT,F0j_pR] = cart2pol(F0j(1),F0j(2));

    TransmitPtR = [F00_pR F01_pR F0j_pR];
    TransmitPtT = [F00_pT F01_pT F0j_pT];
    disp(TransmitPtT);
    polarscatter(TransmitPtT,TransmitPtR,'k','filled');
    hold on
    for i = 1 : TestNum
        % 随机接受无人机极坐标
        r = R*(1+ErrorRate*rand);
        FlightNo = randi([1,8]);
        while FlightNo == j-1
            FlightNo = randi([1,8]);
        end
        theta = pi/4.5*FlightNo*(1+rand*ErrorRate);
        

        %计算角度
        [FlightPointX,FlightPointY] = pol2cart(r,theta);
        FlightPoint = [FlightPointX,FlightPointY];
        alpha = angle(F01,FlightPoint,F00);
        beta = angle(F0j,FlightPoint,F00);
        gamma = angle(F01,FlightPoint,F0j);
        t = pi*(j-1)/4.5;

        % 发送无人机提供给接受无人机的角度信息
        % alpha beta gammer 夹角 t 是F01,F00与F0j的夹角
        ProvideAngle = [t,alpha,beta,gamma];

        % 计算
        PlaceRes = coordinate(t,alpha,beta,gamma);
        
        %验证
        if abs(PlaceRes(1) - FlightPoint(1)) < err && ...
           abs(PlaceRes(2) - FlightPoint(2)) < err
            polarscatter(theta,r,'r','filled');
            hold on
            Correct = Correct + 1;
        else
            polarscatter(theta,r,'b','filled');
            hold on
        end
    end
    hold off
    frame = getframe;
    img = frame.cdata;
    imgName = sprintf("%d-%d.png",j,Correct);
    imwrite(img,imgName);
end


