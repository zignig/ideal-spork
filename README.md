# ideal-spork

This is WIP

Ideal spork is a [nmigen](https://github.com/nmigen/) board builder and [Boneless](https://github.com/whitequark/Boneless-CPU/) SOC builder.

## Requirements

The nmigen suite and the Boneless-CPU

* nmigen        : (https://github.com/nmigen/nmigen)
* nmigen-soc    : (https://github.com/nmigen/nmigen-soc)
* nmigen-boards : (https://github.com/nmigen/nmigen-boards)
* nmigen-stdio  : (https://github.com/nmigen/nmigen-stdio)
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

This is a developer library, if you run the following it will dump every nmigen_board available

> python -m ideal_spork --dumpall 

```
## Available boards
This is generated from [nmigen_boards](https://github.com/nmigen/nmigen-boards)
```
 Available Boards

   0  ecp5_5g_evn
   1  de0_cv
   2  ice40_hx8k_b_evn
   3  upduino_v2
   4  mercury
   5  de10_lite
   6  tinyfpga_ax1
   7  ice40_hx1k_blink_evn
   8  alchitry_au
   9  versa_ecp5
  10  de0
  11  blackice
  12  versa_ecp5_5g
  13  ice40_up5k_b_evn
  14  atlys
  15  blackice_ii
  16  fomu_hacker
  17  tinyfpga_ax2
  18  fomu_pvt
  19  arty_z7
  20  zturn_lite_z010
  21  numato_mimas
  22  upduino_v1
  23  nexys4ddr
  24  sk_xc6slx9
  25  kcu105
  26  arty_a7
  27  kc705
  28  tinyfpga_bx
  29  mister
  30  icestick
  31  de10_nano
  32  zturn_lite_z007s
  33  icebreaker
  34  zignig_dev
  35  icebreaker_unsnapped

```

All comments and patches welcome.

# TODO

- [ ] Working bootloader
- [ ] Device drivers
- [X] Auto board build
- [ ] All spork tools


