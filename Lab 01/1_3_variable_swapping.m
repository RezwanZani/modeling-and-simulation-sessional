x = 42; 
y = 38;

% Semantic error: this copies y into x, but doesn't swap them
x = y; 
y = x; 

% Correct way to swap values using a temporary variable
x = 42; 
y = 38;
temp = x;
x = y;
y = temp;
