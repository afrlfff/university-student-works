% load filter object
if ~exist('filter_object.mat', 'file')
    error('Файл filter_object.mat не найден. Сначала выполните design_filter.m');
end
load('filter_object.mat', 'Hd');

% define main variables
fs = 48000;
x = out.simout;
N = length(x);
t = linspace(0, (N - 1) / fs, N);
[b, a] = tf(Hd);

% get filtered signal
y = filter(b, a, x);

figure('Position', [100, 100, 1000, 600]);

% 1st plot
subplot(2, 1, 1);
plot(t, x, color='Blue');
title('Входной сигнал');
xlabel('t, [с]');
ylabel('V, [u]');
grid on;

% 2nd plot
subplot(2, 1, 2);
plot(t, y, color='Blue');
title('Выходной сигнал');
xlabel('t, [с]');
ylabel('V, [u]');
grid on;


figure('Position', [50, 100, 1500, 600]);

% 3rd plot
[pxx, f, pxxc] = periodogram(x, rectwin(length(x)), length(x), fs);
subplot(1, 2, 1);
plot(f, 10*log10(pxxc(:, 2)));
title('Периодограмма входного сигнала');
xlabel('Hz');
ylabel('dB/Hz)');
xlim([-50, 2000]);
grid on;

% 4th plot
[pxx, f, pxxc] = periodogram(y, rectwin(length(y)), length(y), fs);
subplot(1, 2, 2);
plot(f, 10*log10(pxxc(:, 2)));
title('Периодограмма выходного сигнала');
xlabel('Hz');
ylabel('dB/Hz)');
xlim([-50, 2000]);
grid on;