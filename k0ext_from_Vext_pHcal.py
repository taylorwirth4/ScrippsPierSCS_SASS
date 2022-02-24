#  Calculate k0ext for each calibration point
def k0ext_from_Vext_pHcal(Vext, pHcal, T_C, calsal=35):
    '''
    Inputs
        Vext (V): External ref voltage
        pHcal (total scale): Calibration pH
        T_C (ºC): Measured T during calibration
        calsal (PSU): Measured S during calibration

    Outputs
        k0ext (V): defined as calibration constant at 0 C
        k0ext_insitu (V): temperature-corrected calibration value
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

    # Physical chemistry calcs based on temp and salinity
    Z = 19.924*calsal/(1000-1.005*calsal) # Ionic strength, Dickson et al. 2007
    SO4_tot = (0.14/96.062)*(calsal/1.80655) # Total conservative sulfate
    cCl = 0.99889/35.453*calsal/1.80655 # Conservative chloride
    mCl = cCl*1000/(1000-calsal*35.165/35) # mol/kg-H2O
    K_HSO4 = np.exp(-4276.1/T_K+141.328-23.093*np.log(T_K)
                    +(-13856/T_K+324.57-47.986*np.log(T_K))*Z**0.5
                    +(35474/T_K-771.54+114.723*np.log(T_K))*Z-2698/T_K*Z**1.5
                    +1776/T_K*Z**2+np.log(1-0.001005*calsal)) # Bisulfate equilibrium const., Dickson et al. 2007
    pHcal_free = pHcal+np.log10(1+SO4_tot/K_HSO4)
    cHfree = 10**(-pHcal_free) # mol/kg-sw, not used
    pHcal_free = pHcal_free+np.log10((1000-calsal*35.165/35)/1000) # mol/kg-H2O
    mHfree = 10**(-pHcal_free) # mol/kg-H2O
    DHconst = 0.00000343*T_C**2+0.00067524*T_C+0.49172143 # Debye-Huckel, Khoo et al. 1977
    log10gamma_HCl = 2*(-DHconst*np.sqrt(Z)/(1+1.394*np.sqrt(Z))+(0.08885-0.000111*T_C)*Z)
    aHfree_aCl = mHfree*mCl*10**(log10gamma_HCl)

    # Nernst calibration coefficients, standard-ish potentials
    k0ext_insitu = Vext+S_Nernst*np.log10(aHfree_aCl)
    k0ext = k0ext_insitu-k2_ext*T_C

    return k0ext_insitu, k0ext
