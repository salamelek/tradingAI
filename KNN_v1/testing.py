# ANSI escape codes for text formatting
RESET = "\033[0m"
BOLD = "\033[1m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
BG_BLACK = "\033[40m"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"
BG_BLUE = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN = "\033[46m"
BG_WHITE = "\033[47m"

# Example usage
# print(RED + "This is red text." + RESET)
# print(BOLD + GREEN + "This is bold green text." + RESET)
# print(BG_BLUE + WHITE + "This is white text on a blue background." + RESET)

# print(RED + BOLD + "SHORT" + RESET)
# print("SHORT")

print("\033[33m" + "\033[1m" + "HOLD" + "\033[0m")
