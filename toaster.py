"""
***** Toaster *****
Auteur : Adrien RICQUE
Description : 
"""
from cli import pars_args
from win11toast import notify
from time import perf_counter
import subprocess
import sys
from pathlib import Path

def run_task(file_path:Path, script_args:list[str]) -> None:
    print("task started")
    command = [sys.executable, "-u", file_path, *script_args]
    subprocess.run(command, check=True)
    print("task over")

def send_notification(title:str, message:str) -> None:
    try:
        notify(title, message)
    except Exception as error:
        pass

def main() -> int:
    args = pars_args()
    started_at = perf_counter()
    try:
        run_task(args.script, args.script_args)
    except subprocess.CalledProcessError as error:
        duration = perf_counter() - started_at
        send_notification("Task Failed", f"Task lasted {duration:.2f} secondes\n Error : {sys.stderr}")
        notify("Tache Echouée", f"Task lasted {duration:.2f} secondes\n Error : {error}")
        return error.returncode
    else:
        duration = perf_counter() - started_at
        notify("Tache Réussi", f"Task lasted {duration:.2f} secondes")
        return 0



if __name__ == "__main__":
    raise SystemExit(main())
