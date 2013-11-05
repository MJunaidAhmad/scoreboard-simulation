# Scoreboard Simulator
This is the design and implementation of the [scoreboarding algorithm](http://en.wikipedia.org/wiki/Scoreboarding#The_algorithm) for a subset of MIPS in software. The scoreboarding simulator accepts as input a text-file containing MIPS assembly and output the completed instruction status table showing the clock cycle of Issue, Read Operands, Execute Complete, and Write Result. We will utilize four distinct functional units: integer, mult, add, and div. In order to configure the system, we will use an assembly directive to define the number of each functional unit and the latency.

Here is a sample ASM file that the simulator would be able to read (see decode.py for all accepted instructions):

```
.integer 1 1  ; one int unit that operates in 1 clock 
              ; (execute complete the cycle after read operands)
.mult 2 10    ; two multiply units that take 10 clocks
.add 1 2      ; one add unit that takes 2 clocks
.div 1 40     ; one div unit that takes 40 clocks
LD    F6,  34(R2)
LD    F2,  45(R3)
MULTD F0,  F2, F4
SUBD  F8,  F6, F2
DIVD  F10, F0, F6
ADDD  F6,  F8, F2
```

The simulator contains three important files:
- __scoreboard.py__ defines the Scoreboard class and the ScoreboardParser class which are used for the scoreboarding algorithm and parsing the asm file respectively
- __fu.py__ defines a generic functional unit, which has properties for the type and number of remaining clocks
- __decode.py__ contains the Instruction class which describes an Instruction object within the scoreboard. It also provides methods for decoding an instruction string from the asm file and producing an Instruction object

Compiling and running the file is easy. It can be done with the following command

```
python scoreboard.py
```

To choose a different asm file, open up the scoreboard.py class and change the `ASM_FILE` property at the top.

NOTE: `python` in this case assumes `python3`
