x = [1 2 3; 4 5 6];

% Extract specific rows and columns
x(2, [1 3])       % 2nd row; 1st and 3rd columns
x([2 1], 2)       % 2nd and 1st rows; 2nd column
x([2,1], [2,3])   % 2nd and 1st rows; 2nd and 3rd columns
x(2, [1 2 3])     % 2nd row; columns 1, 2, and 3
x(2, 1:3)         % Same as above using colon operator
