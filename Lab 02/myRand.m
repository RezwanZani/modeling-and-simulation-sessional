function [a, s] = myRand(low, high)
    a = low + rand(3,4)*(high-low);
    s = sumAllElements(a);
end

function suma = sumAllElements(M)
    % Declaring 'v' as a global variable to share its scope with the command window
    % (Note: The lecture advises against using global variables to avoid hard-to-trace bugs)
    global v;
    v = M(:);
    suma = sum(v);
