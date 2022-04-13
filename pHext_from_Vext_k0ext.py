def pHext_from_Vext_k0ext(k0ext, Vext, T_C, sal):
    # See Martz et al. 2010, Bresnahan et al. 2014 for greater detail
    '''
    Inputs
        External ref voltage (V)
        Calibration coefficient, k0ext (25 ºC value)
        Measured T (C)
        Salinity (PSU)

    Outputs
        pHext (total scale)
    '''
    # Constants
    # Universal gas constant, (R) , http://physics.nist.gov/cgi-bin/cuu/Value?r
    import numpy as np
    R    = 8.31451          # J/(mol K)
    F    = 96487            # Faraday constant Coulomb / mol

    k2_int = -0.001101
    k2_ext = -0.001048

    # Lumped, converted quantities
    T_K = T_C+273.15 # used often enough to warrant new variable
    S_Nernst = (R*T_K)/F*np.log(10) # ditto ^^^

    # Physical chemistry calcs based on temp and salinity
    Z = 19.924*sal/(1000-1.005*sal) # Ionic strength, Dickson et al. 2007
    SO4_tot = (0.14/96.062)*(sal/1.80655) # Total conservative sulfate
    cCl = 0.99889/35.453*sal/1.80655 # Conservative chloride
    mCl = cCl*1000/(1000-sal*35.165/35) # mol/kg-H2O
    K_HSO4 = np.exp(-4276.1/T_K+141.328-23.093*np.log(T_K)
                    +(-13856/T_K+324.57-47.986*np.log(T_K))*Z**0.5
                    +(35474/T_K-771.54+114.723*np.log(T_K))*Z-2698/T_K*Z**1.5
                    +1776/T_K*Z**2+np.log(1-0.001005*sal)) # Bisulfate equilibrium const., Dickson et al. 2007
    DHconst = 0.00000343*T_C**2+0.00067524*T_C+0.49172143 # Debye-Huckel, Khoo et al. 1977
    log10gamma_HCl = 2*(-DHconst*np.sqrt(Z)/(1+1.394*np.sqrt(Z))+(0.08885-0.000111*T_C)*Z)

    # Nernstian pH calculations
    pHext_free = -(((k0ext+k2_ext*(T_C-0))-Vext)-S_Nernst*(np.log10(mCl)+log10gamma_HCl))/S_Nernst # mol/kg-H2O
    pHext_free = pHext_free-np.log10((1000-sal*35.165/35)/1000) # mol/kg-sw
    pHext_tot = pHext_free-np.log10(1+SO4_tot/K_HSO4)

    return pHext_tot
