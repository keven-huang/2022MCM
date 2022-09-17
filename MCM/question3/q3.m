% 输入input
polars = readmatrix('data.xlsx');

% r单位转化为100米,转化为弧度制
polars(1,:) = polars(1,:)/100;
polars(2,:) = polars(2,:)*pi/180;
disp(polars);

% 基础参数设定
dim = 2;                % 极坐标参数个数
flight_num = 10;        % 无人机数
max_iter_num = 10;      % 最大可能迭代次数
iter_num = 1;           % 迭代次数
R = 1;                  % 周长
error = 10^-5;          % 误差

% 迭代初始化init
flight_iter = zeros(dim,flight_num,max_iter_num);
flight_iter(:,:,iter_num) = polars;


% 1-4-7调整
r0 = flight_iter(1,8,iter_num);
t0 = 2*pi - flight_iter(2,8,iter_num);

while true
    iter_num = iter_num + 1;
    flight_iter(:,:,iter_num) = flight_iter(:,:,iter_num - 1);
    fun = @(t) r0*sin(t + t0 - 7*pi/6) - sin(5*pi/6 - t);
    t0 = fsolve(fun, 2*pi/3);  
    r0 = 2 * sin(5*pi/6-t0);   

    %调整4号无人机
    if mod(iter_num,2) == 0    
        flight_iter(2,5,iter_num) = t0;
        flight_iter(1,5,iter_num) = r0;
    %调整7号无人机
    else 
        flight_iter(2,8,iter_num) = 2*pi - t0;
        flight_iter(1,8,iter_num) = r0;
        
    end
    %若1号无人机,4号无人机与7号无人机在误差范围内呈等边三角,则认为调整完毕
    if abs(flight_iter(2,5,iter_num) - 2*pi/3) < error && abs(flight_iter(1,5,iter_num) - 1) < error ...
    && abs(flight_iter(2,8,iter_num) - 4*pi/3) < error && abs(flight_iter(1,8,iter_num) - 1) < error
        disp("break")
        break
    end
end

% 其余无人机节点调整
for flight = 2 : 10
    % 1 - 4 - 7 无须调整
    if flight == 2 && flight == 5 && flight == 8
        continue
    end

    iter_num = iter_num + 1;
    flight_iter(:,:,iter_num) = flight_iter(:,:,iter_num - 1);
    %其余无人机节点的处理,如问题1(定位并且调整角到正确的位置)
    ToPoint = CorrectPoint(R,flight);
    [the,rho] = cart2pol(ToPoint(1),ToPoint(2));
    [initx,inity] = pol2cart(flight_iter(2,flight,iter_num),flight_iter(1,flight,iter_num));
    flight_iter(2,flight,iter_num) = the;
    flight_iter(1,flight,iter_num) = rho;
%     distance=@(x,y)sqrt((x(2)-x(1))^2+(y(2)-y(1))^2);
%     ToAngle = atan((ToPoint(2) - inity)/(ToPoint(1) - initx));
%     direct = sprintf("flight %d should direct to %d",flight,ToAngle);
    disp(direct);
end

% 绘图
disp(shiftdim(flight_iter(1,5,:),1));
disp(shiftdim(flight_iter(2,5,:),1));
for i = 1 : flight_num
    a = shiftdim(flight_iter(2,i,:),1);
    b = shiftdim(flight_iter(1,i,:),1);
    polarplot(a,b,'-x','LineWidth',2);
    hold on
end
legend('0','1','2','3','4','5','6','7','8','9')
output = sprintf("总发送信号次数:%d",iter_num);
disp(output);

