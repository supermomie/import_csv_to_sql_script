import os
from sys import argv
from termcolor import colored
from cmdarg import CmdArg


class menu():
    
    def __init__(self, arg):
        arg == self.men(arg)

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
        print("args", args)
        print("error ", error)
        print(error)
        if len(error) != 0 and error:
            print("cc")
            if args[0] == -2:
                print(colored("The argument " +error+" is incorect", "red"))
                exit()
            elif args == -1:
                return -3
            return args

arg = ["d", 't', 'c', 'a']
m = menu(arg)
ar = m.men(arg)
