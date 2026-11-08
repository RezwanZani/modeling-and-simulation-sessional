% Step 1: Define circuit components
R = 1e3;   % Resistance in ohms
C = 1e-6;  % Capacitance in farads

% Step 2: Define transfer function H(s) = 1 / (RC*s + 1)
sys = tf([1], [R*C 1]);

% Step 3: Plot impulse response
impulse(sys);
title('Transient Response of RC Circuit');
