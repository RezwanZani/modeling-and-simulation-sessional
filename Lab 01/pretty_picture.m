function pretty_picture(N)
%PRETTY_PICTURE Plot a growing cosine wave versus a growing sine
% PRETTY_PICTURE(N) plots with N points. 
% PRETTY_PICTURE without input uses N = 500.
% Created 1985 by Cleve Moler and Jack Little

% If no input provided, use default N = 500
if nargin < 1
    N = 500;
end

% Generate parameter
t = 0:(.99*pi/2):N;

% Compute coordinates
x = t .* cos(t);
y = t .* sin(t);

% Plot the curve
plot(x, y, 'k')
axis square
title(sprintf('Pretty Picture with N = %d', N))
xlabel('x = t cos(t)')
ylabel('y = t sin(t)')
end
