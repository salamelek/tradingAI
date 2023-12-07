def loadingBar(currentNum, totalNum, msg="", length=30, fill='█', prefix=''):
    ratio = totalNum // length
    barProg = int(currentNum / ratio)
    bar = fill * barProg + '-' * int(length - barProg)
    print(f'\r{msg}{prefix} |{bar}| {round(((currentNum / totalNum) * 100), 1)}% Complete', end="", flush=True)
