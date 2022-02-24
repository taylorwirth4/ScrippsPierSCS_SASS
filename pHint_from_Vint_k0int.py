def pHint_from_Vint_k0int(k0int, Vint, T_C):
    # See Martz et al. 2010, Bresnahan et al. 2014 for greater detail
    '''
    Inputs
        Internal ref voltage (V)
        Calibration coefficient, k0int (25 ºC value)
        Measured T (C)

    Outputs
        pHint (total scale)
    '''
    # Constants
    # Universal gas constant, (R) , http://physics.nist.gov/cgi-bin/cuu/Value?r
    import numpy as np
    R    = 8.31451          # J/(mol K)
    F    = 96487            # Faraday constant Coulomb / mol

    k2_int = -0.00125
    k2_ext = -0.001048
    
    # Lumped, converted quantities
    T_K = T_C+273.15 # used often enough to warrant new variable
    S_Nernst = (R*T_K)/F*np.log(10) # ditto ^^^

    # Nernstian pH calculation
    pHint_tot = (Vint-(k0int+k2_int*(T_C-25)))/S_Nernst # Calc pHint from Nernst, the "-0" added explicitly intentionally

    return pHint_tot
