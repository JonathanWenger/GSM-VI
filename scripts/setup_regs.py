import numpy as np
from gsmvi.ls_gsm import Regularizers


def setup_regularizer(reg0):

    # default lambda_t
    regularizer = Regularizers()

    # 0: batch_size
    #print("Using lambda_t = c")
    reg0 = regularizer.constant(reg0)

    # 1: batch_size / (t + 1)
    #print("Using lambda_t = c/t")
    reg1 = regularizer.custom(lambda t : reg0/t)

    # 1: batch_size / (t + 1)
    #print("Using lambda_t = c/\sqrt{t}")
    reg2 = regularizer.custom(lambda t : reg0/t**0.5)

    #print("Using lambda_t = B/(D*(t+1))")
    regs = [reg0, reg1, reg2]

    return regs
