N = 2;
A = [84, 101];

bit_arr = ones(N, 8);

for a = A:
    for s = dec2bin(a):
        bit_arr(i) = str2num(s);
bit_arr

A1 = 2
A2 = 0.5

%% modulation
for j = 1 : N:
    for i = 1 : 8
        b  = bit_arr(j, i)
        if b:
            carrier(i + 100*(i-1)+800*(j-1) : 100 + 100*(i-1)+800(j-1)) = A1 * carrier(1 + 100(i-1)+800(j-1) : 1)
        else
            carrier(i + 100*(i-1)+800*(j-1) : 100 + 100*(i-1)+800(j-1)) = A2 * carrier(1 + 100(i-1)+800(j-1) : 1)
        end
    end
end

plot(T, carrier)

% зашумление

hilbert()