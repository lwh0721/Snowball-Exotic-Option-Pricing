import numpy as np
import matplotlib.pyplot as plt


class Pricing():

    def SimStock(Nsims, Nsteps, T, S0, r, sigma):
        dt = T/Nsteps
        
        S = np.zeros(Nsteps+1)
        S[0] = S0
        
        sim_paths = np.zeros((Nsims,Nsteps+1))
        sim_paths[:,0]=S0
        
        for i in range(Nsims):
            for j in range(0, Nsteps):
                S[j + 1] = S[j] * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * np.random.randn())
        
            sim_paths[i] = S
        #plt.figure(figsize=(21, 7))
        #plt.plot(sim_paths.T)
        return sim_paths
    

    
    def Snowball_price(Nsims, Nsteps,sim_path, T, S0, r, sigma, coupon_rate, knock_in, knock_out, principle_value):
        # The observation date that the knock-out is valid
        obser_date = {90,120,150,180,210,240,270,300,330,360}

        # Record the times that each scenario happens
        out_time = 0 
        in_time = 0
        no_time = 0

        # Record Option value 
        f_value = np.zeros(Nsims)

        
        for i in range(Nsims):
            # Check every path and record whether the knock_in or knock_out happens
            knock_in_flag = 0
            knock_out_flag = 0
            knock_time = 0# record the time step that happens knock_in or knock_out
            
            for j in range(0, Nsteps):
                if sim_path[i,j+1] > knock_out:
                    if j+1 in obser_date:
                        knock_time = j+1
                        knock_out_flag = 1
                        break
                elif sim_path[i,j+1] < knock_in:
                    knock_in_flag = 1
                    break
            
            # Valid Knock-out happens
            if knock_out_flag == 1:
                f_value[i] = coupon_rate * knock_time/365 * principle_value * np.exp(-r * knock_time / 365)
                out_time += 1

            # Knock-in, No knock-out
            elif knock_out_flag == 0 and knock_in_flag ==1:
                f_value[i] = -1 * max(1 - (sim_path[i,-1]/S0), 0) * principle_value * np.exp(-r * T)
                in_time += 1

            # Neither knock-in nor knock-out
            elif knock_out_flag == 0 and knock_in_flag ==0:
                #f_value[i] = coupon_rate * Nsteps/365 * principle_value * np.exp(-r * T)
                f_value[i] = coupon_rate * principle_value * np.exp(-r * T)
                no_time += 1
        
        Snowball_value = sum(f_value) / Nsims
        
        print('Snowball Option Value is %.3f' % Snowball_value)
        print('Probability of Knock-out is %.3f' % (out_time/Nsims))
        print('Probability of Knock-in, No Knock-out is %.3f' % (in_time/Nsims))
        print('Probability of Neither knock-in nor knock-out is %.3f' % (no_time/Nsims))
        
        print('Probability of earning profit is %.3f' % ((out_time + no_time)/Nsims))
        print('Probability of loss is %.3f' % (in_time/Nsims))
        
        return out_time, in_time, no_time, Snowball_value, f_value

    

    def Snowball_plot(sim_path,knock_in, knock_out):
        plt.plot(sim_path.T)
        plt.axhline(y=knock_out, linestyle='--', label='Knock-out level', color="red")
        plt.axhline(y=knock_in, linestyle='--', label='Knock-in level', color="green")
        plt.legend()
        plt.xlabel("Time")
        plt.ylabel("Asset price")
        plt.title("Asset price Simulation")
        plt.show()