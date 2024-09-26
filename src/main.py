from cpu import cpu

def test_cpu():
    a = []
    cpu = cpu.CPU()
    cpu.execute(a)


def main():
    test_cpu()

if __name__ == "__main__":
    main()

