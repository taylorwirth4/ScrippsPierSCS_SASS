import numpy as np
def calcO2sat(tempC, S):

    # [O2sat] = calcO2sat(tempC, S)
    # This function calculates oxygen saturation concentration  based on 
    # Garcia and Gordon, 1992
 
    # The input tempC is in Celcius. 
    # The output units are umol/kg.
    
    # Creatd by: Yui Takeshita, converted to python by Taylor Wirth July 25, 2022
    # Monterey Bay Aquarium Research Institute
    # Version 1 Created: November 23, 2016

    # Constants are from Benson and Krause (1994).
    # A0 = 5.80871
    # A1 = 3.20291
    # A2 = 4.17887
    # A3 = 5.10006
    # A4 = -9.86643e-2
    # A5 = 3.80369
    # B0 = -7.01577e-3
    # B1 = -7.70028e-3
    # B2 = -1.13864e-2
    # B3 = -9.51519e-3
    # C0 = -2.75915e-7

    # Constants from combined fit
    A0 = 5.80818
    A1 = 3.20684
    A2 = 4.11890
    A3 = 4.93845
    A4 = 1.01567
    A5 = 1.41575
    B0 = -7.01211e-3
    B1 = -7.25958e-3
    B2 = -7.93334e-3
    B3 = -5.54491e-3
    C0 = -1.32412e-7

    T = np.log((298.15-tempC)/(273.15+tempC)) 

    O2atsat = np.exp(A0 + A1*T + A2*T**2 + A3*T**3 + A4*T**4 + A5*T**5 + S*(B0 + B1*T + B2*T**2 + B3*T**3) + C0*S**2)

    return O2atsat