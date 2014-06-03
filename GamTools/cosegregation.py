import numpy as np


def get_transpositions(array):
    axes = range(len(array.shape))
    for i in axes:
        yield tuple(axes[i:] + axes[:i])


def frequency_to_probability(n):

    total = n.sum()
    f = n / float(total)
    
    return f


def get_marginal_probabilities(f):
    
    ind = []
    for t in get_transpositions(f):
        probs = [ f.transpose(t)[1,...].sum(), f.transpose(t)[0,...].sum() ]
        ind.append(probs)
    return np.array(ind)


def either_locus_not_detected(probs):

    if probs.min() == 0.0:
        return True
    else:
        return False


def raw(n):

    f = frequency_to_probability(n)

    if either_locus_not_detected(f):
        return np.NAN

    return f.flat[-1]


def D(n):
    f = frequency_to_probability(n)
    probs = get_marginal_probabilities(f)

    if either_locus_not_detected(f):
        return np.NAN

    expected = probs.prod(axis=0)[0]
    observed = f.flat[-1]
    return observed - expected


def Dmax(n):
    f = frequency_to_probability(n)
    probs = get_marginal_probabilities(f)

    d = D(n)
    expected = probs.prod(axis=0)[0]
    if d > 0:
        return min(probs[:,0]) - expected
    elif d < 0:
        return expected


def Dprime(n):
    d = D(n)
    dmax = Dmax(n)
    if dmax is None:
        return np.NAN
    else:
        return d / dmax


def corr(n):

    f = frequency_to_probability(n)
    probs = get_marginal_probabilities(f)

    d = D(n)

    return d / np.power(probs.prod(), 1./len(n.shape))


def clip_for_plotting(array, percentile=1.):

    clip_lower = np.percentile(array[np.isfinite(array)], percentile)
    clip_upper = np.percentile(array[np.isfinite(array)], (100. - percentile))
    return np.clip(array, clip_lower, clip_upper)