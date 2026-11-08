clc; clear; close all;

% Aircraft Battery Discharge Model (Exponential Decay)
initial_capacity = 100;  % Initial battery capacity (%)
discharge_rate = 0.08;   % Discharge constant (k)

% Flight time vector (0 to 10 hours)
t = linspace(0, 10, 100); 

% Exponential decay equation
capacity = initial_capacity * exp(-discharge_rate * t);

% Plotting the decay curve
figure('Name', 'Battery Discharge Model');
plot(t, capacity, 'b', 'LineWidth', 2.5);
grid on;
xlabel('Time in Flight (hours)');
ylabel('Capacity Remaining (%)');
title('UAV Battery Discharge Over Time');

% Calculate capacity at specific time (t = 5 hrs)
t_eval = 5;
cap_at_5 = initial_capacity * exp(-discharge_rate * t_eval);
fprintf('Battery remaining at 5 hours: %.2f%%\n', cap_at_5);

% Calculate time when capacity hits 20%
target_cap = 20;
t_target = -log(target_cap / initial_capacity) / discharge_rate;
fprintf('Time to reach 20%% capacity: %.2f hours\n', t_target);

% Mark data points on the plot
hold on;
plot(t_eval, cap_at_5, 'ms', 'MarkerSize', 8, 'MarkerFaceColor', 'm');
text(t_eval, cap_at_5 + 5, sprintf(' %.1f%% (5hr)', cap_at_5));

plot(t_target, target_cap, 'ks', 'MarkerSize', 8, 'MarkerFaceColor', 'k');
text(t_target, target_cap + 5, sprintf(' 20%% (%.1fhr)', t_target));
hold off;
