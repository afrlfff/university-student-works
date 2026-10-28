% ==== START PROGRAM ==== %

text = "Test message";

% ==== Transoform text to bits
% char_arr = reshape(char(text), 1, []);
% num_arr = uint8(char_arr);
% N = length(num_arr);
% bit_arr = zeros(N, 8);
% for j = 1 : N
%     num = num_arr(j);
%     for i = 1 : 8
%         bit_arr(j, i) = bitand(bitshift(num, -1 * (8 - i)), 0b0000001);
%     end
% end


% ==== Define Signal
f = 10;
amp = 1;
duration = 2; % in seconds
Fs = 1000; % sampling rate

number_of_points = Fs * duration + 1; % [0, ..., Fs * duration]
points_t = (0 : number_of_points - 1) * (1 / Fs);
S = zeros(number_of_points);
for i = 1 : (number_of_points)
    S(i) = sin(2 * pi * f * points_t(i)) * amp;
end
%plot(points_t, S, "Color", "blue", "LineWidth", 1.5);
%xlim([0, 1]);


% ==== Transorm to frequency domain
% points_f = (0 : number_of_points - 1) * Fs / number_of_points;
% S_FFT = fft(S);
% ampl_spectrum = abs(S_FFT);
% ampl_spectrum = ampl_spectrum / (number_of_points / 2);
%stem(points_f, ampl_spectrum, "Marker", "_", "LineWidth", 1.5, "Color", "blue");


% ==== Add noise to Signal
f = 1;
amp = 100;
noise = zeros(number_of_points);
for i = 1 : number_of_points
    noise(i) = sin(2 * pi * f * points_t(i)) * amp;
end
S = S + noise;
%plot(points_t, noise, "Color", "blue", "LineWidth", 1.5);
%plot(points_t, S, "Color", "blue", "LineWidth", 1.5);
%S_FFT = fft(S);
%ampl_spectrum = abs(S_FFT);
%ampl_spectrum = ampl_spectrum / (number_of_points / 2);
%stem(points_f, ampl_spectrum, "Marker", "_", "LineWidth", 1.5, "Color", "blue");


% ==== Filtration using FIR
S_filtered = filter(Hhp_FIR.coeffs.Numerator, 1, S);
plot(points_t, S, "Color", "blue");
hold on;
plot(points_t, S_filtered, "Color", "red");
hold off;

% ==== END PROGRAM ==== %