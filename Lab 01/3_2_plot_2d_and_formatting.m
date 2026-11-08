x_coordinates = [1, 3, 10];
y_coordinates = [4, -2, 12.3];

% Basic 2D plot
plot(x_coordinates, y_coordinates);

% Check how many elements are in the vector
length(x_coordinates)

% Plot with just asterisk markers
plot(x_coordinates, y_coordinates, '*');

% Plot with LineSpec: 's' for square marker, 'r' for red line
plot(x_coordinates, y_coordinates, 'sr');

% Formatting the plot
grid on
xlabel('selection')
ylabel('change')
title('Changes in selections during the past years')

% Set manual axis limits: [xmin, xmax, ymin, ymax]
axis([0, 12, -10, 20])
