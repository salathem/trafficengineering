def user_input_check(method, nr_of_steps, delta_time, scenario, precision, show_plots, show_animation, show_values, save_plots, diagram_type, dpi, is_applied, k, optimise_k, show_max_cell, show_max_net):
    user_input_is_valid = True
    booleans = [[show_plots, "show_plots"], [show_animation, "show_animation"], [show_values, "show_values"], [save_plots, "save_plots"], [is_applied, "is_applied"], [optimise_k, "optimise_k"], [show_max_cell, "show_max_cell"], [show_max_net, "show_max_net"]]

    if method not in ["ctm", "metanet", "all"]:
        print("method is not (ctm/metanet/all)")
        user_input_is_valid = False

    if scenario not in ["a", "b", "c", "all"]:
        print("scenario is not (a/b/c/all)")
        user_input_is_valid = False

    if diagram_type not in ["2D", "3D", "all"]:
        print("diagram_type is not (2D/3D/all)")
        user_input_is_valid = False

    if type(nr_of_steps) != int:
        print("nr_of_steps is not an Integer")
        user_input_is_valid = False

    if type(delta_time) != float:
        print("delta_time is not an Float")
        user_input_is_valid = False

    if not (0.1 > precision > 0 or type(precision) is float):
        print("not 0.1 > precision > 0 or is not float")
        user_input_is_valid = False

    if not (1000 > k > 0) or not (type(k) is float):
        print("not 1000 > k > 0 or is not float")
        user_input_is_valid = False

    if not (1000 > dpi > 100) or not (type(dpi) is int):
        print("not 1000 > dpi > 100 or is not int")
        user_input_is_valid = False

    for boolean in booleans:
        if type(boolean[0]) != bool:
            print(boolean[1] + " is not a Boolean")
            user_input_is_valid = False
    return user_input_is_valid
