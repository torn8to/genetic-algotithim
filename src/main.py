import sys
from Gal import Gal
from GalHelper import FileHelper
from tower_stacking import tower_stacker_genetics
from datetime import datetime
def pick_algo():
    pass


if __name__ =='__main__':

    if len(sys.argv) == 4:
        if float(sys.argv[1]) == 1:
            list_input = FileHelper.read_file(sys.argv[2])
            max_run_time = sys.argv[3]
            gal = Gal(list_input,20,float(max_run_time))
            gal.iterator("Combo")
        if float(sys.argv[1]) == 2:
            # file = open(sys.argv[2],'r')
            file = open(sys.argv[2], 'r')
            t = tower_stacker_genetics(file)
            t.run_for_n_time(max_run_time)
            t.export_csv()
    else:
        print('wrong number of arguments')
