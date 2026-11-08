function ultimate_question_nested2(x)
    if x <= 42
        if x == 42
            fprintf('Wow! You answered the question.\n');
        else
            fprintf('Too small. Try again.\n');
        end
    else
        fprintf('Too big. Try again.\n');
    end
end
