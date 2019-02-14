import sys
from squad_lava_1_submit_check import submit_check_main


if __name__ == "__main__":
    try:
        submit_check_main(sys.argv[1])  # http://192.168.1.20:5000/api/testjobs/xx/
    finally:
        pass
