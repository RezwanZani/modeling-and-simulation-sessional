% Create x and y values for sine and cosine
x1 = 0:0.1:2*pi;
y1 = sin(x1);
x2 = pi/2:0.1:3*pi;
y2 = cos(x2);

% Plot sine and cosine on the same graph without styles
plot(x1,y1,x2,y2)

% Plot with line colors and styles ('r' = red, 'k:' = black dotted line)
plot(x1,y1,'r',x2,y2,'k:')

% Plot with markers ('m--o' = magenta dashed line with circle markers)
plot(t,b,'m--o')