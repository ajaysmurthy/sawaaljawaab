## Table analysis and synthesis module for the HAMR 2015 ISMIR hack

import os
import essentia as es
import essentia.standard as ess
import numpy as np
import pickle
import glob

import parameters as params
import csv

rms=ess.RMS()
window = ess.Windowing(type = "hamming")
spec = ess.Spectrum(size=params.Nfft)
zz = np.zeros((params.zeropadLen,), dtype = 'float32')
genmfcc = ess.MFCC(highFrequencyBound = 7000.0, inputSize = params.Nfft/2+1, sampleRate = params.Fs)

strokeLabels = ['dha', 'dhen', 'dhi', 'dun', 'ge', 'kat', 'ke', 'na', 'ne', 're', 'tak', 'te', 'tit', 'tun']

def getFeatSequence(inputFile,pulsePos):
    audio = ess.MonoLoader(filename = inputFile, sampleRate = params.Fs)()
    frameCounter = 0
    pool = es.Pool()
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
    for stroke in strokeLabels:
        filenames = glob.glob(dataBasePath + stroke + os.sep + '*.wav')
        feats = {}
        for fpath in filenames:
            fname = os.path.split(fpath)[1].rsplit('.')[0]
            feats[fname] = getFeatSequence(inputFile = fpath, pulsePos = None)
        poolFeats[stroke] = feats
    return poolFeats


def genRandomComposition(pulsePos, dataPath = '../HAMRDataset/16k/'):
    pulsePeriod = np.median(np.diff(pulsePos))
    
    # todo
    return None

def getPulsePosFromAnn(inputFile):
    pulsePos = np.array([])
    with open(inputFile,'rt') as csvfile:
        sreader = csv.reader(csvfile)
        for row in sreader:
            pulsePos = np.append(pulsePos,float(row[0]))
    return pulsePos

def getJawaab(ipFile = '../HAMRdataset/testInputs/testInput_1.wav', ipulsePos = getPulsePosFromAnn('../HAMRdataset/testInputs/testInput_1.csv'), strokeModels = None, oFile = './tablaOutput.wav'):
    # If poolFeats are not built, give an error!
    if strokeModels == None:
        print "Train the models first. Returning a random composition"
        opulsePos = genRandomComposition(ipulsePos)
    else:
        pulsePeriod = np.median(np.diff(ipulsePos))
        
        opulsePos = ipulsePos
        print 60/pulsePeriod
        
    return oFile, opulsePos
   
def testModule(dataPath = '../HAMRDataset/16k/', inputFile = '../HAMRdataset/testInputs/testInput_1.wav', pulsePos = getPulsePosFromAnn('../HAMRdataset/testInputs/testInput_1.csv')):
    # todo
    # Train
    print "Building stroke models..."
    poolFeats = buildStrokeModels(strokeLabels, dataBasePath = dataPath)
    # Test 
    outFile = 'outTabla.wav'
    print "Generating output file..."
    outFile, opulsePos = getJawaab(ipFile = inputFile, ipulsePos = pulsePos, strokeModels = poolFeats, oFile = outFile)
    return outFile, opulsePos

if __name__ == "__main__":
    outFile, opulsePos = testModule()
    print "Stored output file to %s" %outFile
    