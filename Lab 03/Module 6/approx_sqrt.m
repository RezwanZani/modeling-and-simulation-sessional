% approx_sqrt.m
% TOPIC: Using a while-loop and Newton's method to approximate a square root.

function y = approx_sqrt(x)
    % Set the initial guess equal to the given input
    y = x;
    
    % Keep improving the guess while the error exceeds the allowed tolerance
    while abs(y^2 - x) > 1e-7 * x
        % Apply Newton's method formula to calculate the next guess
        y = (x / y + y) / 2;
    end
end
