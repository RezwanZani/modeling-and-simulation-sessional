% Create a list of sensor readings.
readings = [45 70 95 110 130 80 60];

ii = 1; % Start checking from the first reading

% FIX: Changed strictly less than (<) to less than or equal to (<=)
while ii <= length(readings) && readings(ii) <= 100
    % Replace the current reading with 0
    readings(ii) = 0;
    
    % Move to the next reading
    ii = ii + 1;
end

disp('Result after Example 1:');
disp(readings);

%% Example 2: Using BREAK statement to stop a FOR loop
% Objective:
% Check every reading and stop immediately when a value above 100 is found.
% Concept:
% FOR loop normally checks all values.

% BREAK allows us to exit the loop early when a condition is satisfied.

% Reset the original readings
readings = [45 70 95 110 130 80 60];

for ii = 1:length(readings)
    % Check if the current reading is greater than 100
    if readings(ii) > 100
    
        % Stop the loop immediately
        break;
    else
        % If reading is 100 or less, replace it with 0
        readings(ii) = 0;
    end
end

disp('Result after Example 2:');
disp(readings);


%% Example 3: Finding the position of the first reading above 100
% Objective:
% Find the index number where the first reading above 100 appears.
% Concept:
% The FOR loop stops using BREAK.

% The variable "ii" keeps the value where the loop stopped.

% Reset the original readings
readings = [45 70 95 110 130 80 60];

for ii = 1:length(readings)
    % When a value above 100 is found,
    % leave the loop immediately.
    if readings(ii) > 100
        break;
    end
end

% Display the location of the first reading above 100
fprintf('First reading above 100 is at index %d.\n', ii);