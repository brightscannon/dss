
num = 1234

def disp1(s):
    print("disp1:",s)
def disp2(s):
    print("disp2:",s)
def disp3(s):
    print("disp3:",s)
class Calc:
    def plus(self, *args):
        return sum(args)