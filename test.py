'''
PROJECT BLACKBOX UNIT TESTS
All tests were performed through pytest. 
In order to run the tests open the terminal in this directory and enter the following command:

python -m pytest test.py

A few observations about the tests:
- The "controller" function is not tested as it is hard to test it by itself. However, controller is tested indirectly through the other tests.
- The "main" and "simulation_run" functions were not tested as they are part of the Terminal UI and they would be too complex to test.
'''

from simulator import Simulator

'''INSTRUCTION FUNCTION TESTS'''
'''TESTS FOR "read" INSTRUCTION FUNCTION'''

def test_read_success():
    '''Tests if function successfully reads user input into desired register'''
    #Simulates user inputing +1000 to be stored in register 0
    temp = Simulator()
    temp.console_memory = "+010000"
    temp.read("000")
    assert temp.registers[0] == "+010000"

'''TEST FOR "write" INSTRUCTION UNCTION'''

def test_write_success():
    '''Tests if function successfully writes word to screen'''
    temp = Simulator()
    temp.registers[0] = "+010000"
    temp.write("000")
    assert temp.console_memory == "+010000" #Had to specify that it's the 5 first digits as it also captures the newline character (\n)

'''TEST FOR "load" INSTRUCTION FUNCTION'''

def test_load_success():
    '''Tests if function successfully loads word from register to the accumulator'''
    temp = Simulator()
    temp.registers[0] = "+010000"
    temp.load("000")
    assert temp.accumulator == "+010000"

'''TEST FOR "store" INSTRUCTION FUNCTION'''

def test_store_success():
    '''Tests if function successfully stores word from the accumulator to a location in the registers'''
    temp = Simulator()
    temp.accumulator = "+010000"
    temp.store("000")
    assert temp.registers[0] == "+010000"

'''TESTS FOR "add" INSTRUCTION FUNCTION'''

def test_add_success():
    '''Tests if function adds successfully'''
    temp = Simulator()
    temp.registers[0] = "+001234"
    temp.accumulator = "+004321"
    temp.add("000")
    assert temp.accumulator == "+005555"

def test_add_overflow():
    '''Tests if function returns false in case add results in overflow'''
    temp = Simulator()
    temp.registers[0] = "+500000"
    temp.accumulator = "+500000"
    assert temp.add("000") == False #Tests for positive overflow
    temp.registers[0] = "-500000"
    temp.accumulator = "-500000"
    assert temp.add("000") == False #Tests for negative overflow

def test_add_zero():
    '''Tests if function stores 0 in the accumulator correctly'''
    temp = Simulator()
    temp.registers[0] = "-100000"
    temp.accumulator = "+100000"
    temp.add("000")
    assert temp.accumulator == ("+000000")

def test_add_negative():
    '''Tests if function stores negative values in the accumulator correctly'''
    temp = Simulator()
    temp.registers[0] = "-100000"
    temp.accumulator = "-100000"
    temp.add("000")
    assert temp.accumulator == "-200000"

'''TESTS FOR "subtract" INSTRUCTION FUNCTION'''

def test_subtract_success():
    '''Tests if function subtracts successfully'''
    temp = Simulator()
    temp.registers[0] = "+001234"
    temp.accumulator = "+004321"
    temp.subtract("000")
    assert temp.accumulator == "+003087"

def test_subtract_overflow():
    '''Tests if function returns false in case subtract results in overflow'''
    temp = Simulator()
    temp.registers[0] = "-500000"
    temp.accumulator = "+500000"
    assert temp.subtract("000") == False #Tests for positive overflow
    temp.registers[0] = "+500000"
    temp.accumulator = "-500000"
    assert temp.subtract("000") == False #Tests for negative overflow

def test_subtract_zero():
    '''Tests if function stores 0 in the accumulator correctly'''
    temp = Simulator()
    temp.registers[0] = "+100000"
    temp.accumulator = "+100000"
    temp.subtract("000")
    assert temp.accumulator == ("+000000")

def test_subtract_negative():
    '''Tests if function stores negative values in the accumulator correctly'''
    temp = Simulator()
    temp.registers[0] = "+100000"
    temp.accumulator = "-100000"
    temp.subtract("000")
    assert temp.accumulator == "-200000"

'''TESTS FOR "divide" INSTRUCTION FUNCTION'''

def test_divide_success():
    '''Tests if function divide successfully'''
    temp = Simulator()
    temp.registers[0] = "+000002"
    temp.accumulator = "+200000"
    temp.divide("000")
    assert temp.accumulator == "+100000"

#THE "divide" FUNCTION ACCOUNTS FOR OVERFLOWS JUST TO BE OVERLY CAUTIOUS.
#HOWEVER, IT SHOULDN'T BE POSSIBLE TO HAVE AN OVERFLOW IN A DIVISION OPERATION.

def test_divide_zero():
    '''Tests if function stores 0 in the divide correctly'''
    temp = Simulator()
    temp.registers[0] = "+000001"
    temp.accumulator = "+000000"
    temp.divide("000")
    assert temp.accumulator == ("+000000")

def test_divide_negative():
    '''Tests if function stores negative values in the divide correctly'''
    temp = Simulator()
    temp.registers[0] = "+000001"
    temp.accumulator = "-050000"
    temp.divide("000")
    assert temp.accumulator == "-050000"

'''TESTS FOR "multiply" INSTRUCTION FUNCTION'''

def test_multiply_success():
    '''Tests if function multiplies successfully'''
    temp = Simulator()
    temp.registers[0] = "+000002"
    temp.accumulator = "+200000"
    temp.multiply("000")
    assert temp.accumulator == "+400000"

def test_multiply_overflow():
    '''Tests if function returns false in case multiply results in overflow'''
    temp = Simulator()
    temp.registers[0] = "+000002"
    temp.accumulator = "+500000"
    assert temp.multiply("000") == False #Tests for positive overflow
    temp.registers[0] = "+000002"
    temp.accumulator = "-500000"
    assert temp.multiply("000") == False #Tests for negative overflow

def test_multiply_zero():
    '''Tests if function stores 0 in the accumulator correctly'''
    temp = Simulator()
    temp.registers[0] = "+100000"
    temp.accumulator = "+000000"
    temp.multiply("000")
    assert temp.accumulator == ("+000000")

def test_multiply_negative():
    '''Tests if function stores negative values in the accumulator correctly'''
    temp = Simulator()
    temp.registers[0] = "+000002"
    temp.accumulator = "-100000"
    temp.multiply("000")
    assert temp.accumulator == "-200000"

'''TEST FOR "branch" INSTRUCTION FUNCTION'''

def test_branch_success():
    '''Tests if function successfully branches to a new register address'''
    temp = Simulator()
    temp.branch("090")
    #It's one less than the desired location since once the function returns cur_addr is incremented by 1.
    assert temp.cur_addr == 89 

'''TESTS FOR "branch_neg" INSTRUCTION FUNCTION'''

def test_branch_neg_move():
    '''Tests if the function moves when accumulator is negative'''
    temp = Simulator()
    temp.accumulator = "-100000"
    temp.branch_neg("090")
    #It's one less than the desired location since once the function returns cur_addr is incremented by 1.
    assert temp.cur_addr == 89

def test_branch_neg_stay():
    '''Tests if the function does not move to another address when accumulator is not negative'''
    temp = Simulator()
    temp.accumulator = "+100000"
    temp.branch_neg("090")
    assert temp.cur_addr == 0

'''TESTS FOR "branch_zero" INSTRUCTION FUNCTION'''

def test_branch_zero_move():
    '''Tests if the function moves when accumulator is zero'''
    temp = Simulator()
    #Accumulator is zero by default
    temp.branch_zero("090")
    #It's one less than the desired location since once the function returns cur_addr is incremented by 1.
    assert temp.cur_addr == 89

def test_branch_zero_stay():
    '''Tests if the function does not move to another address when accumulator is not zero'''
    temp = Simulator()
    temp.accumulator = "+010000"
    temp.branch_zero("090")
    assert temp.cur_addr == 0

'''TEST FOR "halt" INSTRUCTION FUNCTION'''

def test_halt_success():
    '''Tests if function returns False to terminate program'''
    temp = Simulator()
    assert temp.halt() == False