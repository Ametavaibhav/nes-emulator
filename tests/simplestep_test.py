"""
Test using the test suite from git@github.com:SingleStepTests/65x02.git.
All tests (about 10k) are available in JSON format, with initial and final cpu states.

## Test cases are not included in this repo. Clone git@github.com:SingleStepTests/65x02.git repo, and use the tests in
nes6502 directory.
"""
import json

import os

from src.cpu import CPU
from src.instructions.opcode_table import  OPCODE_TABLE


# Perform test on one instance of the test data
def test_simplestep(test_data, debug=False):
    init_state = test_data["initial"]

    init_state['memory_locs'] = init_state.pop('ram')

    cpu = CPU()
    cpu.set_cpu_state(**init_state)

    # Execute one instruction
    cpu.execute(step=True, debug=debug)

    # Get cpu state after execution
    cpu_state = cpu.get_cpu_state()

    ## Match expected vs final steps
    final_state = test_data["final"]

    ## Remove the ram locations with value 0, as cpu_state won't contain locations with value 0
    final_state['ram'] = [mem for mem in final_state['ram'] if mem[1]]

    if final_state == cpu_state:
        if debug:
            print("Test passed!")
        return True
        #print(f"{cpu_state=}, {final_state=}")
    else:
        if debug:
            print(f"Test failed! for {cpu_state=}, {final_state=}")
        return False



def test_instruction(opcode):
    """
    test a particular instruction identified by the file name containing the test cases
    """
    filepath = f"./data/65x02/nes6502/v1/{opcode}.json"

    with open(filepath, 'r') as f:
        data = json.load(f)


    counter = 0
    for test_data in data:
        if counter == 7168:
            print("Here") # to setup breakpoint
        res = test_simplestep(test_data, debug=True)
        if not res:
            break

        counter += 1
        print(counter)



def test_all_instructions():
    test_folder = "./data/65x02/nes6502/v1"

    test_results = {}

    total_tests = 0
    no_impl_counts = 0
    total_passed = 0


    continue_flag = True

    for filename in os.listdir(test_folder):
        opcode = filename.split(".")[0]


        # ### This section to skip already tried opcodes
        # if opcode== 'd0':
        #     continue_flag = False
        #
        # if continue_flag:
        #     continue

        opcode_details = OPCODE_TABLE.get(int(opcode, 16))

        if opcode_details:
            test_results[opcode] = {'name': opcode_details[0].__name__, 'address_mode': opcode_details[1].__name__,
                                 'total_tests': 0, 'total_passed': 0, 'total_failed': 0}

            print(f"Looking at {test_results[opcode]['name']}")

            with open(os.path.join(test_folder, filename), 'r') as f:
                data = json.load(f)

            total_tests_indi = 0
            total_passed_indi = 0

            for test_data in data:
                total_tests += 1
                total_tests_indi += 1

                result = test_simplestep(test_data)

                if result:
                    total_passed += 1
                    total_passed_indi += 1

            test_results[opcode]['total_tests'] = total_tests_indi
            test_results[opcode]['total_passed'] = total_passed_indi
            test_results[opcode]['total_failed'] = total_tests_indi - total_passed_indi

            # break

        else:
            print(f"No implementation present for {opcode}")
            no_impl_counts += 1


    test_results['total_tests'] = total_tests
    test_results['total_passed'] = total_passed
    test_results['total_failed'] = total_tests - total_passed
    test_results['no_implementation'] = no_impl_counts

    with open('./simplestep_results.json', 'w') as f:
        json.dump(test_results, f)



def test_failed_cases():
    filename_1 = './simplestep_results.json'
    test_folder = "./data/65x02/nes6502/v1"

    with open(filename_1, 'r') as f:
        data = json.load(f)

    failed_opcodes = []
    for opcode in data:
        if isinstance(data[opcode], dict) and data[opcode]["total_failed"] > 0:
            failed_opcodes.append(opcode)


    ## Copied from the block above
    test_results = {}

    total_tests = 0
    no_impl_counts = 0
    total_passed = 0

    continue_flag = True
    for opcode in failed_opcodes:
        opcode_details = OPCODE_TABLE.get(int(opcode, 16))

        if opcode_details:
            test_results[opcode] = {'name': opcode_details[0].__name__, 'address_mode': opcode_details[1].__name__,
                                    'total_tests': 0, 'total_passed': 0, 'total_failed': 0}

            print(f"Looking at {test_results[opcode]['name']}")

            filename = f"{opcode}.json"
            with open(os.path.join(test_folder, filename), 'r') as f:
                data = json.load(f)

            total_tests_indi = 0
            total_passed_indi = 0

            for test_data in data:
                total_tests += 1
                total_tests_indi += 1

                result = test_simplestep(test_data)

                if result:
                    total_passed += 1
                    total_passed_indi += 1

            test_results[opcode]['total_tests'] = total_tests_indi
            test_results[opcode]['total_passed'] = total_passed_indi
            test_results[opcode]['total_failed'] = total_tests_indi - total_passed_indi

            # break

        else:
            print(f"No implementation present for {opcode}")
            no_impl_counts += 1

    test_results['total_tests'] = total_tests
    test_results['total_passed'] = total_passed
    test_results['total_failed'] = total_tests - total_passed
    test_results['no_implementation'] = no_impl_counts

    with open('./simplestep_results_failed_cases.json', 'w') as f:
        json.dump(test_results, f)








def main():
    #test_instruction('40')
    #print(" -------------------------\n\n\n\n\n\n\n\n\n\n\n TEST FOR BMI inst -------------------------\n\n\n\n\n\n\n\n\n\n\n")
    # test_all_instructions()

    test_failed_cases()


if __name__ == "__main__":
    main()