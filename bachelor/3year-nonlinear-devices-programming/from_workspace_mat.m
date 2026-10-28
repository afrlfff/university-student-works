t = 0:0.01:10;
tau = 5;
y1 = t < tau;
y2 = sin(2 * pi * 10/tau * t);
y = y1 .* y2;
plot(t, y)
simin = [t', y'];