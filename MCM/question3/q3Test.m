clear;
rng(sum(100*clock));

%参数设定
TestNum = 2;            % 最大测试数量
ErrRate = 0.1;          % 偏差率
dim = 2;                % 极坐标参数个数
Flag = 0;               % 是否收敛（调整成功）
Correctency = 0;        % 正确性
flight_num = 10;        % 无人机数
max_iter_num = 20;      % 最大可能迭代次数
iter_num = 1;           % 迭代次数
all_iter_num = 0;       % 总迭代次数
R = 1;                  % 周长
error = 10^-5;          % 误差

ErrRates = [0.1 0.12 0.14 0.16 0.18 0.2];       % 测试偏差率
iters = zeros(1,6);

%初始数据
polars = zeros(2,10);   
polars(1,1) = 0;
polars(2,1) = 0;
polars(1,2) = 1;
polars(2,2) = 0;

for rate = 1:6
    all_iter_num = 0;
    for i = 1:TestNum
        iter_num = 1;      
        Flag = 1;
        for j = 3:10
            polars(1,j) = 1 * (1+2*ErrRates(rate)*(rand-0.5));
            polars(2,j) = (j-2)*pi/4.5*(1+2*ErrRates(rate)*(rand-0.5));
        end
        disp(polars)
        % 迭代初始化init
        flight_iter = zeros(dim,flight_num,max_iter_num);
        flight_iter(:,:,iter_num) = polars;
        
        
        % 1-4-7调整
        r0 = flight_iter(1,8,iter_num);
        t0 = 2*pi - flight_iter(2,8,iter_num);
        
        for t = 1 : max_iter_num
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
                Flag = 1;
                break
            end
        end
        disp(iter_num);
        if Flag
            all_iter_num = all_iter_num + iter_num - 1;
            Correctency = Correctency + 1;
        end
    end
    % 输出
    avg_iter = all_iter_num/TestNum;
    iters(rate) = avg_iter;
    result = sprintf("平均调整次数：%d",avg_iter);
    disp(result)
end

plot(ErrRates,iters,'r-o');




