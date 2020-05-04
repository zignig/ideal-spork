# ideal-spork

This is WIP

Ideal spork is a [nmigen](https://github.com/nmigen/) nmigen board builder and [Boneless](https://github.com/whitequark/Boneless-CPU/) SOC builder.

## Installation 

Clone this repository
```
> git clone https://github.com/zignig/ideal-spork.git
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
## Available boards
This is generated from [nmigen_boards](https://github.com/nmigen/nmigen-boards)
```
 Available Boards 

   0  ECP55GEVNPlatform
   1  DE0CVPlatform
   2  ICE40HX8KBEVNPlatform
   3  MercuryPlatform
   4  TinyFPGAAX1Platform
   5  ICE40HX1KBlinkEVNPlatform
   6  VersaECP5Platform
   7  DE0Platform
   8  BlackIcePlatform
   9  VersaECP55GPlatform
  10  AtlysPlatform
  11  BlackIceIIPlatform
  12  FomuHackerPlatform
  13  TinyFPGAAX2Platform
  14  ZTurnLiteZ010Platform
  15  NumatoMimasPlatform
  16  SK_XC6SLX9Platform
  17  KCU105Platform
  18  ArtyA7Platform
  19  KC705Platform
  20  TinyFPGABXPlatform
  21  MisterPlatform
  22  ICEStickPlatform
  23  DE10NanoPlatform
  24  ZTurnLiteZ007SPlatform
  25  ICEBreakerPlatform
```

All comments and patches welcome.
