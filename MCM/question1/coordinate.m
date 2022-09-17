function res = coordinate(t,alpha,beta,gamma)
A = zeros(4,1);x=zeros(4,1);y=zeros(4,1);
a = [alpha,alpha,-alpha,-alpha];
b = [beta,-beta,beta,-beta];
for i = 1:4
    A(i) = (cos(t)/tan(b(i))-sin(t)-1/tan(a(i)))/(cos(t)+sin(t)/tan(b(i))-1);
    y(i) = (A(i)-1/tan(a(i)))/(A(i)^2+1);
    x(i) = A(i)*y(i);
end
O= [0,0];A= [1,0];B=[cos(t),sin(t)];
for i = 1:4
   C = [x(i),y(i)];
   if abs(angle(A,C,O)-alpha)<10^(-5) && abs(angle(B,C,O)-beta)<10^(-5) && abs(angle(A,C,B)-gamma)<10^(-5)
      xx = x(i);yy = y(i); 
   end
end    
res = [xx,yy];