% Очистка рабочей области и закрытие всех открытых графиков
clear;
clc;
close all;

function result = MakeSignal(A, f, t)
    result = A * sin(2 * pi * f * t);
end

Fs = 1000;
t = 0 : 1/Fs : 1;
y1 = MakeSignal(10, 5, t);
y2 = MakeSignal(3, 15, t);
y3 = MakeSignal(1, 25, t);


figure;
subplot(4, 1, 1);
plot(t, y1)

subplot(4, 1, 2);
plot(t, y2)

subplot(4, 1, 3);
plot(t, y3)

subplot(4, 1, 4);
plot(t, y1 + y2 + y3)
xlabel('t');
ylabel('y(t)');
grid on;