import os
from sys import argv
from termcolor import colored
from cmdarg import CmdArg


class Menu():
    
    #def __init__(self):
        #arg == self.men(arg)

    def men(self, arg):
        if len(argv) == 1 or len(argv) <= 1:
            mandatoryArg = colored("?", "green", attrs=["bold"])
            print(colored("                            Mode d'emploi :                                \n\n", "red", attrs=['bold', 'reverse'])
            + colored(os.getcwd(), "red", attrs=["bold"])+ 
            " [" + colored("-db", "red") + "=" + colored("\"database server\"", "yellow") +"]"+ 
            " [" + colored("-d", "red") + "=" + colored("\"directory\"", "yellow") +"]"+ 
            " [" + colored("-tn", "red") + "=" + colored("\"table name\"", "yellow" ) + "]"+
            " [" + colored("-cn", "red") + "=" + colored("\"column name\"", "yellow" ) + "]"+ 
            " [" + colored("-a", "red") + "]"+ mandatoryArg +"\n\n"

            + colored("Arguments : \n\n", "green")
            
            + colored("  -db  / --database", "cyan") + "   : Choice [mysql or mongodb] " + colored("(string) \n", "blue")
            + colored("  -d  / --dir", "cyan") + "         : Absolute path of file/folder " + colored("(string) \n", "blue")
            + colored("  -tn / --table_name", "cyan") + "  : Database Name " + colored("(string) \n", "blue")
            + colored("  -cn / --column_name", "cyan") + " : Column name " + colored("(string) \n", "blue")
            + colored("  -a  / --all", "cyan") + "         : All compatible files in folder " + colored("(string) \n", "blue")
            )
            exit()
        error = []
        cmdarg = CmdArg(argv, arg)
        args = cmdarg.check(error)
        if len(error) > 0:
            for e in error:
                print(colored("The argument " +e+" is incorect", "red"))
            exit()
        return args
