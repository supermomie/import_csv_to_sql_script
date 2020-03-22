import os
from sys import argv
from termcolor import colored

def men():
    arguments = {
        'n:': 'nom',
        'c:': 'chemin',
    }
    print("a")
    if len(argv) == 1 or len(argv) <= 1:
        print(colored("                            Mode d'emploi :                                \n\n", "red", attrs=['bold', 'reverse'])
        + colored(os.getcwd()+" nom", "red", attrs=["bold"]) , colored("\"regex\" [-d=\"directory\"]  [-f=\"files\"]? [-a]? \n\n", "yellow")
        + " [\e[1;31m-c\e[0m=\e[0;33mchemin\e[0m]"
        + "\e[0;32mArguments : \n\n"
        + "  \e[0;36m-n / --nom : \e[0;37mNom de la base de donnee\e[0m(\e[1;34mstring\e[0m)\n"
        + "  \e[0;36m-c / --chemin : \e[0;37mChemin absolu a la racine de la base de donnee\e[0m(\e[1;34mstring\e[0m)\n")
        exit()
    error = []
    
men()
