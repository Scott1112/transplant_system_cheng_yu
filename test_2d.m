clc, clear;

camera_x_1 = 589;
camera_y_1 = 526;
camera_x_2 = 1017;
camera_y_2 = 526;

true_x_1   = -50.8;
true_y_1   = -179.42;
true_x_2   = 257.44;
true_y_2   = -179.42;

% 定義函式
syms f1(a11,a12) f2(a11,a12) f3(a21,a22) f4(a21,a22);
f1 = camera_x_1*a11 + camera_y_1*a12 - (true_x_1);
f2 = camera_x_2*a11 + camera_y_2*a12 - (true_x_2);
f3 = camera_x_1*a21 + camera_y_1*a22 - (true_z_1);
f4 = camera_x_2*a21 + camera_y_2*a22 - (true_z_2);

% 求解方程組
[a11, a12] = solve(f1, f2);
[a21, a22] = solve(f3, f4);
disp(vpa([a11 a12],4))
disp(vpa([a21 a22],4))

