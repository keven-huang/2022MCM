function res = coordinate(t,alpha,beta,gamma)
k=1;
A = zeros(4,1);x=zeros(4,1);y=zeros(4,1);X=zeros(4,1);Y=zeros(4,1);
a = [alpha,alpha,-alpha,-alpha];
b = [beta,-beta,beta,-beta];
for i = 1:4
    A(i) = (cos(t)/tan(b(i))-sin(t)-1/tan(a(i)))/(cos(t)+sin(t)/tan(b(i))-1);
    y(i) = (A(i)-1/tan(a(i)))/(A(i)^2+1);
    x(i) = A(i)*y(i);
    k1 = (sin(t)-y(i))/(cos(t)-x(i));
    k2 = (y(i))/(x(i)-1);
    if abs((k1-k2)/(1+k1*k2)-tan(gamma))<10^(-10) || abs((k1-k2)/(1+k1*k2)+tan(gamma))<10^(-10)
        X(k)=x(i);Y(k)=y(i);k=k+1;
    end
    for k = 1:4
       if abs(X(k)^2+Y(k)^2-1) <10^(-10)
           xx = X(k); yy = Y(k);
       end
    end
end
res = [xx,yy];