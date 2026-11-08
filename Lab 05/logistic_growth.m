clc; clear; close all;

% UAV Fleet Growth Model: Logistic vs Exponential
pop_initial = 50;    % Starting number of drones
max_capacity = 1000; % Maximum fleet capacity (K)
growth_rate = 0.4;   % Rate of growth (r)

time_yrs = 0:0.2:20; % Simulation over 20 years

% Compute Logistic Growth
P_log = max_capacity ./ (1 + ((max_capacity - pop_initial)/pop_initial) .* exp(-growth_rate .* time_yrs));

% Compute Unlimited Exponential Growth
P_exp = pop_initial .* exp(growth_rate .* time_yrs);

% Generate Comparison Plot
figure('Name', 'Drone Population Growth');
plot(time_yrs, P_log, 'g', 'LineWidth', 2.5);
hold on;
plot(time_yrs, P_exp, 'r-.', 'LineWidth', 2);
grid on;

xlabel('Time (Years)');
ylabel('Fleet Size (Number of Drones)');
title('UAV Fleet Expansion: Restricted vs Unrestricted');
legend('Logistic (Cap: 1000)', 'Exponential (Unlimited)', 'Location', 'northwest');

% Output final populations at t = 20
t_final = 20;
final_logistic = max_capacity / (1 + ((max_capacity - pop_initial)/pop_initial) * exp(-growth_rate * t_final));
final_exponential = pop_initial * exp(growth_rate * t_final);

fprintf('--- 20 Year Projection ---\n');
fprintf('Logistic Model Output: %d drones\n', round(final_logistic));
fprintf('Exponential Model Output: %d drones\n', round(final_exponential));
