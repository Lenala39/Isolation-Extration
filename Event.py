class Event():

    def __init__(this, component1, component2, name="isolated_from"):
        this.name = name

        if isinstance(component1, list):
            this.component1 = ' '.join(str(elem) for elem in component1)
        else:
            this.component1 = component1

        if isinstance(component2, list):
            this.component2 = ' / '.join(str(elem) for elem in component2)
        else:
            this.component2 = component2

    def __str__(this):
        #string = this.name + "(" + this.component1 + ", " + this.component2 + ")"
        string = this.component1 + " - " + this.name + " - " + this.component2
        return string

    def __eq__(self, other):
        if(not isinstance(other, Event)):
            return False

        if(not(self.name.rstrip() == other.name.rstrip())):
            return False

        if (not (self.component1.rstrip() == other.component1.rstrip())):
            return False

        if (not (self.component2.rstrip() == other.component2.rstrip())):
            return False

        return True

if __name__ == '__main__':
    test = Event("A", ["B", "D"])
    test2 = Event("A", ["B", "D"])
    test3 = Event("B", ["B", "D"])
    test4 = ["A", ["B", "C"]]

    print(test == test2)
    print(test == test3)
    print(test2 == test3)
    print(test == test4)


