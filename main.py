from Pricing_Simulate import Pricing
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__": 
    Nsims = 1000
    Nsteps =  365
    T =  1
    S0 = 100
    r = 0.03
    sigma = 0.20
    coupon_rate = 0.25
    knock_in = 80 
    knock_out = 105 
    principle_value = 10000
    
    np.random.seed(721)

    sim_path = Pricing.SimStock(Nsims, Nsteps, T, S0, r, sigma)
    out_time, in_time, no_time, Snowball_value, f_value = Pricing.Snowball_price(Nsims, Nsteps,sim_path, T, S0, r, sigma, coupon_rate, knock_in, knock_out, principle_value)
    Pricing.Snowball_plot(sim_path,knock_in, knock_out)


#sim_paths = PS.SimStock(1000, 365, 1, 100, 0.05, 0.2)
#out_time, in_time, no_time, Snowball_value, f_value = PS.Snowball_price(1000, 365,sim_paths, 1, 100, 0.05, 0.2, 0.25, 80, 110, 10000)
#PS.Snowball_plot(sim_paths,knock_in, knock_out)



