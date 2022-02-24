#  Calculate k0int for each calibration point
def k0int_from_Vint_pHcal(Vint, pHcal, T_C):
    '''
    Inputs
        Vint (V): Internal ref voltage
        pHcal (total scale): Calibration pH
        T_C (ºC): Measured T

    Outputs
        k0int (V): defined as calibration constant at 0 C
        k0int_insitu (V): temperature-corrected calibration value
    '''
    # Constants
    # Universal gas constant, (R) , http://physics.nist.gov/cgi-bin/cuu/Value?r
    R    = 8.31451          # J/(mol K)
    F    = 96487            # Faraday constant Coulomb / mol

    k2_int = -0.00125
    k2_ext = -0.001048

    # Lumped, converted quantities
    T_K = T_C+273.15 # used often enough to warrant new variable
    S_Nernst = (R*T_K)/F*np.log(10) # ditto ^^^

    # Nernst calibration coefficients, standard-ish potentials
    k0int_insitu = Vint-S_Nernst*pHcal # Calc E0int from Nernst & pH @ calibration point
    k0int = k0int_insitu-k2_int*T_C

    return k0int_insitu, k0int
