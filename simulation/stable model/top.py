# Define top file
import numpy as np

eps1 = 2.0  # 2kBT, T=1
eps2 = 0.3  # for NB
eps3 = 1.0  # for repulsion only cases
eps4 = 5.0  # for TF to e/p

sigma1 = 0.6  # for LJ
sigma2 = 0.4  # for repulsion only cases

r0 = 0.4
Kb = 20000
Ka = 2 * eps1

Vs = 4 * eps1 * (sigma1) ** 6  # for e to p
Ws = 4 * eps1 * (sigma1) ** 12  # for e to p
Vn = 4 * eps2 * (sigma1) ** 6  # for normal blue beads
Wn = 4 * eps2 * (sigma1) ** 12  # for normal blue beads
Vr = 0  # for repulsion only cases
Wr = 4 * eps3 * (sigma2) ** 12  # for repulsion only cases
Vt = 4 * eps4 * (sigma1) ** 6  # for TF to e/p
Wt = 4 * eps4 * (sigma1) ** 12  # for TF to e/p

nTF=0

x=1

defaults = "[ defaults ]\n;nbfunc        comb-rule       gen-pairs\n1               1              no\n"

atomtypes = f"""
[ atomtypes ]
;name    mass    charge  ptype        V           W
NB       1.0      0.0     A       {Vn:.6E}    {Wn:.6E}  ;normal beads(blue)
TF       1.0      0.0     A       {Vr:.6E}    {Wr:.6E}  ;TFs
EN       1.0      0.0     A       {Vn:.6E}    {Wn:.6E}  ;enhancer
PR       1.0      0.0     A       {Vn:.6E}    {Wn:.6E}  ;promoter
OB       1.0      0.0     A       {Vr:.6E}    {Wr:.6E}  ;other beads(grey)
"""

nonbond_params = f"""
[ nonbond_params ]
;i    j    func          V             W
NB    NB      1        {Vn:.6E}    {Wn:.6E}  ;sigma=0.6, eps2={eps2}
TF    TF      1        {Vr:.6E}    {Wr:.6E}  ;sigma=0.4, eps3={eps3}
EN    EN      1        {Vn:.6E}    {Wn:.6E}  ;sigma=0.6, eps2
PR    PR      1        {Vn:.6E}    {Wn:.6E}  ;sigma=0.6, eps2
OB    OB      1        {Vr:.6E}    {Wr:.6E}  ;sigma=0.4, eps3
OB    NB      1        {Vr:.6E}    {Wr:.6E}  ;sigma=0.4, eps3
OB    TF      1        {Vr:.6E}    {Wr:.6E}  ;sigma=0.4, eps3
OB    EN      1        {Vr:.6E}    {Wr:.6E}  ;sigma=0.4, eps3
OB    PR      1        {Vr:.6E}    {Wr:.6E}  ;sigma=0.4, eps3
NB    TF      1        {Vr:.6E}    {Wr:.6E}  ;sigma=0.4, eps3
NB    EN      1        {Vn:.6E}    {Wn:.6E}  ;sigma=0.6, eps2
NB    PR      1        {Vn:.6E}    {Wn:.6E}  ;sigma=0.6, eps2
TF    EN      1        {Vt:.6E}    {Wt:.6E}  ;sigma=0.6, eps4={eps4}
TF    PR      1        {Vt:.6E}    {Wt:.6E}  ;sigma=0.6, eps4
EN    PR      1        {Vs:.6E}    {Ws:.6E}  ;sigma=0.6, eps1={eps1}
"""

moleculetype = """
[ moleculetype ]
;name       nrexcl
Macromolecule   2
"""

no_en = 246
no_pr = 286

atoms = """
[ atoms ]
;nr    type  resnr  residue  atom  cgnr     charge       mass
"""
for i in range(1, 101):
    atoms += "{:>3}\t{:>4}\t{:>3}\t{:>6}\t{:>4}\t{:>3}\t{:>7}\t{:>7}\n".format(
        i, "OB", i, "ASN", "OB", i, 0.0, 1.0)

for i in range(101, no_en):
    atoms += "{:>3}\t{:>4}\t{:>3}\t{:>6}\t{:>4}\t{:>3}\t{:>7}\t{:>7}\n".format(
        i, "NB", i, "ASN", "NB", i, 0.0, 1.0)

atoms += "{:>3}\t{:>4}\t{:>3}\t{:>6}\t{:>4}\t{:>3}\t{:>7}\t{:>7}\t{:>16}\n".format(
    no_en, "EN", no_en, "ASN", "EN", no_en, 0.0, 1.0, ';enhancer')

for i in range(no_en + 1, no_pr):
    atoms += "{:>3}\t{:>4}\t{:>3}\t{:>6}\t{:>4}\t{:>3}\t{:>7}\t{:>7}\n".format(
        i, "NB", i, "ASN", "NB", i, 0.0, 1.0)

atoms += "{:>3}\t{:>4}\t{:>3}\t{:>6}\t{:>4}\t{:>3}\t{:>7}\t{:>7}\t{:>16}\n".format(
    no_pr, "PR", no_pr, "ASN", "PR", no_pr, 0.0, 1.0, ';promoter')

for i in range(no_pr + 1, 434):
    atoms += "{:>3}\t{:>4}\t{:>3}\t{:>6}\t{:>4}\t{:>3}\t{:>7}\t{:>7}\n".format(
        i, "NB", i, "ASN", "NB", i, 0.0, 1.0)

for i in range(434, 534):
    atoms += "{:>3}\t{:>4}\t{:>3}\t{:>6}\t{:>4}\t{:>3}\t{:>7}\t{:>7}\n".format(
        i, "OB", i, "ASN", "OB", i, 0.0, 1.0)

for i in range(534, 534 + nTF):
    atoms += "{:>3}\t{:>4}\t{:>3}\t{:>6}\t{:>4}\t{:>3}\t{:>7}\t{:>7}\n".format(
        i, "TF", i, "ASN", "TF", i, 0.0, 1.0)

bonds = """
[ bonds ]
;ai   aj     func        r0(\sigma)             kb
"""
bonds += "{:>3}\t{:>3}\t{:>5}\t{:>18.6E}\t{:>18.6E}\t{:>20}\n".format(
    101, 433, 6, r0, Kb, ';anchor, and exclude LJ')
for i in range(1, 533):
    bonds += "{:>3}\t{:>3}\t{:>5}\t{:>18.6E}\t{:>18.6E}\n".format(
        i, i + 1, 1, r0, Kb)

exclusions = """
[ exclusions ]
;ai  aj
101  433
"""

angle_restraints = """
[ angle_restraints ]
;ai    aj    ak    al    func       theta0(deg)               Ka            mult
"""
for i in range(1, 532):
    angle_restraints += "{:>3}\t{:>3}\t{:>3}\t{:>3}\t{:>5}\t{:>18}\t{:>18E}\t{:>5}\n".format(
        i + 1, i, i + 1, i + 2, 1, "1.800000E+02", Ka, 1)

system = """
[ system ]
;name
Macromolecule
"""

molecules = """
[ molecules ]
;name           #molec
Macromolecule        1
"""

# Write topology sections to file
with open(f'{x}.top', 'w') as f:
    f.write(defaults)
    f.write(atomtypes)
    f.write(nonbond_params)
    f.write(moleculetype)
    f.write(atoms)
    f.write(bonds)
    f.write(exclusions)
    f.write(angle_restraints)
    f.write(system)
    f.write(molecules)
