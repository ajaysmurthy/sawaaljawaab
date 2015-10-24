## Table analysis and synthesis module for the HAMR 2015 ISMIR hack

import os
import essentia as es
import essentia.standard as ess
import numpy as np
import pickle
import glob
import utilFunctions as UF
import scipy.spatial.distance as DS

import parameters as params
import csv

rms=ess.RMS()
window = ess.Windowing(type = "hamming")
spec = ess.Spectrum(size=params.Nfft)
zz = np.zeros((params.zeropadLen,), dtype = 'float32')
genmfcc = ess.MFCC(highFrequencyBound = 22000.0, inputSize = params.Nfft/2+1, sampleRate = params.Fs)

strokeLabels = ['dha', 'dhen', 'dhi', 'dun', 'ge', 'kat', 'ke', 'na', 'ne', 're', 'tak', 'te', 'tit', 'tun']
dataPath = '../dataset/44k/'

def getFeatSequence(inputFile,pulsePos):
    if type(inputFile) == str:
        audio = ess.MonoLoader(filename = inputFile, sampleRate = params.Fs)()
    else:
        audio = inputFile           # Assuming mono 
    frameCounter = 0
    pool = es.Pool()
    pool.add('samples',audio)
    for frame in ess.FrameGenerator(audio, frameSize = params.frmSize, hopSize = params.hop):
        ts = params.hop/params.Fs*frameCounter + params.frmSize/float(2*params.Fs)
        zpFrame = np.hstack((frame,zz))
        mag = spec(window(zpFrame))
        mfccBands,mfccSeq = genmfcc(mag)
        pool.add('rms',rms(mag))
        pool.add('mfcc',mfccSeq)
        pool.add('time',ts)
        frameCounter += 1
    if pulsePos != None:
        pulsePos = np.append(pulsePos,len(audio)/params.Fs)
        for tp in xrange(len(pulsePos)-1):
            pool.add('pst', pulsePos[tp])
            pool.add('pet', pulsePos[tp+1])
            temp1 = np.where(pool['time'] >= pulsePos[tp])[0]
            temp2 = np.where(pool['time'] < pulsePos[tp+1])[0]
            binIndices = np.intersect1d(temp1, temp2)
            pool.add('pmfcc', np.mean(pool['mfcc'][binIndices,:], axis = 0))
            pool.add('prms', np.mean(pool['rms'][binIndices]))
    else:
        pool.add('pst', 0.0)
        pool.add('pet', len(audio)/params.Fs)
        pool.add('pmfcc', np.mean(pool['mfcc'], axis = 0))
        pool.add('prms', np.mean(pool['rms'], axis = 0))
    return pool

def buildStrokeModels(strokeLabels, dataBasePath):
    poolFeats = {}
    poolFeats = []
    print "Building stroke models..."
    for stroke in strokeLabels:
        print stroke
        filenames = glob.glob(dataBasePath + stroke + os.sep + '*.wav')
        for fpath in filenames:
            fname = os.path.split(fpath)[1].rsplit('.')[0]
            feat = {'strokeId': [stroke + os.sep + fname], 'feat': getFeatSequence(inputFile = fpath, pulsePos = None)}
            poolFeats.append(feat) 
    return poolFeats
def getPulsePosFromAnn(inputFile):
    pulsePos = np.array([])
    with open(inputFile,'rt') as csvfile:
        sreader = csv.reader(csvfile)
        for row in sreader:
            pulsePos = np.append(pulsePos,float(row[0]))
    return pulsePos

def InitSystem():
    poolFeats = buildStrokeModels(strokeLabels, dataPath)
    
strokeModelsG = buildStrokeModels(strokeLabels, dataPath)

def genAudioFromStrokeSeq(strokeModels,strokeSeq,timeStamps):
    # Generates a numpy array sequence of values from fnames at the given times
    tail = np.max(np.diff(timeStamps))
    audio = np.zeros(int(np.round((timeStamps[-1] + tail)*params.Fs)))
    print len(audio)
    tsSamp = np.round(timeStamps*params.Fs)
    print tsSamp
    for k in range(len(strokeSeq)):
        strokeAudio = strokeModels[int(strokeSeq[k])]['feat']['samples'][0]        
        lenAudio = len(strokeAudio)
        print tsSamp[k], lenAudio
        audio[tsSamp[k]:tsSamp[k]+lenAudio] = audio[tsSamp[k]:tsSamp[k]+lenAudio] + strokeAudio
    # The last sample
    return audio[:tsSamp[-1]+lenAudio]

def getInvCovarianceMatrix(poolFeats):
    dataMat = np.zeros((len(params.selectInd),len(poolFeats)))
    # dataMat = np.array([])
    for k in range(len(poolFeats)):
        dataMat[:,k] = np.array(poolFeats[k]['feat']['pmfcc'][0][params.selectInd])
    invC = np.linalg.inv(np.cov(dataMat))
    return invC

invCmat = getInvCovarianceMatrix(strokeModelsG)

def genSimilarComposition(pulsePeriod, pieceDur, iAudio, strokeModels = strokeModelsG, invC = None):
    if strokeModels == None:
        strokeSeq = None
        strokeTime = None 
        opulsePos = None
    else:
        iPos = np.arange(0.0,pieceDur,pulsePeriod)
        testFeatFull = getFeatSequence(iAudio,iPos)
        testFeat = testFeatFull['pmfcc']
        print testFeat.shape
        Npulse = testFeat.shape[0]
        Ndata = len(strokeModels)
        strokeSeq = []
        strokeTime = np.array([])
        strokeAmp = np.array([])
        tscurr = 0.0
        opulsePos = np.arange(0,pieceDur,pulsePeriod)
        for k in range(Npulse):
            ftIn = testFeat[k,params.selectInd]
            distVal = 1e6*np.ones(Ndata)
            strokeTime = np.append(strokeTime,tscurr)
            strokeAmp = np.append(strokeAmp, np.random.rand())
            tscurr = tscurr + pulsePeriod
            for p in range(Ndata):
                ftOut = strokeModels[p]['feat']['pmfcc'][0][params.selectInd]
                distVal[p] = DS.mahalanobis(ftIn,ftOut,invC)
            strokeSeq.append(strokeModels[np.argmin(distVal)]['strokeId'][0])
    return strokeSeq, strokeTime, strokeAmp, np.median(np.diff(opulsePos))

def getJawaabLive(ipAudio, ipulsePer, strokeModels = strokeModelsG):
    # If poolFeats are not built, give an error!
    if strokeModels == None:
        print "Train models first before calling getJawaab() ..."
        strokeModels = InitSystem()
    else:
        print "Getting jawaab..."
        pulsePeriod = ipulsePer
        print pulsePeriod
        audioIn = ipAudio
        fss = params.Fs
        strokeSeq, strokeTime, strokeAmp, opulsePer = genSimilarComposition(pulsePeriod, pieceDur = len(audioIn)/params.Fs, iAudio = audioIn, strokeModels = strokeModels, invC = invCmat)
    return strokeSeq, strokeTime, strokeAmp, opulsePer

def testModuleLive(inputFile = '../dataset/testInputs/testInput_3.wav', pulsePos = getPulsePosFromAnn('../dataset/testInputs/testInput_3.csv')):    
    ipulsePer = np.median(np.diff(pulsePos))
    print ipulsePer
    fss, ipAudio = UF.wavread(inputFile)
    print "Analysing input..."
    strokeSeq, strokeTime, strokeAmp, opulsePer = getJawaabLive(ipAudio, ipulsePer)
    return strokeSeq, strokeTime, strokeAmp, opulsePer
    
if __name__ == "__main__":
    print "Testing..."
    testModuleLive()
    # print "Stored output file to %s" %outFile
    