clear
close all
clc
% Organize dataset and resample
dbpath = './HAMRDataset/';
strokes = {'dha', 'dhen', 'dhi', 'dun', 'ge', 'kat', 'ke', 'na', 'ne', 're', ...
    'tak', 'te', 'tit', 'tun'};
for k = 1:length(strokes)
    files = dir([dbpath '44k/' strokes{k} filesep '*.wav']);
    for p = 1:length(files)
        [y Fs] = wavread([dbpath '44k/' strokes{k} filesep files(p).name]);
        x = resample(mean(y,2),16000,44100);
        if ~isdir([dbpath '16k/' strokes{k}])
            mkdir([dbpath '16k/' strokes{k}]);
        end
        x = x./(max(x)+0.1);
        if max(x) >= 0.9
            stop = 1;
            max(x)
        end
        wavwrite(x, 16000, [dbpath '16k/' strokes{k} filesep strokes{k} '_' sprintf('%.2d', p) '.wav']);
        p
    end
    k
end