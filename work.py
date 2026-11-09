from time import sleep
import sys

def run_task() -> None:
    print("task work.py launched")
    print("Arguments reçus :", sys.argv[1:])
    #sleep(2)
    #raise RuntimeError("Impossible de joindre le serveur")
    #raise SystemExit(7)
    
if __name__ == "__main__":
    run_task()