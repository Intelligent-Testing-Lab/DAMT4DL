# This file is adapted from the following source:
# Title: Replication package for the "DeepCrime: Mutation Testing of Deep Learning Systems based on Real Faults" paper
# Authors: Nargiz Humbatova, Gunel Jahangirova, & Paolo Tonella
# Conference: ACM SIGSOFT International Symposium on Software Testing and Analysis (ISSTA), Aarhus, Denmark
# Link: https://zenodo.org/records/4772465
# DOI: https://doi.org/10.5281/zenodo.4772465
# License: Creative Commons Attribution 4.0 International

import numpy as np
import pandas as pd 
import statsmodels.api as sm

from patsy import dmatrices
from scipy.stats import wilcoxon

def is_diff_sts(orig_accuracy_list, accuracy_list, model_type = "classification", statistical_test = "GLM", threshold = 0.05):
    """
    Check if the difference between the original model and the mutant is statistically significant.

    Returns:
    - is_sts: boolean: True if the difference is statistically significant, False otherwise
    - p_value: float: the p-value of the statistical test
    - effect_size: float: the Cohen's d effect size
    """
    # if there is nan in the accuracy list, view it as different with the original
    if np.isnan(accuracy_list).any():
        return True, 0, 0

    if statistical_test == "WLX":
        p_value = p_value_wilcoxon(orig_accuracy_list, accuracy_list)
    elif statistical_test == "GLM":
        p_value = p_value_glm(orig_accuracy_list, accuracy_list)
    else:
        raise Exception("The selected statistical test is invalid/not implemented.")

    effect_size = abs(cohen_d(orig_accuracy_list, accuracy_list))

    is_sts = ((p_value < threshold) and effect_size >= 0.5)

    return is_sts, p_value, effect_size


    
def p_value_wilcoxon(orig_accuracy_list, accuracy_list):
    """
    Calculate the p-value using the Wilcoxon signed-rank test.
    """
    # If the lists are the same, return 1.0
    if orig_accuracy_list == accuracy_list:
        return 1.0
    w, p_value_w = wilcoxon(orig_accuracy_list, accuracy_list)

    return p_value_w

def p_value_glm(orig_accuracy_list, accuracy_list):
    """
    Calculate the p-value using the Generalized Linear Model.
    """
    # If the lists are the same, return 1.0
    if orig_accuracy_list == accuracy_list:
        return 1.0

    list_length = len(orig_accuracy_list)

    zeros_list = [0] * list_length
    ones_list = [1] * list_length
    mod_lists = zeros_list + ones_list
    acc_lists = orig_accuracy_list + accuracy_list

    data = {'Acc': acc_lists, 'Mod': mod_lists}
    df = pd.DataFrame(data)

    response, predictors = dmatrices("Acc ~ Mod", df, return_type='dataframe')
    glm = sm.GLM(response, predictors)
    glm_results = glm.fit()
    glm_sum = glm_results.summary()
    pv = str(glm_sum.tables[1][2][4])
    p_value_g = float(pv)

    return p_value_g

def cohen_d(orig_accuracy_list, accuracy_list):
    """
    Calculate the Cohen's d effect size.
    """
    nx = len(orig_accuracy_list)
    ny = len(accuracy_list)
    dof = nx + ny - 2
    pooled_std = np.sqrt(((nx-1)*np.std(orig_accuracy_list, ddof=1) ** 2 + (ny-1)*np.std(accuracy_list, ddof=1) ** 2) / dof)
    result = (np.mean(orig_accuracy_list) - np.mean(accuracy_list)) / pooled_std
    return result