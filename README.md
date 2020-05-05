# ideal-spork

This is WIP

Ideal spork is a [nmigen](https://github.com/nmigen/) board builder and [Boneless](https://github.com/whitequark/Boneless-CPU/) SOC builder.

## Requirements

The nmigen suite and the Boneless-CPU

* nmigen        : (https://github.com/m-labs/nmigen)
* nmigen-soc    : (https://github.com/m-labs/nmigen-soc)
* nmigen-boards : (https://github.com/m-labs/nmigen-boards)
* nmigen-stdio  : (https://github.com/m-labs/nmigen-stdio)
* Boneless-CPU  : (https://github.com/whitequark/Boneless-CPU)

FPGA development programs

Current development is on a [TinyFPGABx](https://tinyfpga.com/) this uses the following software

* yoysys   : (https://github.com/YosysHQ/yosys)
* nextpnr  : (https://github.com/YosysHQ/nextpnr)
* icestorm : (https://github.com/cliffordwolf/icestorm) 

With this software installed ideal_spork provides some board tooling

## Installation 

Clone this repository
```
> git clone https://github.com/zignig/ideal-spork.git
> cd ideal-spork
> python setup.py develop --user
```

This will install the library and create a program called spork.

bash> spork

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
   0  ECP55GEVNPlatform
   1  DE0CVPlatform
   2  ICE40HX8KBEVNPlatform
   3  UpduinoV2Platform
   4  MercuryPlatform
   5  DE10LitePlatform
   6  TinyFPGAAX1Platform
   7  ICE40HX1KBlinkEVNPlatform
   8  AlchitryAuPlatform
   9  VersaECP5Platform
  10  DE0Platform
  11  BlackIcePlatform
  12  VersaECP55GPlatform
  13  ICE40UP5KBEVNPlatform
  14  AtlysPlatform
  15  BlackIceIIPlatform
  16  FomuHackerPlatform
  17  TinyFPGAAX2Platform
  18  FomuPVTPlatform
  19  ArtyZ720Platform
  20  ZTurnLiteZ010Platform
  21  NumatoMimasPlatform
  22  UpduinoV1Platform
  23  Nexys4DDRPlatform
  24  SK_XC6SLX9Platform
  25  KCU105Platform
  26  ArtyA7Platform
  27  KC705Platform
  28  TinyFPGABXPlatform
  29  MisterPlatform
  30  ICEStickPlatform
  31  DE10NanoPlatform
  32  ZTurnLiteZ007SPlatform
  33  ICEBreakerPlatform

```

All comments and patches welcome.

# TODO

- [ ] Galactic Domination
- [ ] Working bootloader
- [ ] Device drivers
- [ ] Auto board build
- [ ] All spork tools


