import os
import struct
import matplotlib.pyplot as plt
import numpy as np
os.chdir(os.path.dirname(__file__))
"""
MSTAR LOADER for raw img
mag and phase both, no quantification
shape [2 , w, h].  0 for mag, 1 for phase
"""

def load_parm(header, string):
    start = header.find(string) + len(string)
    end = header.find(b'\n', start)
    parm = int(header[start:end])
    return parm

def read(file):
    with open(file, 'rb') as f:
        header = f.read(512)
        head = load_parm(header, b'PhoenixHeaderLength= ')
        # print(head)

        w = load_parm(header, b'NumberOfColumns= ')
        h = load_parm(header, b'NumberOfRows= ')
        # print(w, h)
        f.seek(0, 0)
        f.read(head)

        data = struct.unpack_from('>'+str(w*h*2)+'f', f.read(), 0)
        # print(data)
        data = np.reshape(np.array(data), (2, w, h))
        return data


state = r'mstar2raw.exe '
ind = ' 0'

#IMAGE FOLDER
folder = r'D:\MSTAR\MSTAR_PUBLIC_MIXED_TARGETS_CD2\17_DEG\COL2\SCENE1\ZSU_23_4'
#SAVE FOLDER
save_folder = r'train\ZSU_23_4'
if os.path.exists(save_folder):
    raise FileExistsError("YOU KNOW WHY, IDIOT")
os.makedirs(save_folder, exist_ok=True)
files = os.listdir(folder)
i = 0
for filename in files:
    # POSTFIX
    if '.026' in filename:
        i += 1
        file = os.path.join(folder, filename)
        data = read(file)
        np.save(os.path.join(save_folder, filename.replace('.', '_')), data)
        print(filename)
# TOTAL NUMBER
print(i)
        # break

