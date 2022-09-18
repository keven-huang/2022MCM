clear;

% 参数
ErrRate = 0.1;          % 偏差率
iter_num = 1;           % 迭代次数
max_iter_num = 15;      % 初始创建最大可能迭代次数
error = 10^-4;          % 误差
flight_num = 9;        % 无人机数

% 理想队列
idealform = [0 -1 -1 -1 -2 -2 -2 -2 -2;
             0  1  0 -1  2  1  0 -1 -2];
disp(idealform);

% 构造队列
form = zeros(2,flight_num);
for i = 1:flight_num
    form(1,i) = idealform(1,i) * (1 + ErrRate*2*(rand-0.5));
    form(2,i) = idealform(2,i) * (1 + ErrRate*2*(rand-0.5));
end
form(1,3) = -1;          % 认为1-3正确
disp(form);

% 迭代初始化init
flight_iter = zeros(2,flight_num,max_iter_num);
flight_iter(:,:,iter_num) = form;

F1 = form(:,1)';
F3 = form(:,3)';
F5 = form(:,5)';
F9 = form(:,9)';

% 1-3-5-9调整

% 提供角度信息                 A B C O
[res, conver_rate] = caculate(F1,F5,F9,F3);
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

[idealT9,idealR9] = cart2pol(idealform(1,9),idealform(2,9));
[idealT5,idealR5] = cart2pol(idealform(1,5),idealform(2,5));

[realT ,realR] = cart2pol(form(1,9),form(2,9));

D1 = (realR - idealR9)/idealR9;
d1 = realT - idealT9 ;

while true
    % 调整5号无人机
    iter_num = iter_num + 1;
    flight_iter(:,:,iter_num) = flight_iter(:,:,iter_num - 1);
    g1 = @(t) sin(a2)*sin(a1-t)-L1*(1+D1)*sin(b2)*sin(b3+t+d1);
    d2 = fsolve(g1,0);
    D2 = sin(a1-d2)/sin(b2)/L2-1;
    F5_PR = idealR5 * (1+D2);
    F5_PT = idealT5 + d2;
    [F5X,F5Y] = pol2cart(F5_PT,F5_PR);
    flight_iter(1,5,iter_num) = F5X;
    flight_iter(2,5,iter_num) = F5Y;

    % 调整9号无人机
    iter_num = iter_num + 1;
    flight_iter(:,:,iter_num) = flight_iter(:,:,iter_num - 1);
    g2 = @(t) sin(a2+t+d2)*sin(a3)*L2*(1+D2)-sin(b3)*sin(b1-t);
    d1 = fsolve(g2,0);
    D1 = sin(b1-d1)/sin(a3)/L1-1;
    F9_PR = idealR9 * (1+D1);
    F9_PT = idealT9 + d1;
    [F9X,F9Y] = pol2cart(F9_PT,F9_PR);
    flight_iter(1,9,iter_num) = F9X;
    flight_iter(2,9,iter_num) = F9Y;
    j = j + 1;
    ress(1,j) = d1;
    ress(2,j) = D1;
    %若1-3-5-9调整指定位置
    if abs(F9_PR-idealR9)<error && abs(F9_PT-idealT9)<error ...
            && abs(F5_PR-idealR5)<error && abs(F5_PT-idealT5)<error
        disp("break")
        break
    end
end

% 其余节点调整
for i = 1:9
    iter_num = iter_num + 1;
    flight_iter(:,:,iter_num) = flight_iter(:,:,iter_num - 1);
    if i ~= 1 && i ~= 3 && i ~= 5 && i~= 9
        flight_iter(1,i,iter_num) = idealform(1,i);
        flight_iter(2,i,iter_num) = idealform(2,i);
    end
end

% 绘图
disp(shiftdim(flight_iter(1,5,:),1));
disp(shiftdim(flight_iter(2,5,:),1));
for i = 1 : flight_num
    x = shiftdim(flight_iter(1,i,:),1);
    y = shiftdim(flight_iter(2,i,:),1);
    plot(x,y,'-x','LineWidth',2);
    hold on
end
legend('0','1','2','3','4','5','6','7','8','9')
