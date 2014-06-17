import sys
import time, sys
import logging

class QueryTools:
    @classmethod
    def query_yes_no(self, question, default="yes"):
        """Ask a yes/no question via raw_input() and return their answer.

        "question" is a string that is presented to the user.
        "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

        The "answer" return value is one of "yes" or "no".
        """
        valid = {"yes":True,   "y":True,  "ye":True,
                "no":False,     "n":False}
        if default == None:
            prompt = " [y/n] "
        elif default == "yes":
            prompt = " [Y/n] "
        elif default == "no":
            prompt = " [y/N] "
        else:
            raise ValueError("invalid default answer: '%s'" % default)

        while True:
            sys.stdout.write(question + prompt)
            choice = raw_input().lower()
            if default is not None and choice == '':
                return valid[default]
            elif choice in valid:
                return valid[choice]
            else:
                sys.stdout.write("Please respond with 'yes' or 'no' "\
                                "(or 'y' or 'n').\n")

class ConsoleProgress:
    verbose = True

    def __init__(self, size, verbose_=None, message=""):
        if verbose_ is not None:
            self.verbose = verbose_
        else:
            self.verbose = self.__class__.verbose
        if not self.verbose:
            return
        self.message = message
        self.size = size
        self.current_state = 0
        self.start_time = time.time()
        if message:
            logging.info(message+"...")
        else:
            print

    def update_progress(self, index):
        self.current_state = index
        if not self.verbose:
            return
        sys.stdout.write("\r{0:.2f}%".format(100*float(index)/self.size))
        sys.stdout.flush()

    def increment_progress(self):
        self.update_progress(self.current_state + 1)

    def finish(self):
        if not self.verbose:
            return
        sys.stdout.write("\r")
        sys.stdout.flush()
        message = ""
        if self.message:
            message = self.message+" completed in "
        else:
            message = "Completed in "
        message = message + str(time.time() - self.start_time) + 's'
        logging.info(message)
