rand('seed',sum(100*clock));
x1 = rand;
x2 = rand;
r0 = 1.05;
t0 = 2*pi - 4.18;
mlist = zeros(2,10);
for j = 1:5
    fun = @(t) r0*sin(t + t0 - 7*pi/6) - sin(5*pi/6 - t);
    t0 = fsolve(fun, 2*pi/3);
    r0 = 2 * sin(5*pi/6-t0);
    disp(r0);
    disp(t0);
    mlist(1,j)=abs(r0-1);
    mlist(2,j)=abs(t0-2*pi/3);
end