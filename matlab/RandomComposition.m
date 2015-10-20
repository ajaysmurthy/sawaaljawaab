clear
close all
clc
oFile = './test.wav';
dataset = './HAMRDataset/16k/';
strokes = {'dha', 'dhen', 'dhi', 'dun', 'ge', 'kat', 'ke', 'na', 'ne', 're', ...
    'tak', 'te', 'tit', 'tun'};
Ns = 150;
n = 1;
Fs = 16000;
for k = 1:length(strokes)
    files = dir([dataset strokes{k} filesep '*.wav']);
    for p = 1:length(files)
        fpath{n} = [dataset strokes{k} filesep files(p).name];
        [y, fs] = wavread(fpath{k});
        if fs ~= Fs
            error('Bad sampling')
        end
        dur(n) = length(y)/Fs;
        n = n+1;
    end
end
N = n-1;
kInd = randperm(N);
kInd = kInd(1:Ns);
% maxDur = max(dur(kInd))*Fs/2;
maxDur = 0.16*Fs;
x = [];
x = zeros(Ns*maxDur*2,1);
totDur = 0;
stIndex = 1;
for k = 1:Ns
    y = wavread(fpath{kInd(k)});
    flag = (rand > 0.9);
    if flag
        maxDurNow = maxDur*2;
    else
        maxDurNow = maxDur;    
    end
    if length(y) < maxDurNow
        y = [y; zeros(maxDurNow - length(y),1)];
    end
    totDur = totDur + length(y);
    x(stIndex:stIndex+length(y)-1) = x(stIndex:stIndex+length(y)-1) + (rand(1)+3)/4.*y;
    stIndex = stIndex + maxDurNow;
    clear y
    k
end
x = x(1:stIndex);
x = x/(max(x)+0.1);
wavwrite(x,Fs,oFile);