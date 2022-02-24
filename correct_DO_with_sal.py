# Correct O2 following Aanderaa salinity compensation calcs from manual
def correct_DO_with_sal(O2_uM, T_C, pressure, sal_meas, sal_input=0):
    '''
    Inputs
        O2_uM (µM): Dissolved oxygen recorded by Aanderaa with no salinity compensation applied
        T_C (ºC): Temperature measured by Aanderaa or auxiliary thermometer
        pressure (dbar): Pressure measured by auxiliary pressure sensor
        sal_meas (PSU): Salinity measured by auxiliary salinity/conductivity sensor
        sal_input (PSU): Salinity input into Aanderaa pre-deployment, usually 0
    '''

    # Coefficients from manual
    B0 = -0.00624097; B1 = -0.00693498; B2 = -0.00690358; B3 = -0.00429155;
    C0 = -0.00000031168
    Pcorr = 0.032

    # Calculations from manual
    Ts = np.log((298.15-T_C)/(273.15+T_C)) # scaled temp
    Sfctr = np.exp((sal_meas-sal_input)*(B0+B1*Ts+B2*Ts**2+B3*Ts**3))+C0*(sal_meas**2-sal_input**2)
    Pfctr = 1+np.abs(pressure)/1000*Pcorr
    O2_corr = O2_uM*Sfctr*Pfctr

    return O2_corr
