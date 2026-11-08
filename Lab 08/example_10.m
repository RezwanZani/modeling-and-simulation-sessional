% Step 1: Create time vector and AC input voltage wave
t = linspace(0, 0.1, 1000);           % Time duration of 0.1s
V_in = sin(2 * pi * 50 * t);          % 50 Hz AC signal

% Step 2: Perform full-wave rectification
V_out = abs(V_in);

% Step 3: Plot input vs output waveforms
plot(t, V_in, t, V_out);
title('Full-Wave Rectifier Simulation');
xlabel('Time (s)');
ylabel('Voltage (V)');
legend('Input Voltage', 'Output Voltage');
grid on;
