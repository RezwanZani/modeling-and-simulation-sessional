%{
Array Operations and Operator Precedence
Question a: Given the row vectors X = [1, 5, -2] and Y = [1, 2, 3]
What is the result of the element-wise multiplication Z = X .* Y?
Why does matrix multiplication Z = X * Y cause an error?
Question b: According to MATLAB's operator precedence rules, determine the output of 1:3+10 and explain whether addition or the colon operator is executed first.
%}

X = [1, 5, -2];
Y = [1, 2, 3];

Z = X .* Y;

disp("Answer: " + Z)

a = 1:3+10;


%% Plotting Discrete Data Points
%{
Problem: Define two vectors for x and y coordinates:
x_coordinates = [1, 3, 10];
y_coordinates = [4, -2, 12.3];
Task:
Write a command to plot these points using red square markers and no connecting lines.
Add a grid to the plot, label the x-axis as 'Selection', label the y-axis as 'Change', and give the plot the title 'Changes in selections during the past years'.
%}

disp('Starting Problem 2');

x_coordinates = [1, 3, 10];
y_coordinates = [4, -2, 12.3];

plot(y_coordinates, y_coordinates, 'rs');
grid on;
axis square;
axis([0 12 -10 20])

title('Changes in selections during the past years');
xlabel('Selection');
ylabel('Change');


%% 3D Curve Plotting
%{
Problem: You want to plot a 3D helix.
Task:
Define a parameter t ranging from 0 to 10*pi with a step size of pi/50.
Write the command using plot3 to create a 3D plot where $x = \sin(t)$, $y = \cos(t)$, and $z = t$.
%}

disp('Starting Problem 3')
t = 0:pi/50:10*pi;
x = sin(t);
y= cos(t);
z = t;

plot3(x, y, z,'g');
grid on;


%% Bar Chart and Pie Chart
%{
Bar Charts and Pie Charts
Problem:
Task 4a: Write the command to display the x_coordinates and y_coordinates vectors as a bar chart instead of a line plot.
Task 4b: Write the command to plot a pie chart for the vector [4, 2, 7, 4, 7].
%}

disp('Starting Problem 4')

bar(x_coordinates, y_coordinates);

pie([4, 2, 7, 4, 7])