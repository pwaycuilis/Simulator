full version simulator that tracks cycle-by-cycle process (instruction-by-instruction version available in disassembler repository)

cycle-by-cycle ARM instruction simulator

loads and executes binary ARM file. Produces disassembled program code and produces cycle-by-cycle simulation showing the processor state at each cycle. 
The processor state includes the contents of registers, buffers, cache, and data memory at each cycle.

Quick Start --  
(linux command line )
Clone the repo : 
$git clone https://pwaycuilis/Simulator

$cd Simulator

$python3 team23_project3.py -i branchtest_bin.txt -o team23_out

Then display output printed to text files)
(for cycle-by-cycle pipeline output)
$cat team23_out_pipeline.txt

For disassembler output: (list of assembly instructions translated from binary ARM input file)

$cat team23_out_dis.txt

NOTE: can change input or output file name using -i or -o argument respectively


