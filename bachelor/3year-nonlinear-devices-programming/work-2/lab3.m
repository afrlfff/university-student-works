function main()
    Tmax = 5e-3;
    h = 1e-8;
    T = 0:h:Tmax;
    initial_conditions = [0, 0, 0];

    result = zeros(3, length(T));
    result(:, 1) = initial_conditions;

    i = 2;
    while i <= length(T)
        if any(abs(result(:, i - 1)) > 10000)
            fprintf('Расчет прерван на шаге %d: [%f, %f, %f]\n', ...
                i - 1, result(i - 1, 1), result(i - 1, 2), result(i - 1, 3));
            break;
        end

        result(:, i) = result(:, i - 1) + h * func(T(i - 1), result(:, i - 1));
        i = i + 1;
    end

    build_all(result, i - 1);
end

function Ydot = func(t, Y)
    V_CE = Y(1);
    V_BE = Y(2);
    I_L = Y(3);

    V_CC = 5; V_EE = -5;
    R_L = 40;
    R_EE = 700;
    R_ON = 10;
    L = 100e-6;
    C1 = 47e-9;
    C2 = 47e-9;
    V_TN = 0.75;
    beta = 100;

    I_B = (V_BE <= V_TN) * 0 + (V_BE > V_TN) * ((V_BE - V_TN) / R_ON);
    I_C = beta * I_B;

    dV_CE = (1 / C1) * (I_L - I_C);
    dV_BE = (1 / C2) * ((-V_BE - V_EE) / R_EE - C1 * dV_CE - I_C - I_B);
    %dV_BE = (1 / C2) * (I_L - C1 * dV_CE - I_C - I_B);
    dI_L = (1 / L) * (V_CC - V_CE + V_BE - I_L * R_L);

    Ydot = [dV_CE; dV_BE; dI_L];
end

function build_all(result, i)
    figure;

    subplot(1, 3, 1);
    plot(result(1, 1:i), result(2, 1:i), 'b');
    xlabel('V_C_E');
    ylabel('V_B_E');
    grid on;

    subplot(1, 3, 2);
    plot(result(1, 1:i), result(3, 1:i), 'b');
    xlabel('V_C_E');
    ylabel('I_L');
    grid on;

    subplot(1, 3, 3);
    plot(result(2, 1:i), result(3, 1:i), 'b');
    xlabel('V_B_E');
    ylabel('I_L');
    grid on;
end