""" Basic template file that you should fill in for Problem Set 3. Some util
functions are provided from the NAND notebooks online that implement some
of the NAND essentials. """
from util import EVAL
from util import TRUTH
from util import NANDProgram
import util

# TODO: Implement this function and return a string representation of its NAND
# implementation. You don't have to use the class we supplied - you could use
# other methods of building up your NAND program from scratch.
C = 83077384819225213653292785468473349
PSET_DIM = 128
def nandmultiply():
    '''Generates a NAND program. Outputs the string representation of a NAND 
    program that takes in inputs x_0, ..., x_{127} and multiplies it with C 
    mod 2^n. The output of the NAND program should be stored in variables
    y_0, ..., y_{127}. The first digit will be the least significant
    digit (ex: 110001 --> 35). Good luck!'''
    # creates a blank NAND program with n inputs and n outputs.
    prog = NANDProgram(PSET_DIM, PSET_DIM)

    # now add lines to your NAND program by calling python functions like
    # prog.NAND() or prog.OR() or other helper functions. For an example, take
    # a look at the stuff after if __name__ == '__main__': or the nand adder
    # function that we implemented.

    # Store C as binary
    C_bin = format(C, '128b')[::-1]

    # Store C in binary as C0-C127
    for idx in range(len(C_bin)):
        if C_bin[idx] == "1":
            prog.ONE("C" + str(idx))
        else:
            prog.ZERO("C" + str(idx))

    # Store the 128 lines of multiplication. These only need to be 128 bits long due to the mod
    for row in range(128):
        for col in range(128):
            if row == 0:
                prog.AND("y_" + str(col), "C" + str(row), "x_" + str(col))
            else:
                if col >= row:
                    prog.AND("l" + str(row) + "-" + str(col), "C" + str(row),"x_" + str(col - row))
                else:
                    prog.ZERO("l" + str(row) + "-" + str(col))

    # Add the 128 lines of multiplication
    for row in range(1, 128):
        prog.ZERO("C")
        for j in range(128):
            prog.ADD_3("y_" + str(j), "C", "C", "y_" + str(j), "l" + str(row) + "-" + str(j))

    # "compiles" your completed program as a NAND program string.
    return str(prog)


# Examples of using the NANDProgram class to build NAND Programs. Please don't
# worry too much about the details of using this class - this is not a class
# about designing NAND programs.
def nandadder(N):
    '''Creates a NAND adder that takes in two n-digit binary numbers and gets
    the sum, returning a n+1-digit binary number. Returns the string repr. of
    the NAND program created.'''
    nand = NANDProgram(2 * N, N + 1)
    nand.ONE("ONE")

    carry = nand.allocate()
    nand.ADD_3(nand.output_var(0), carry,
               nand.input_var(0), nand.input_var(N), nand.NAND("ZERO", "ONE", "ONE"))

    last_carry = ""
    for i in range(1, N - 1):
        last_carry = carry
        carry = nand.allocate()
        nand.ADD_3(nand.output_var(i), carry,
                   nand.input_var(i), nand.input_var(N + i), last_carry)

    nand.ADD_3(nand.output_var(N-1), nand.output_var(N),
               nand.input_var(N-1), nand.input_var(2 * N - 1), carry)
    return str(nand)



if __name__ == '__main__':
    # Generate the string representation of a NAND prog. that adds numbers
    #addtwo = str(nandadder(2))
    #print(EVAL(addtwo, '0010'))  # 0 + 1 = 1 mod 2
    #print(EVAL(addtwo, '1010'))  # 1 + 1 = 2 mod 2

    #addfive = str(nandadder(10))
    # Input Number 1: 11110 --> 15
    # Input Number 2: 10110 --> 13   1111010110
    # Expected Output: 28 --> 001110

    #816 0000110011
    #877 1011011011
    #    10111001011
    #print(EVAL(addfive,'00001100111011011011'))

    # You should test your implementation.
    # Again, note that the binary strings have the least significant digit first 
    # Or, you can submit to gradescope and run the automatic test cases.
    prog = nandmultiply()
    for test_integer in [0, 1, 100, 123123]:
        print("Testing C * {}".format(test_integer))
        ans = (test_integer * C) % (2 ** PSET_DIM)
        print("Answer should be: {} with binary:\n{}".format(ans, util.int2bin(ans, PSET_DIM)))
        print("Program Output")
        print(EVAL(prog, util.int2bin(test_integer, PSET_DIM)))
        print("-" * 80)
