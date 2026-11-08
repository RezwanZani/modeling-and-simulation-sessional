% 2D Incompressible Navier-Stokes (Lid-Driven Cavity Flow)
% Tested for MATLAB R2025a

clc; clear; close all;

% 1. Grid and Parameters
nx = 41; ny = 41;       % Grid size
nt = 500; nit = 50;     % Time steps and pressure iterations
dx = 2 / (nx - 1); 
dy = 2 / (ny - 1);
dt = 0.001;             % Time step
rho = 1; nu = 0.1;      % Density and Kinematic Viscosity

% 2. Initialization
u = zeros(ny, nx); v = zeros(ny, nx); p = zeros(ny, nx);
[X, Y] = meshgrid(linspace(0, 2, nx), linspace(0, 2, ny));

% 3. Main Time Loop
figure('Name', 'Navier-Stokes Simulation', 'Color', 'w');
for n = 1:nt
    un = u; vn = v;
    
    % Predictor step (nonlinear advection and viscous diffusion)
    u(2:end-1, 2:end-1) = un(2:end-1, 2:end-1) - ...
        un(2:end-1, 2:end-1) .* dt / dx .* (un(2:end-1, 2:end-1) - un(2:end-1, 1:end-2)) - ...
        vn(2:end-1, 2:end-1) .* dt / dy .* (un(2:end-1, 2:end-1) - un(1:end-2, 2:end-1)) + ...
        nu * dt / dx^2 * (un(2:end-1, 3:end) - 2 * un(2:end-1, 2:end-1) + un(2:end-1, 1:end-2)) + ...
        nu * dt / dy^2 * (un(3:end, 2:end-1) - 2 * un(2:end-1, 2:end-1) + un(1:end-2, 2:end-1));
        
    v(2:end-1, 2:end-1) = vn(2:end-1, 2:end-1) - ...
        un(2:end-1, 2:end-1) .* dt / dx .* (vn(2:end-1, 2:end-1) - vn(2:end-1, 1:end-2)) - ...
        vn(2:end-1, 2:end-1) .* dt / dy .* (vn(2:end-1, 2:end-1) - vn(1:end-2, 2:end-1)) + ...
        nu * dt / dx^2 * (vn(2:end-1, 3:end) - 2 * vn(2:end-1, 2:end-1) + vn(2:end-1, 1:end-2)) + ...
        nu * dt / dy^2 * (vn(3:end, 2:end-1) - 2 * vn(2:end-1, 2:end-1) + vn(1:end-2, 2:end-1));
        
    % Pressure Poisson Equation (iterative solver)
    rhs = rho / dt * ((u(2:end-1, 3:end) - u(2:end-1, 1:end-2)) / (2 * dx) + ...
                      (v(3:end, 2:end-1) - v(1:end-2, 2:end-1)) / (2 * dy));
    for q = 1:nit
        pn = p;
        p(2:end-1, 2:end-1) = ((pn(2:end-1, 3:end) + pn(2:end-1, 1:end-2)) * dy^2 + ...
                               (pn(3:end, 2:end-1) + pn(1:end-2, 2:end-1)) * dx^2 - ...
                               rhs * dx^2 * dy^2) / (2 * (dx^2 + dy^2));
        % Pressure Boundary Conditions
        p(:, end) = p(:, end-1);   % dp/dx = 0 at x = 2
        p(1, :) = p(2, :);         % dp/dy = 0 at y = 0
        p(:, 1) = p(:, 2);         % dp/dx = 0 at x = 0
        p(end, :) = 0;             % p = 0 at top wall
    end
    
    % Corrector step (apply pressure gradient to velocity)
    u(2:end-1, 2:end-1) = u(2:end-1, 2:end-1) - dt / rho * (p(2:end-1, 3:end) - p(2:end-1, 1:end-2)) / (2 * dx);
    v(2:end-1, 2:end-1) = v(2:end-1, 2:end-1) - dt / rho * (p(3:end, 2:end-1) - p(1:end-2, 2:end-1)) / (2 * dy);
    
    % Velocity Boundary Conditions (No-slip walls, Lid moving at u=1)
    u(1, :) = 0; u(:, 1) = 0; u(:, end) = 0; u(end, :) = 1; 
    v(1, :) = 0; v(end, :) = 0; v(:, 1) = 0; v(:, end) = 0;
    
    % 4. Visualization (Updates every 10 steps)
    if mod(n, 10) == 0
        contourf(X, Y, sqrt(u.^2 + v.^2), 20, 'LineColor', 'none'); 
        colormap parula; hold on;
        % Quiver plot for velocity vectors (skipping points for clarity)
        quiver(X(1:2:end, 1:2:end), Y(1:2:end, 1:2:end), ...
               u(1:2:end, 1:2:end), v(1:2:end, 1:2:end), 1.5, 'w');
        title(sprintf('Lid-Driven Cavity Flow | Step %d', n));
        xlabel('X'); ylabel('Y');
        drawnow; hold off;
    end
end