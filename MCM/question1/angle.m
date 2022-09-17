function anglebac = angle(b, a, c)
    anglebac=acos((dot((b-a),(c-a)))/(norm(b-a)*norm(a-c)));
end
