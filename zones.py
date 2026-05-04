def get_zone(x, width):
    if x < width // 3:
        return "A"
    elif x < 2 * width // 3:
        return "B"
    return "C"