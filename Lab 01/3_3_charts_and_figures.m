x_coordinates = [1, 3, 10];
y_coordinates = [4, -2, 12.3];

% Create a bar chart
bar(x_coordinates, y_coordinates);

% Open a new blank figure window
figure 

% Create a pie chart (spaces or commas work)
pie([4 2 7 4 7])

% Open another figure window and create another pie chart
figure
pie([4, 2, 7, 4, 7])

% Close specific figures by their number
close(1)
close(3)
