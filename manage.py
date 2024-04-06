#!/bin/python3
import sys, importlib


def main(args):
    try:
        func = args[1]
    except IndexError:
        print(f"No argument passed, try '{args[0]} help'")
        return

    
    module_name = "apps." + func

    module = importlib.import_module(module_name)
    
    module.run(args)

if __name__=="__main__":
    main(sys.argv)
