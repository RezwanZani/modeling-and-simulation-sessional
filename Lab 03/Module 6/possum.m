% possum.m
% TOPIC: A while-loop that counts how many integers to add before exceeding a limit.

function [n, total] = possum(limit)
    % Initialize total and step counter to zero
    total = 0;
    n = 0;
    
    % Continue looping while the total remains under or equal to the limit
    while total <= limit
        % Increment the step counter by one
        n = n + 1;
        % Add the current counter value to the running total
        total = total + n;
    end
    
    % Display the final sum and the total number of steps taken
    fprintf('sum: %d count: %d\n', total, n);
end
