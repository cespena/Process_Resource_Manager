##from project1manager import ManagerClass
import project1manager as p1m

class WrongInputLengthError(Exception):
    pass

class WrongLength1Error(Exception):
    pass

class WrongLength2Error(Exception):
    pass

class WrongLength3Error(Exception):
    pass

class SecondElementNotIntError(Exception):
    pass

class ThirdElementNotIntError(Exception):
    pass

class IncorrectDestroyIndexError(Exception):
    pass

class IncorrectCreateIndexError(Exception):
    pass

class ManagerIsNoneError(Exception):
    pass

class NegativeValueError(Exception):
    pass

class ShellClass:
    def __init__(self):
        self.Manager = None
        self.running = 1
        self.user_input = None
        self.split_text = None
        self.debugging = 0############ REMEMBER TO CHANGE ##########


    def run_shell(self):
        while self.running:
            try:
                if self.debugging == 1:
                    self.user_input = input()

                else:
                    self.user_input = input()

                if self.user_input == 'cesar':
                    self.running = 0
                else:
                    self.split_text = self.user_input.split()
                    self.check_input()

            except WrongInputLengthError:
                self.print_error_message("Wrong Input Length")
            except WrongLength1Error:
                self.print_error_message("Wrong Length 1 Error")
            except WrongLength2Error:
                self.print_error_message("Wrong Length 2 Error")
            except WrongLength3Error:
                self.print_error_message("Wrong Length 3 Error")
            except SecondElementNotIntError:
                self.print_error_message("Second Element Not Int")
            except ThirdElementNotIntError:
                self.print_error_message("Third Element Not Int")
            except IncorrectDestroyIndexError:
                self.print_error_message("Incorrect Destroy Index Error")
            except IncorrectCreateIndexError:
                self.print_error_message("Incorrect Create Index Error")
            except ManagerIsNoneError:
                self.print_error_message("Manager Is None Error")
            except NegativeValueError:
                self.print_error_message("NegativeValueError")
            except p1m.CreateMoreThan16ProcessesError:
                self.print_error_message("CreateMoreThan16ProcessesError")
            except p1m.DestroyProcessThatsNotAChildOfCurrentProcessError:
                self.print_error_message("DestroyProcessThatsNotAChildOfCurrentProcessError")
            except p1m.RequestANonExistentResourceError:
                self.print_error_message("RequestANonExistentResourceError")
            except p1m.RequestAResourceProcessAlreadyHolding:
                self.print_error_message("RequestAResourceProcessAlreadyHolding")
            except p1m.ReleaseAResourceProcessIsNotHolding:
                self.print_error_message("ReleaseAResourceProcessIsNotHolding")
            except p1m.Process0RequestingAResourceError:
                self.print_error_message("Process0RequestingAResourceError")
            except p1m.DestroyProcess0Error:
                self.print_error_message("DestroyProcess0Error")
            except p1m.SizeOfUnitsIsZeroError:
                self.print_error_message("SizeOfUnitsIsZeroError")
            except p1m.IncorrectResourceSizePairError:
                self.print_error_message("IncorrectResourceSizePairError")
            except p1m.RequestedSizeTooBigError:
                self.print_error_message("RequestedSizeTooBigError")
            except EOFError:
                if self.debugging == 1:
                    print("* EndOfFile")
                # else:
                    # print()
                self.running = 0
            

    
    def check_input(self):
##        print(self.split_text)
        if self.Manager != None:
            if len(self.split_text) > 3:
                raise WrongInputLengthError
            elif len(self.split_text) == 3:
                self.check_length_3_functions()
            elif len(self.split_text) == 2:
                self.check_length_2_functions()
            elif len(self.split_text) == 1:
                self.check_length_1_functions()
            else:
                pass
        elif self.Manager == None:
            if len(self.split_text) == 1:
                if self.split_text[0] == "in":
                    self.check_length_1_functions()
                else:
                    raise ManagerIsNoneError
            else:
                raise ManagerIsNoneError

    def check_length_3_functions(self):
        '''
        rq<r><n>     request(r, n)
        rl<r><n>     release(r, n)
        '''
        try:
            self.split_text[1] = int(self.split_text[1])
        except ValueError:
            raise SecondElementNotIntError

        if self.split_text[1] < 0:
            raise NegativeValueError

        try:
            self.split_text[2] = int(self.split_text[2])
        except ValueError:
            raise ThirdElementNotIntError
        if self.split_text[2] < 0:
            raise NegativeValueError

##        print(self.split_text)
        if self.split_text[0] == "rq":
            self.Manager.request(self.split_text[1], self.split_text[2])
        elif self.split_text[0] == "rl":
            self.Manager.release(self.split_text[1], self.split_text[2])
        else:
            raise WrongLength3Error
    
    def check_length_2_functions(self):
        '''
        de<i>     destroy(i)
        cr<i>     create(i)
        '''
        try:
            self.split_text[1] = int(self.split_text[1])
        except ValueError:
            raise SecondElementNotIntError

        if self.split_text[0] == "de":
            if self.split_text[1] < 0 or self.split_text[1] > 15:
                raise IncorrectDestroyIndexError
            else:
                self.Manager.destroy(self.split_text[1])
        elif self.split_text[0] == "cr":
            if self.split_text[1] == 1 or self.split_text[1] == 2:
                self.Manager.create(self.split_text[1])
            else:
                raise IncorrectCreateIndexError
        else:
            raise WrongLength2Error

    def check_length_1_functions(self):
        '''
        to        timeout()
        in        init()
        '''
        if self.split_text[0] == "to":
            self.Manager.timeout()

        elif self.split_text[0] == "in":
            if self.Manager == None:
                self.Manager = p1m.ManagerClass(self.debugging)
            else:
                print()
                self.Manager = p1m.ManagerClass(self.debugging)
        else:
            raise WrongLength1Error


    def print_error_message(self, message):
        if(self.debugging == 1):
            print(message)
        else:
            print("-1 ", end='')

if __name__ == "__main__":
    shell = ShellClass()
    shell.run_shell()
