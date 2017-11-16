class Car:
    def __init__(self):
        self.name = ""


    def getName(self):
        return self.name


    def setName(self, name):
        self.name = name

if __name__ == "__main__":

    a = Car()
    a.setName('van')
    print(a.getName())
