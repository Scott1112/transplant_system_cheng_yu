clc, clear;

camera_x_1 = 304;
camera_y_1 = 611;
camera_z_1 = 61.4;

camera_x_2 = 710;
camera_y_2 = 611;
camera_z_2 = 58.8;

camera_x_3 = 946;
camera_y_3 = 611;
camera_z_3 = 63.6;

true_x_1   = -196.37;
true_y_1   = -174.98;
true_z_1   = 484.94;

true_x_2   = 100.89;
true_y_2   = -174.98;
true_z_2   = 462.36;

true_x_3   = 246.65;
true_y_3   = -174.98;
true_z_3   = 513.91; % 左邊


% 定義函式
syms f1(a11,a12,a13) f2(a11,a12,a13) f3(a11,a12, a13) f4(a21,a22,a23) f5(a21,a22,a23) f6(a21,a22,a23) f7(a31,a32,a33) f8(a31,a32,a33) f9(a31,a32,a33);

f1 = camera_x_1*a11 + camera_y_1*a12 + camera_z_1*a13 - (true_x_1);
f2 = camera_x_2*a11 + camera_y_2*a12 + camera_z_2*a13 - (true_x_2);
f3 = camera_x_3*a11 + camera_y_3*a12 + camera_z_3*a13 - (true_x_3);

f4 = camera_x_1*a21 + camera_y_1*a22 + camera_z_1*a23 - (true_z_1);
f5 = camera_x_2*a21 + camera_y_2*a22 + camera_z_2*a23 - (true_z_2);
f6 = camera_x_3*a21 + camera_y_3*a22 + camera_z_3*a23 - (true_z_3);

f7 = camera_x_1*a31 + camera_y_1*a32 + camera_z_1*a33 - (true_y_1);
f8 = camera_x_2*a31 + camera_y_2*a32 + camera_z_2*a33 - (true_y_2);
f9 = camera_x_3*a31 + camera_y_3*a32 + camera_z_3*a33 - (true_y_3);


% 求解方程組
[a11, a12, a13] = solve(f1, f2, f3);
[a21, a22, a23] = solve(f4, f5, f6);
[a31, a32, a33] = solve(f7, f8, f9);

disp(vpa([a11 a12 a13],3))
disp(vpa([a21 a22 a23],3))
disp(vpa([a31 a32 a33],3))
