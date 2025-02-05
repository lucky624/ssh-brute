from colorama import init, Fore, Back, Style
import os

if os.name == "posix":
    # colors foreground text:
    fc = "\033[0;96m"
    fg = "\033[0;92m"
    fw = "\033[0;97m"
    fr = "\033[0;91m"
    fb = "\033[0;94m"
    fy = "\033[0;33m"
    fm = "\033[0;35m"
    ff = Fore.RESET
    # colors background text:
    bc = "\033[46m"
    bg = "\033[42m"
    bw = "\033[47m"
    br = "\033[41m"
    bb = "\033[44m"
    by = "\033[43m"
    bm = "\033[45m"
    bf = Back.RESET
    # colors style text:
    sd = Style.DIM
    sn = Style.NORMAL
    sb = Style.BRIGHT
    sf = Style.RESET_ALL

else:
    init(autoreset=True)
    # colors foreground text:
    fc = Fore.CYAN
    fg = Fore.GREEN
    fw = Fore.WHITE
    fr = Fore.RED
    fb = Fore.BLUE
    fy = Fore.YELLOW
    fm = Fore.MAGENTA
    ff = Fore.RESET
    # colors background text:
    bc = Back.CYAN
    bg = Back.GREEN
    bw = Back.WHITE
    br = Back.RED
    bb = Back.BLUE
    by = Back.YELLOW
    bm = Back.MAGENTA
    bf = Back.RESET

    # colors style text:
    sd = Style.DIM
    sn = Style.NORMAL
    sb = Style.BRIGHT
    sf = Style.RESET_ALL

fgb = fg + sb
fbb = fb + sb
fyb = fy + sb
fcb = fc + sb
frb = fr + sb
fwb = fw + sb
fmb = fm + sb
ffb = ff + sb

info_out = fgb + "[$] "
ver_out = fyb + "[+] "
err_out = frb + "[-] "

