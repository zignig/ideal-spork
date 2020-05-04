# ideal-spork

This is WIP

Ideal spork is a [nmigen](https://github.com/nmigen/) nmigen board builder and [Boneless](https://github.com/whitequark/Boneless-CPU/) SOC builder.

## Installation 

Clone this repository
```
> git clone (https://github.com/zignig/ideal-spork.git)
> cd ideal-spork
> python setup.py develop --user
```

This will install the library and create a program called spork.

```
No spork file
usage: spork [-h] [-v] [-d DIRECTORY]
             {init,info,console,build,status,list,burn,program,gatesim} ...

spork is a nmigen board build helper

positional arguments:
  {init,info,console,build,status,list,burn,program,gatesim}
    init                Create files for a new board
    info                Get information from the base board
    console             Attach to a new console
    build               Build gateware and program onto the board
    status              Get the status of the current spork
    list                List available boards
    burn                Add the given firmware to boot image
    program             Upload the given firmware onto the board
    gatesim             Run a gate simulation of the board

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Logging Level
  -d DIRECTORY, --directory DIRECTORY
                        Directory for spork file

ideal_spork is a nmigen_board builder spork init will create all the files for
a platform build
```

All comments and patches welcome.

