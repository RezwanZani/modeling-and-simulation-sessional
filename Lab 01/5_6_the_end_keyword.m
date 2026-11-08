x = [1 2 3 4; 5 6 7 8; 9 10 11 12];

% 'end' refers to the last index of that dimension
x(end, 2)
x(2, end)
x(end, end)
x([2 end 1 end], 3)
x(1, end-1)
x(1, [end, end-1])

% Expand array by adding a new row at the end
x(end+1, 1) = 17;

% Skip elements using step sizes with 'end'
x(1, 1:2:end)
x(1, end:-1:2)

% Select entire rows or columns using just the colon (:)
x(1:end, 2)
x(:, 2) % Shorthand for "all rows, 2nd column"
x(1, :) % All columns in 1st row
x(:, :) % Entire matrix
