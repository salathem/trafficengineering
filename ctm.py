def ctm(net):
    length = net.length
    p_jam = net.fundamentaldiagram.jam_density
    v_f = net.fundamentaldiagram.free_flow_speed
    q = net.fundamentaldiagram.flow_capacity
    t_i = net.time_interval
    t_simu = net.time_simulation
    t_i_h = t_i/3600          #Time Intervall [h]
    t_simu_h = t_simu/3600      #Duration of Simulation [h]

    if t_i_h <= length/v_f:
        print("CFL check okay.")
    else:
        print("CFL check not okay.")

    #Script:
    for time in range(10, t_simu, t_i):
        k = time/t_i

        for cell in net.cells:

            #On Ramp and Start Ramp Demand
            if time <= 450:
                d_i = cell.d_in * time / 450
                d_array(1, k) = d_i
            elif 450 < time <= 3150:
                d_i = cell.d_in
                d_array(1, k) = d_i
            elif 3150 < time < 3600:
                d_i = cell.q_in - cell.d_in * (time - 3150) / 450
                d_array(1, k) = d_i
            else:
                d_i = 0
                d_array(1, k) = d_i

            if time <= 900:
                x_i = cell.x_in / 900 * time
                x_array(1, k) = d_i
            elif 900 < time < 2700:
                x_i = cell.x_in
                x_array(1, k) = d_i
            elif 2700 < time < 3600:
                x_i = cell.x_in - cell.x_in / 900 * (time - 2700)
                x_array(1, k) = d_i
            else:
                x_i = 0
                x_array(1, k) = d_i

            #Start Ramp Demand and Queue
            if cell.index == 1:
                q_0 = min([d_i + queue1(1, k) / t_i_h, w(i, k) * ((p_jam(i, k) - p(i, k)) * cell.lanes Q(i, k) * lanes(i, 1)])
                q_0_log(1, k) = q_0
                queue1(1, k + 1) = queue1(1, k) + (d_i - q_0) * T

            #Traffic Volume - -----------------------------------------------
            q(i, k) = v(i, k) * p(i, k) * cell.lanes

            #On Ramp Demand and Queue - -------------------------------------
            if cell.index == 4:
                q_dash = min([v(i - 1, k) * p(i - 1, k) * cell.lanesbefor w(i, k) * (p_jam(i, k) - p(i, k)) * cell.lanesbefor
                              Q(i - 1, k) * cell.lanesbefor])
                r_dash = queue2(1, k) / T + x_i
                if q_dash + r_dash <= w(i, k) * (p_jam(i, k) - p(i, k)) * cell.lanesbefor
                    q(i - 1, k) = q_dash
                    r(1, k) = r_dash
                else:
                    q(i - 1, k) = q_dash / (q_dash + r_dash) * w(i, k) * (p_jam(i, k) - p(i, k)) * cell.lanesbefor
                    r(1, k) = r_dash / (q_dash + r_dash) * w(i, k) * (p_jam(i, k) - p(i, k)) * cell.lanesbefor

            queue2(1, k + 1) = queue2(1, k) + (x_i - r(1, k)) * T

            #Number of Vehicles in cell - -----------------------------------
            if cell.index == 1:
                n(i, k + 1) = n(i, k) + t_i_h * (q_0 - q(i, k))
            elif cell.index == 3:
                n(i, k + 1) = n(i, k) + t_i_h * (q(i - 1, k) + r(1, k) - q(i, k));
            else:
                n(i, k + 1) = n(i, k) + t_i_h * (q(i - 1, k) - q(i, k))

            #Density - -------------------------------------------------------
            p(i, k + 1) = n(i, k + 1) / length / cell.lanes

            #Velocity - ------------------------------------------------------
            if p(i, k) == 0:
                v(i, k) = vf
            else:
                v(i, k) = q(i, k) / (p(i, k) * cell.lanes)
