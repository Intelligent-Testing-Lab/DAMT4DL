# This file is adapted from the following source:
# Title: Replication package for the "DeepCrime: Mutation Testing of Deep Learning Systems based on Real Faults" paper
# Authors: Nargiz Humbatova, Gunel Jahangirova, & Paolo Tonella
# Conference: ACM SIGSOFT International Symposium on Software Testing and Analysis (ISSTA), Aarhus, Denmark
# Link: https://zenodo.org/records/4772465
# DOI: https://doi.org/10.5281/zenodo.4772465
# License: Creative Commons Attribution 4.0 International

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class AddAFMutationError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class InvalidStatisticalTest(Error):
    """Exception raised for errors in the input.

        Attributes:
            expression -- input expression in which the error occurred
            message -- explanation of the error
        """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message