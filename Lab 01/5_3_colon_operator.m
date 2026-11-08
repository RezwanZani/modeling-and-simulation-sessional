% Syntax: start:step:stop
x = 1:3:7;  % Output: 1, 4, 7
x = 1:4:8;  % Output: 1, 5
x = 1:5:10; % Output: 1, 6

% Default step is 1
ints = 1:100;
size(ints)

% Function equivalent of the colon operator
colon(1, 7)

% Odd and even numbers
odd_number = 1:2:100;
size(odd_number)

even_number = 2:2:100;
size(even_number)

% Negative steps
7:-3:1
down_by_10 = 100:-10:-100;
size(down_by_10)
