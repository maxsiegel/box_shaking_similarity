function score = pairwise_compare_stats(sound1, sound2, fname)
    addpath("Sound_Texture_Synthesis_Toolbox")
    % try
    stats1 = get_texture_stats(sound1);
    stats2 = get_texture_stats(sound2);

        % dbstop if error
        to_compare = {'env_mean',
                      'env_var',
                      'env_skew',
                      'env_C',
                      'mod_power'};

    score = 0;

    for i = 1:length(to_compare)

        val1 = getfield(stats1, to_compare{i});
        val2 = getfield(stats2, to_compare{i});

        c = corrcoef(val1, val2);
        score = score + c(2);
        % modulation power is much bigger than others, normalize it somehow
    end

    if ~exist('stats')
        mkdir('stats')
    end
    f = fopen(fname, 'w');
    fprintf(f, '%f', score);
    fclose(f);

    [~, name1, ~] = fileparts(sound1);
    [~, name2, ~] = fileparts(sound1);
    save(strcat('stats/', name1), 'stats1');
    save(strcat('stats/', name2), 'stats2');
    exit;
    % catch exception
    % display(['error in ', fname])
    % exit;
    % end
end
