"""
***** TOASTER *****
Auteur : Adrien RICQUE
Description : Définition et récupération des arguments
"""
import argparse
from pathlib import Path

def pars_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description = "Exécuter un script Python et otifier sa fin"
    )
    parser.add_argument(
        "script",
        type=Path,
        help="Chemin du script python à exécuter"
    )
    parser.add_argument(
        "script_args",
        nargs="*",
        help="Arguments du script cible, à placer après --"
    )
    
    args = parser.parse_args()
    
    if not args.script.is_file():
        parser.error(f"Le chemin ne correspond pas à un fichier existant : {args.script}")
        
    return args

