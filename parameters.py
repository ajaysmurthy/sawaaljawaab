# A file with parameters for tabla stroke analysis
import numpy as np
import math
# Frame parameters first
Fs = 16000.0
hop = int(np.round(10.0e-3*Fs))
frmSize = int(np.round(20.0e-3*Fs))
Nfft = int(np.power(2, np.ceil(np.log2(frmSize))))
zeropadLen = Nfft - frmSize
