import numpy as np


def scidx(bw, ng):
    """SubCarrier InDeX

    Table 9-54-Number of matrices and carrier grouping

    Args:
        bw (int): Bandwidth, it can be 20 and 40.
        ng (int): Grouping, it can be 1, 2 and 4.

    Returns:
        ndarray: Subcarrier index

    Examples:

        >>> s_index = scidx(20, 2)

    References:
        1. `IEEE Standard for Information technology—Telecommunications and
        information exchange between systems Local and metropolitan area
        networks—Specific requirements - Part 11: Wireless LAN Medium Access
        Control (MAC) and Physical Layer (PHY) Specifications, in
        IEEE Std 802.11-2016 (Revision of IEEE Std 802.11-2012), vol., no.,
        pp.1-3534, 14 Dec. 2016, doi: 10.1109/IEEESTD.2016.7786995. <#>`_
    """
    if bw not in [20, 40] or ng not in [1, 2, 4]:
        raise ValueError("bw should be [20, 40] and ng should be [1, 2, 4]")
    a, b = int(bw * 1.5 - 2), int(bw / 20)
    k = np.r_[-a:-b:ng, -b, b:a:ng, a]
    return k


def calib(phase, bw=20, ng=2, axis=1):
    """Phase calibration

    Args:
        phase (ndarray): Unwrapped phase of CSI.
        bw (int): Bandwidth, it can be 20 and 40. Default: 20
        ng (int): Grouping, it can be 1, 2 and 4. Default: 2
        axis (int): Axis along which is subcarrier. Default: 1

    Returns:
        ndarray: Phase calibrated

    Examples:

        >>> csi = csidata.csi[:10]
        >>> phase = np.unwrap(np.angle(csi), axis=1)
        >>> phase = calib(phase, bw=20, ng=2, axis=1)

    References:
        1. `Enabling Contactless Detection of Moving Humans with Dynamic Speeds
        Using CSI <#>`_
    """
    p = np.asarray(phase)
    s = scidx(bw, ng)

    slice1 = [slice(None, None)] * p.ndim
    slice1[axis] = slice(-1, None)
    slice1 = tuple(slice1)
    slice2 = [slice(None, None)] * p.ndim
    slice2[axis] = slice(None, 1)
    slice2 = tuple(slice2)
    shape1 = [1] * p.ndim
    shape1[axis] = s.shape[0]
    shape1 = tuple(shape1)

    k_n, k_1 = s[-1], s[1]
    a = (p[slice1] - p[slice2]) / (k_n - k_1)
    b = p.mean(axis=axis, keepdims=True)
    s = s.reshape(shape1)

    phase_calib = p - a * s - b
    return phase_calib
