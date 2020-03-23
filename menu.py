import os
from sys import argv
from termcolor import colored



mandatoryArg = colored("?", "green", attrs=["bold"])

def men():
    arguments = {
        'n:': 'nom',
        'c:': 'chemin',
    }
    if len(argv) == 1 or len(argv) <= 1:
        print(colored("                            Mode d'emploi :                                \n\n", "red", attrs=['bold', 'reverse'])
        + colored(os.getcwd(), "red", attrs=["bold"])+ " [" + colored("-d", "red") + "=" + colored("\"directory\"", "yellow") +"] [" + colored("-tn", "red") + "=" + colored("\"table name\"", "yellow" ) + "] [" + colored("-cn", "red") + "=" + colored("\"column name\"", "yellow" ) + "]"  + " [" + colored("-a", "red") + "]"+ mandatoryArg +"\n\n"
        
        
        + colored("Arguments : \n\n", "green")
        + colored("  -d  / --dir", "cyan") + "         : Absolute path of file/folder " + colored("(string) \n", "blue")
        + colored("  -tn / --table_name", "cyan") + "  : Database Name " + colored("(string) \n", "blue")
        + colored("  -cn / --column_name", "cyan") + " : Column name " + colored("(string) \n", "blue")
        + colored("  -a  / --all", "cyan") + "         : All compatible files in folder " + colored("(string) \n", "blue")
        )
        exit()
    error = []
    
men()
