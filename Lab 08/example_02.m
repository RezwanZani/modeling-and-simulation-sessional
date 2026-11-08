% Step 1: Define circuit components
R = 1e3; % Resistance in ohms
L = 1e-3; % Inductance in henries

% Step 2: Calculate transfer function H(s) = Ls / (Ls + R)
H = tf([L 0], [L R]);

% Step 3: Plot Bode frequency response
bode(H);
title('Frequency Response of RL High-Pass Filter');
grid on;
