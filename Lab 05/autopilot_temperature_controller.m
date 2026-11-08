clc; clear; close all;

% Aircraft Cabin Temperature Control (Negative Feedback)
T_target = 20;       % Setpoint temperature (C)
T_initial = 30;      % Starting temperature (C)
feedback_gain = 0.5; % Proportional control constant (k)

% Run simulation for 20 minutes
t_range = [0 20]; 

% Solve the differential equation with ode45
[time_sim, Temp_sim] = ode45(@(t, T) temp_dynamics(t, T, feedback_gain, T_target), t_range, T_initial);

% Plotting the system response
figure('Name', 'Cabin Temp Control');
plot(time_sim, Temp_sim, 'b', 'LineWidth', 2);
hold on;
yline(T_target, 'r--', 'LineWidth', 1.5); % Draw target line
grid on;

xlabel('Simulation Time (mins)');
ylabel('Temperature (Celsius)');
title('Cabin Temperature Feedback Regulation');
legend('System Response', 'Target Setpoint');

% Identify when temperature reaches within 0.1C of target
tol = 0.1; 
idx_reached = find(abs(Temp_sim - T_target) < tol, 1);

if ~isempty(idx_reached)
    fprintf('Target achieved (~%.1fC) at %.2f minutes.\n', T_target, time_sim(idx_reached));
else
    fprintf('Target not reached within simulation time.\n');
end

% Define the ODE function
function dT_dt = temp_dynamics(~, T, k, T_set)
    % Rate of change depends on the error (T - T_set)
    dT_dt = -k * (T - T_set);
end
