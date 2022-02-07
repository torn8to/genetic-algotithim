import sys

def pick_algo():


if __name__ =='__main__':
    if len(sys.argv) == 3:
        pick_algo(sys.argv[1])
        file = open(sys.argv[2],'r')
        max_run_time = sys.argv[3]

    else:
        print('wrong number of arguments')