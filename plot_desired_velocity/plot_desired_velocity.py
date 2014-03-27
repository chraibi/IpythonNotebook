from multiprocessing import Pool, current_process
import numpy as np
import matplotlib.pyplot as plt
from sys import argv
import pandas as pd
import os, time

if len(argv)<=2:
    print "usage: %s, filename <nproc>"%argv[0]
    exit()

def plotFrame(args):
    data, i = args
    fig = plt.figure()
    for line in data:
        v0x = line[0]
        v0y = line[1]
        x = line[2]
        y = line[3]
        Gx= line[4]
        Gy= line[5]
        plt.plot((x), (y), 'og')
        plt.arrow(x, y, v0x-x, v0y-y, head_width=0.1, head_length=0.2, fc='r', ec='r')
        plt.arrow(x, y, Gx-x, Gy-y, head_width=0.1, head_length=0.2, fc='b', ec='b')
        #geometry
        plt.plot([65, 62, 62, 60, 60, 56], [104,104,103, 103, 104, 104], 'k', lw=2)
        plt.plot([65, 62, 62, 60, 60, 56], [100,100,102, 102, 100, 100], 'k', lw=2)
        plt.xlim((48,66))
        plt.ylim((99,105))
        plt.annotate('%d'%line[6], xy=(x, y), xytext=(x+0.5, y+0.5),
                    arrowprops=dict(facecolor='black', shrink=0.05),
                    )
    fig.savefig("figs_bot/%.4d.png"%i)
    plt.clf()
    print "---> figs_bot/%.4d.png"%i 


if __name__ == "__main__":
    Plot = 1
    Movie = 0
    if Plot:
        filename = argv[1]
        
        proc = argv[2]
        if not proc.isdigit():
            print "proc (\"%s\") should be a number"%proc
            exit()
        proc = int(proc)
        start = time.time() 
        print "read_csv file ..."
        data = np.array( pd.read_csv(filename, sep = " ", header=None)  )
        readTime = time.time() - start
        m = int( max(data[:,-1]) ) # 
        l = data.shape[0]
        pool = Pool(processes=proc)
        nfigs = range(0, l/m, 100)
        list_data = [ data[i*m:(i+1)*m, :] for i in nfigs ]
        inputData = zip(list_data, range(len(nfigs)))
        start = time.time()
        pool.map(plotFrame, inputData)     
        paTime = time.time() - start
        pool.close()
        pool.join()
        print "Read Data in ", readTime, "/s"
        print "Time ", paTime, "/s"
    
    if Movie:
        cmd = "\"mf://figs_bot/*.png\" -mf w=800:h=600:fps=25:type=png -ovc lavc -lavcopts vcodec=mpeg4 -oac copy -o output.avi"
        print "Mencoder ---- "
        os.system("mencoder %s" %cmd)
        MPlayer= "mplayer output.avi"
        os.system("%s" %MPlayer)

