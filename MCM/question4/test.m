clear;

% 参数
ErrRate = 0.1;          % 偏差率
iter_num = 1;           % 迭代次数
max_iter_num = 1;      % 初始创建最大可能迭代次数
error = 10^-3;          % 误差
flight_num = 4;        % 无人机数

% 理想队列
% idealform = [0 1 0 -2;
%              0 0 1 -1];
% liner
idealform = [0.8408 0.0093 1.6212 2.0325;
            1.3517 1.9073 0.3122 1.1602];
disp(idealform);

% 构造队列
form = zeros(2,flight_num);
for i = 1:flight_num
    form(1,i) = idealform(1,i) * (1 + ErrRate*2*(rand-0.5));
    form(2,i) = idealform(2,i) * (1 + ErrRate*2*(rand-0.5));
end
form(1,1) = idealform(1,1);          % 认为1-2正确
form(2,1) = idealform(2,1);
form(1,2) = idealform(1,2);          
form(2,2) = idealform(2,2);
disp(form);

% 迭代初始化init
flight_iter = zeros(2,flight_num,max_iter_num);
flight_iter(:,:,iter_num) = form;

F1 = form(:,1)';
F2 = form(:,2)';
F3 = form(:,3)';
F4 = form(:,4)';
% 1-3-5-9调整

% 提供角度信息                 A B C O
[res, conver_rate] = caculate(F2,F3,F4,F1);
disp(conver_rate);

% Debug
j = 1;
ress = zeros(2,max_iter_num);
% 提取角信息
a1 = res(1);
b1 = res(2);
a2 = res(3);
b2 = res(4); 
a3 = res(5);
b3 = res(6);
L1 = res(7);
L2 = res(8);

[idealT4,idealR4] = cart2pol(idealform(1,4),idealform(2,4));
[idealT3,idealR3] = cart2pol(idealform(1,3),idealform(2,3));

[realT ,realR] = cart2pol(form(1,4),form(2,4));

D1 = (realR - idealR4)/idealR4;
d1 = realT - idealT4 ;

while true
    % 调整3号无人机
    iter_num = iter_num + 1;
    flight_iter(:,:,iter_num) = flight_iter(:,:,iter_num - 1);
    g1 = @(t) sin(a2)*sin(a1-t)-L1*(1+D1)*sin(b2)*sin(b3+t+d1);
    d2 = fsolve(g1,0);
    D2 = sin(a1-d2)/sin(b2)/L2-1;
    F3_PR = idealR3 * (1+D2);
    F3_PT = idealT3 + d2;
    [F3X,F3Y] = pol2cart(F3_PT,F3_PR);
    flight_iter(1,3,iter_num) = F3X;
    flight_iter(2,3,iter_num) = F3Y;

    % 调整4号无人机
    iter_num = iter_num + 1;
    flight_iter(:,:,iter_num) = flight_iter(:,:,iter_num - 1);
    g2 = @(t) sin(a2+t+d2)*sin(a3)*L2*(1+D2)-sin(b3)*sin(b1-t);
    d1 = fsolve(g2,0);
    D1 = sin(b1-d1)/sin(a3)/L1-1;
    F4_PR = idealR4 * (1+D1);
    F4_PT = idealT4 + d1;
    [F4X,F4Y] = pol2cart(F4_PT,F4_PR);
    flight_iter(1,4,iter_num) = F4X;
    flight_iter(2,4,iter_num) = F4Y;
    j = j + 1;
    ress(1,j) = d1;
    ress(2,j) = D1;
    %若调整指定位置
    if abs(F4_PR-idealR4)<error && abs(F4_PT-idealT4)<error ...
            && abs(F3_PR-idealR3)<error && abs(F3_PT-idealT3)<error
        disp("break")
        break
    end
end


% 绘图
disp(shiftdim(flight_iter(1,3,:),1));
disp(shiftdim(flight_iter(2,3,:),1));
for i = 1 : flight_num
    x = shiftdim(flight_iter(1,i,:),1);
    y = shiftdim(flight_iter(2,i,:),1);
    plot(x,y,'-x','LineWidth',2);
    hold on
end
legend('1','2','3','4')