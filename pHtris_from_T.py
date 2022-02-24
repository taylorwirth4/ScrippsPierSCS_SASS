# Calculate tris pH
def pHtris_from_T(T_C, S=35):
    T_K = T_C+273.15

    # Eq. 18 DelValls and Dickson 1998
    pH = (11911.08 - 18.2499*S - 0.039336*S**2)/T_K - 366.27059 + 0.53993607*S + 0.00016329*S**2 + (64.52243 - 0.084041*S)*np.log(T_K) - 0.11149858*T_K

    return pH
