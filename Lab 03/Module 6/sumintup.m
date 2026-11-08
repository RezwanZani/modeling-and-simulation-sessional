% sumintup.m
% TOPIC: Basic for-loop to calculate the sum of integers from 1 to N.

function sumintup(N)
    % Initialize the total counter to zero
    total = 0;
    
    % Loop through numbers 1 to N
    for n = 1:N
        % Add the current number to the total
        total = total + n;
    end
    
    % Print the final total to the command window
    fprintf('total equals %d\n', total);
end
