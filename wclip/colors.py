def color_temperature(celsius):
    if celsius < 0:
        return "bright_cyan"
    if celsius < 15:
        return "bright_blue"
    if celsius < 27:
        return "bright_green"
    if celsius < 35:
        return "bright_yellow"
    return "bright_red"

def color_relative_humidity(percent):
    if percent < 30:
        return "bright_yellow"
    if percent < 60:
        return "bright_green"
    if percent < 80:
        return "bright_cyan"
    return "bright_blue"

def color_precipitation(mm):
    if mm == 0:
        return "bright_green"
    if mm < 3:
        return "bright_yellow"
    if mm < 10:
        return "dark_orange"
    return "bright_red"

def color_wind_speed(kmh):
    if kmh < 10:
        return "bright_green"
    if kmh < 30:
        return "bright_yellow"
    if kmh < 60:
        return "dark_orange"
    return "bright_red"

def color_cloud_cover(percent):
    if percent < 25:
        return "light_cyan1"
    if percent < 50:
        return "sky_blue1"
    if percent < 75:
        return "deep_sky_blue3"
    return "grey50"

def color_visibility(km):
    if km < 3:
        return "bright_red"
    if km < 7:
        return "dark_orange"
    if km < 10:
        return "bright_yellow"
    return "bright_green"

def color_surface_pressure(hpa):
    if hpa < 1000:
        return "bright_red"
    if hpa < 1020:
        return "bright_green"
    return "bright_cyan"