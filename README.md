# Toaster

**Une notification Windows quand ton script Python se termine.**

Toaster lance un script Python local, mesure sa durée d’exécution et envoie une notification de réussite ou d’échec. Tu peux ainsi lancer un traitement long sans revenir vérifier le terminal régulièrement.

## Fonctionnalités

- Exécution d’un script Python depuis la ligne de commande.
- Notification Windows à la fin du script, avec sa durée en secondes.
- Distinction entre une fin normale et une sortie en erreur.
- Transmission facultative d’arguments au script exécuté.
- Affichage des sorties et des erreurs du script dans le terminal.
- Vérification de l’existence du fichier avant son lancement.

## Prérequis

- Windows 10 ou Windows 11.
- Python 3 et `pip` ; les annotations `list[str]` du projet nécessitent au minimum Python 3.9. Utiliser une version de Python encore maintenue et compatible avec les dépendances.
- La bibliothèque [win11toast](https://pypi.org/project/win11toast/) et les dépendances propres au script à lancer.
- Les notifications Windows autorisées pour l’application utilisée.

## Installation

Place `toaster.py` et `cli.py` dans le même dossier, puis ouvre PowerShell dans ce dossier.

Installe la dépendance dans l’environnement Python avec lequel tu exécuteras Toaster :

```powershell
python -m pip install win11toast
```

Si tu utilises un environnement virtuel, active-le avant cette commande. Le script cible sera lancé avec le même interpréteur que Toaster : ses propres dépendances doivent donc être installées dans cet environnement.

## Utilisation

### Lancer un script sans arguments

```powershell
python .\toaster.py .\work.py
```

Les arguments du script sont facultatifs.

### Transmettre des arguments au script

Place `--` entre le chemin du script et ses arguments :

```powershell
python .\toaster.py .\traitement.py -- --input "mes donnees.csv" --verbose
```

Dans cet exemple, `traitement.py` doit accepter les options `--input` et `--verbose`. Le séparateur `--` est consommé par Toaster ; les éléments qui le suivent sont transmis au script. Les guillemets permettent de conserver une valeur contenant des espaces comme un seul argument.

### Utiliser un chemin contenant des espaces

```powershell
python .\toaster.py "C:\Mes scripts\traitement.py"
```

### Afficher l’aide

```powershell
python .\toaster.py --help
```

## Fonctionnement

1. `cli.py` lit les arguments et vérifie que le chemin désigne un fichier existant.
2. `toaster.py` démarre le chronométrage avec `perf_counter()`.
3. Le script est lancé via `subprocess.run(..., check=True)` avec le même interpréteur Python que Toaster.
4. Toaster attend la fin du processus, calcule la durée écoulée et envoie la notification correspondante.

Le script est lancé avec l’option Python `-u`, qui désactive la mise en tampon des sorties standard et d’erreur de Python. Ses messages restent visibles dans le terminal. Toaster attend la fin du script : le terminal utilisé reste occupé pendant son exécution.

La réussite est déterminée par le code de sortie du processus. Si un script traite lui-même une erreur puis se termine avec le code `0`, Toaster le considère comme réussi.

## Codes de sortie

Le point d’entrée doit transmettre le résultat de `main()` au système :

```python
if __name__ == "__main__":
    raise SystemExit(main())
```

`main()` retourne `0` en cas de réussite et `error.returncode` lorsqu’une `subprocess.CalledProcessError` est interceptée.

| Situation | Code de sortie |
| --- | --- |
| Le script se termine normalement | `0` |
| Le script se termine avec un code non nul | Code renvoyé par le script |
| Toaster rejette les arguments ou un chemin invalide via `parser.error()` | `2` |

Le code `2` peut aussi provenir du script cible : il faut consulter le message du terminal pour connaître son origine.

Pour consulter le code de sortie dans PowerShell, immédiatement après l’exécution :

```powershell
python .\toaster.py .\work.py
$LASTEXITCODE
```

Ces retours supposent que l’envoi de la notification ne lève pas d’exception non interceptée. Si `notify()` est appelé directement, une erreur d’envoi peut empêcher le retour du code prévu.

## Structure du projet

| Fichier | Rôle |
| --- | --- |
| `toaster.py` | Point d’entrée, lancement du script, chronométrage et notifications |
| `cli.py` | Définition, lecture et validation des arguments |
| `work.py` | Script utilisé pour les essais ; remplaçable par ton propre script |
| `README.md` | Documentation du projet |

## Test manuel

Un exemple de `work.py` pour vérifier le fonctionnement :

```python
from time import sleep


def run_task() -> None:
    print("Début du traitement")
    sleep(2)
    print("Fin du traitement")


if __name__ == "__main__":
    run_task()
```

Lance-le avec Toaster : une notification de réussite doit être demandée après environ deux secondes, plus le temps de démarrage de Python.

Pour tester l’échec, remplace `print("Fin du traitement")` par `raise SystemExit(7)`, puis relance la commande. La notification doit signaler un échec et `$LASTEXITCODE` doit valoir `7`, sous réserve que l’envoi de notification fonctionne.

## Points à connaître

- **Dossier de travail :** Toaster ne change pas automatiquement de dossier pour lancer le script. Un chemin relatif utilisé pour ouvrir un fichier est donc interprété depuis le dossier de lancement, sauf si le script le gère lui-même.
- **Détail des erreurs :** la notification résume l’échec du processus. La trace complète d’une exception du script reste dans le terminal.
- **Exécution du script :** définir une fonction ne l’exécute pas. Le fichier cible doit appeler son traitement, par exemple avec le bloc `if __name__ == "__main__":`.

## Documentation des dépendances

- [win11toast — notifications Windows](https://pypi.org/project/win11toast/)
- [Python — subprocess](https://docs.python.org/3/library/subprocess.html)
- [Python — argparse](https://docs.python.org/3/library/argparse.html)


