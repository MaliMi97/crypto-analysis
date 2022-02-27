import numpy as np

'''
This python script contains various metrics, which can be used to create on-chain metrics.
'''

def L_1_norm_single_value(v, v_ref):
    return (v - v_ref)/v_ref

def L_k_norm(vs, v_refs, k):
    nom, denom = 0, 0
    for i,j in zip(vs, v_refs):
        nom += (i - j)**k
        denom += j**k
    return (nom/denom)**(1./k)

def moving_L_k_norm(vs, v_refs, k, step):
    if len(vs) != len(v_refs):
        raise Exception("values and v_refs have dofferent length!")
    return np.array([L_k_norm(vs[i-step:i], v_refs[i-step:i], k) for i in np.arange(step, len(vs))])

def order_1_precision_1_backwards_difference(vs):
    return np.array([vs[i] - vs[i-1] for i in np.arange(1, len(vs))])

def order_1_precision_2_backwards_difference(vs):
    return np.array([1.5*vs[i] - 2*vs[i-1] + 0.5*vs[i-2] for i in np.arange(2, len(vs))])

def order_1_precision_2_central_difference(vs):
    return np.array([0.5*(vs[i+1] - vs[i-1]) for i in np.arange(1, len(vs)-1)])

def moving_average(vs, step):
    return np.array([np.sum(vs[i-step+1:i+1])/step for i in np.arange(step-1, len(vs))])

def exponential_moving_average(vs, step):
    ema = [np.sum(vs[:step])/step]
    for i in np.arange(step,len(vs)):
        ema.append(2/(step+1)*(vs[i] - ema[i-step]) + ema[i-step])
    return np.array(ema)