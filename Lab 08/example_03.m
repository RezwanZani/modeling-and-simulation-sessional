% Step 1: Define circuit components
R = 5;       % Resistance in ohms
L = 1e-3;    % Inductance in henrys
C = 100e-6;  % Capacitance in farads

% Step 2: Calculate transfer function H(s) = 1 / (LC*s^2 + RC*s + 1)
sys = tf([1], [L*C R*C 1]);

% Step 3: Plot step response
step(sys);
title('Series RLC Circuit Step Response');
