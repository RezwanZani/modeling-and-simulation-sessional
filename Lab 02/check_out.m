% The \n character creates a new line after the text
fprintf('This is MATLAB lecture\n')

% Call the function so it actually runs
check_it_out(5, 12.00);

% Printing every element of a vector automatically
fprintf('%4.1f\n', [1 2 3 4 5 6]);

% --- ALL FUNCTIONS MUST GO AT THE VERY BOTTOM ---
function check_it_out(n, price)
    total = n * price;
    fprintf('%d items at %.2f each\nTotal = $ %5.2f\n', n, price, total);
end