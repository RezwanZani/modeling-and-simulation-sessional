clc; clear; close all;

% UAV Altitude Controller (Nonlinear Dynamics)
gravity = 9.81;    % Gravity acceleration (m/s^2)
drag_coeff = 0.05; % Nonlinear drag constant (c)
thrust_cmd = 15.0; % Upward thrust (u)

% Initial State: [Altitude; Velocity]
state_0 = [0; 0]; 

sim_time = [0 20]; % 20 seconds simulation

% Solve ODE with Nonlinear Drag
[t_drag, state_drag] = ode45(@(t, x) uav_dynamics(t, x, thrust_cmd, gravity, drag_coeff), sim_time, state_0);
alt_drag = state_drag(:, 1);
vel_drag = state_drag(:, 2);

% Solve ODE Without Drag (c = 0)
[t_nodrag, state_nodrag] = ode45(@(t, x) uav_dynamics(t, x, thrust_cmd, gravity, 0), sim_time, state_0);
alt_nodrag = state_nodrag(:, 1);

% Plot 1: Altitude Comparison
figure('Name', 'Altitude Tracking');
plot(t_drag, alt_drag, 'b', 'LineWidth', 2);
hold on;
plot(t_nodrag, alt_nodrag, 'r--', 'LineWidth', 2);
grid on;
xlabel('Time (s)');
ylabel('Altitude (m)');
title('UAV Altitude: Drag vs No Drag');
legend('With Aerodynamic Drag', 'Ideal (No Drag)', 'Location', 'northwest');

% Plot 2: Velocity Profile
figure('Name', 'Velocity Profile');
plot(t_drag, vel_drag, 'g', 'LineWidth', 2);
grid on;
xlabel('Time (s)');
ylabel('Vertical Speed (m/s)');
title('UAV Climb Velocity (With Drag)');

% Dynamics Function Definition
function dx_dt = uav_dynamics(~, state, u, g, c)
    h = state(1); % current altitude
    v = state(2); % current velocity
    
    h_dot = v;
    v_dot = u - g - (c * v * abs(v)); % nonlinear drag term
    
    dx_dt = [h_dot; v_dot];
end
