#!/usr/bin/env python
import logging
from os.path import splitext
import numpy as np
from semnet.writer import createOutput
from semnet import utils

################################################################################
# Add additional links to existing genes in the network
################################################################################
def add_newlinks_beta_to_beta(path, args):
    """ function to add new links to above all of the betas """
    # Initialize default values
    path.reinit()

    # Iterate overall of the endogenous variables (cols of beta)
    for index, gene in enumerate(path.yvar):
        # Determine if gene has multiple isoforms
        isoCnt = utils.isoCount(gene)

        # Iterate over the the endogenous varaibles (rows of beta) and add link
        # one at a time.
        for row, target in enumerate(path.yvar):
            # A gene cannot regulate itself in SEMs
            if row != index:
                # Determine if gene has multiple isoforms
                tCnt = utils.isoCount(target)

                # Skip when one gene is already regulating the other
                if path.beta[row, index] == 0 and path.beta[index, row] == 0:
                    model_type = "Adding Newlinks Beta to Beta:\n {0} -> {1}".format(gene, target)

                    path.beta[row:row+tCnt, index:index+isoCnt] = 1
                    createOutput(path, model_type, args)
                    path.beta[row:row+tCnt, index:index+isoCnt] = 0
                    path.count_increment()

def add_newlinks_gamma_to_beta(path, args):
    """ function to add new links to above all of the betas """
    # Initialize default values
    path.reinit()

    # Iterate overall of the exogenous variables
    for index, gene in enumerate(path.xvar):
        # Determine if gene has multiple isoforms
        isoCnt = utils.isoCount(gene)

        # Iterate over the rows of gamma and add link one at a time. In other words,
        # add new links to each of the endogenous variables.
        for row, target in enumerate(path.yvar):
            # Determine if gene has multiple isoforms
            tCnt = utils.isoCount(target)

            if path.gamma[row, index] == 0:
                model_type = "Adding Newlinks Gamma to Beta:\n {0} -> {1}".format(gene, target)

                path.gamma[row:row+tCnt, index:index+isoCnt] = 1
                createOutput(path, model_type, args)
                path.gamma[row:row+tCnt, index:index+isoCnt] = 0
                path.count_increment()

def add_newlinks_beta_to_gamma(path, args):
    """ function to add new links to above all of the betas """
    # Initialize default values
    path.reinit()

    # make a copy of the yvar and xvar for iteration, because I am going to be
    # messing with both lists
    _yvar = list(path.yvar)
    _xvar = list(path.xvar)


    # Iterate over all exogenous variables (cols of gamma), turn them into an
    # endogenous variable 1 at a time and then add all betas
    for col, target in enumerate(_xvar):
        # Determine if gene has multiple isoforms
        tCnt = utils.isoCount(target)

        # Convert exogenous varaible to an endogenous variable
        path.convert_ExogToEndog(target)

        # Now iterate over all endogenous variables (cols of beta)
        for index, gene in enumerate(_yvar):
            # Determine if gene has multiple isoforms
            isoCnt = utils.isoCount(gene)

            # Skip when one gene is already regulating the other
            if path.beta[index, -1] == 0:
                model_type = "Adding Newlinks Beta to Gamma :\n {0} -> {1}".format(gene, target)

                path.beta[-tCnt:, index:index+isoCnt] = 1
                createOutput(path, model_type, args)
                path.beta[-tCnt:, index:index+isoCnt] = 0
                path.count_increment()

        # Initialize default values
        path.reinit()

def add_newlinks_gamma_to_gamma(path, args):
    """ function to add new links to above all of the betas """
    # Initialize default values
    path.reinit()

    # make a copy of the yvar and xvar for iteration, because I am going to be
    # messing with both lists
    _xvar = list(path.xvar)

    # Iterate over all exogenous variables (cols of gamma), turn them into an
    # endogenous variable 1 at a time and then add all betas
    for col, target in enumerate(_xvar):
        # Determine if gene has multiple isoforms
        tCnt = utils.isoCount(target)

        # Convert exogenous varaible to an endogenous variable
        path.convert_ExogToEndog(target)

        # Now iterate over the new endogenous variable list (cols of gamma) and
        # add links 1 at a time to gamma
        for index, gene in enumerate(path.xvar):
            model_type = "Adding Newlinks Gamma to Gamma :\n {0} -> {1}".format(gene, target)

            # Determine if gene has multiple isoforms
            isoCnt = utils.isoCount(gene)

            # Skip when one gene is already regulating the other
            path.gamma[-tCnt:, index:index+isoCnt] = 1
            createOutput(path, model_type, args)
            path.gamma[-tCnt:, index:index+isoCnt] = 0
            path.count_increment()

        # Initialize default values
        path.reinit()
