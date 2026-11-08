% Animated 3D Black Hole Simulation
clear; clc; close all;

% Setup dark figure
fig = figure('Color', 'k', 'Name', 'Black Hole', 'MenuBar', 'none');
set(gca, 'Color', 'k', 'XColor', 'none', 'YColor', 'none', 'ZColor', 'none');
hold on; axis equal; axis vis3d; % Fixed line

% 1. Event Horizon (The Black Sphere)
[X, Y, Z] = sphere(60);
r_eh = 1; % Schwarzschild radius
surf(r_eh*X, r_eh*Y, r_eh*Z, 'FaceColor', 'k', 'EdgeColor', 'none', 'FaceLighting', 'none');

% 2. Photon Ring (Faint glowing aura)
r_pr = 1.4;
surf(r_pr*X, r_pr*Y, r_pr*Z, 'FaceColor', [1 0.6 0.1], 'EdgeColor', 'none', 'FaceAlpha', 0.15);

% 3. Accretion Disk (Plasma)
theta = linspace(0, 2*pi, 120);
r = linspace(1.5, 6, 60);
[THETA, R] = meshgrid(theta, r);
Xd = R .* cos(THETA);
Yd = R .* sin(THETA);
% Color intensity (hotter closer to the event horizon)
Intensity = 1 ./ (R.^1.5);

% Plot the disk
hDisk = surf(Xd, Yd, zeros(size(Xd)), Intensity, 'EdgeColor', 'none', 'FaceAlpha', 0.85);
colormap(hot); % Fire colors
clim([0, max(Intensity(:))*0.6]); 

% Camera setup
campos([12 12 4]);
camtarget([0 0 0]);
camva(35); % Zoom

disp('Close the figure window to stop the animation.');

% Animation Loop: Rotate camera and warp the accretion disk
t = 0;
while isgraphics(fig)
    t = t + 0.1;
    
    % Simulate relativistic plasma turbulence by warping the Z-axis of the disk
    Zd = 0.3 * sin(4*THETA - t) .* exp(-0.4*R);
    hDisk.ZData = Zd;
    
    % Rotate the camera slowly
    camorbit(0.5, 0.1, 'camera'); 
    
    drawnow;
    pause(0.015);
end