"""Probe: does swe.set_sid_mode() corrupt calc_ut() without FLG_SIDEREAL?

Run:  <venv>/bin/python scripts/sidereal_mode_probe.py [path/to/ephe]
Settles the contradiction documented in references/sidereal-mode-resolved.md.
"""
import sys

import swisseph as swe

swe.set_ephe_path(sys.argv[1] if len(sys.argv) > 1 else "/home/zd0l0r/Projects/astrologica/ephe")

JD = swe.julday(1991, 2, 15, 17 + 45 / 60.0)   # 17:45 UT
BASE = swe.FLG_SWIEPH | swe.FLG_SPEED          # deliberately NO FLG_SIDEREAL


def tropical_sun():
    return swe.calc_ut(JD, swe.SUN, BASE)[0][0]


base = tropical_sun()
print(f"pristine                       : {base:.6f}")

ay_default = swe.get_ayanamsa(JD)              # BEFORE any set_sid_mode
print(f"  get_ayanamsa() before set_sid : {ay_default:.6f}  <-- NOT Lahiri")
print(f"  calc_ut unchanged?            : {tropical_sun() == base}")

swe.set_sid_mode(swe.SIDM_LAHIRI)
print(f"Lahiri ayanamsa                : {swe.get_ayanamsa(JD):.6f}")
print(f"  calc_ut unchanged?            : {tropical_sun() == base}   (copy A claims False)")

true_sid = swe.calc_ut(JD, swe.SUN, BASE | swe.FLG_SIDEREAL)[0][0]
print(f"FLG_SIDEREAL (Lahiri)          : {true_sid:.6f}")
print(f"  manual tropical-ayanamsa      : {(base - swe.get_ayanamsa(JD)) % 360:.6f}")
print(f"  method gap (arcsec)           : "
      f"{abs(true_sid - ((base - swe.get_ayanamsa(JD)) % 360)) * 3600:.1f}")

swe.set_sid_mode(swe.SIDM_RAMAN)
raman = swe.calc_ut(JD, swe.SUN, BASE | swe.FLG_SIDEREAL)[0][0]
print(f"FLG_SIDEREAL (Raman, silent)   : {raman:.6f}")
print(f"  shift vs Lahiri (arcmin)      : {abs(raman - true_sid) * 60:.2f}  <-- no error raised")

swe.set_sid_mode(swe.SIDM_LAHIRI)
print(f"restored, calc_ut unchanged?   : {tropical_sun() == base}")

print("\nVERDICT: copy A's 'silent correction' claim is FALSE;")
print("         the real trap is that get_ayanamsa()/FLG_SIDEREAL read an")
print("         unset global whose default is not Lahiri.")
