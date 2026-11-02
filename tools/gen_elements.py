"""Generate the ELEMENTS array for index.html and sanity-check it.
Fields: z, symbol, name, mass, family, shells (K,L,M,N,O,P,Q).
Period/group are computed from z with the standard layout rules and
written out explicitly so the final array is easy to review."""
import json, sys

ALK, AE, TM, PT, MD, NM, HAL, NG, LAN, ACT = (
    "alkali", "alkaline-earth", "transition", "post-transition", "metalloid",
    "nonmetal", "halogen", "noble-gas", "lanthanide", "actinide")

E = [
(1,"H","Hydrogen","1.008",NM,[1]),
(2,"He","Helium","4.0026",NG,[2]),
(3,"Li","Lithium","6.94",ALK,[2,1]),
(4,"Be","Beryllium","9.0122",AE,[2,2]),
(5,"B","Boron","10.81",MD,[2,3]),
(6,"C","Carbon","12.011",NM,[2,4]),
(7,"N","Nitrogen","14.007",NM,[2,5]),
(8,"O","Oxygen","15.999",NM,[2,6]),
(9,"F","Fluorine","18.998",HAL,[2,7]),
(10,"Ne","Neon","20.180",NG,[2,8]),
(11,"Na","Sodium","22.990",ALK,[2,8,1]),
(12,"Mg","Magnesium","24.305",AE,[2,8,2]),
(13,"Al","Aluminium","26.982",PT,[2,8,3]),
(14,"Si","Silicon","28.085",MD,[2,8,4]),
(15,"P","Phosphorus","30.974",NM,[2,8,5]),
(16,"S","Sulfur","32.06",NM,[2,8,6]),
(17,"Cl","Chlorine","35.45",HAL,[2,8,7]),
(18,"Ar","Argon","39.948",NG,[2,8,8]),
(19,"K","Potassium","39.098",ALK,[2,8,8,1]),
(20,"Ca","Calcium","40.078",AE,[2,8,8,2]),
(21,"Sc","Scandium","44.956",TM,[2,8,9,2]),
(22,"Ti","Titanium","47.867",TM,[2,8,10,2]),
(23,"V","Vanadium","50.942",TM,[2,8,11,2]),
(24,"Cr","Chromium","51.996",TM,[2,8,13,1]),
(25,"Mn","Manganese","54.938",TM,[2,8,13,2]),
(26,"Fe","Iron","55.845",TM,[2,8,14,2]),
(27,"Co","Cobalt","58.933",TM,[2,8,15,2]),
(28,"Ni","Nickel","58.693",TM,[2,8,16,2]),
(29,"Cu","Copper","63.546",TM,[2,8,18,1]),
(30,"Zn","Zinc","65.38",TM,[2,8,18,2]),
(31,"Ga","Gallium","69.723",PT,[2,8,18,3]),
(32,"Ge","Germanium","72.630",MD,[2,8,18,4]),
(33,"As","Arsenic","74.922",MD,[2,8,18,5]),
(34,"Se","Selenium","78.971",NM,[2,8,18,6]),
(35,"Br","Bromine","79.904",HAL,[2,8,18,7]),
(36,"Kr","Krypton","83.798",NG,[2,8,18,8]),
(37,"Rb","Rubidium","85.468",ALK,[2,8,18,8,1]),
(38,"Sr","Strontium","87.62",AE,[2,8,18,8,2]),
(39,"Y","Yttrium","88.906",TM,[2,8,18,9,2]),
(40,"Zr","Zirconium","91.224",TM,[2,8,18,10,2]),
(41,"Nb","Niobium","92.906",TM,[2,8,18,12,1]),
(42,"Mo","Molybdenum","95.95",TM,[2,8,18,13,1]),
(43,"Tc","Technetium","[98]",TM,[2,8,18,13,2]),
(44,"Ru","Ruthenium","101.07",TM,[2,8,18,15,1]),
(45,"Rh","Rhodium","102.91",TM,[2,8,18,16,1]),
(46,"Pd","Palladium","106.42",TM,[2,8,18,18]),
(47,"Ag","Silver","107.87",TM,[2,8,18,18,1]),
(48,"Cd","Cadmium","112.41",TM,[2,8,18,18,2]),
(49,"In","Indium","114.82",PT,[2,8,18,18,3]),
(50,"Sn","Tin","118.71",PT,[2,8,18,18,4]),
(51,"Sb","Antimony","121.76",MD,[2,8,18,18,5]),
(52,"Te","Tellurium","127.60",MD,[2,8,18,18,6]),
(53,"I","Iodine","126.90",HAL,[2,8,18,18,7]),
(54,"Xe","Xenon","131.29",NG,[2,8,18,18,8]),
(55,"Cs","Caesium","132.91",ALK,[2,8,18,18,8,1]),
(56,"Ba","Barium","137.33",AE,[2,8,18,18,8,2]),
(57,"La","Lanthanum","138.91",LAN,[2,8,18,18,9,2]),
(58,"Ce","Cerium","140.12",LAN,[2,8,18,19,9,2]),
(59,"Pr","Praseodymium","140.91",LAN,[2,8,18,21,8,2]),
(60,"Nd","Neodymium","144.24",LAN,[2,8,18,22,8,2]),
(61,"Pm","Promethium","[145]",LAN,[2,8,18,23,8,2]),
(62,"Sm","Samarium","150.36",LAN,[2,8,18,24,8,2]),
(63,"Eu","Europium","151.96",LAN,[2,8,18,25,8,2]),
(64,"Gd","Gadolinium","157.25",LAN,[2,8,18,25,9,2]),
(65,"Tb","Terbium","158.93",LAN,[2,8,18,27,8,2]),
(66,"Dy","Dysprosium","162.50",LAN,[2,8,18,28,8,2]),
(67,"Ho","Holmium","164.93",LAN,[2,8,18,29,8,2]),
(68,"Er","Erbium","167.26",LAN,[2,8,18,30,8,2]),
(69,"Tm","Thulium","168.93",LAN,[2,8,18,31,8,2]),
(70,"Yb","Ytterbium","173.05",LAN,[2,8,18,32,8,2]),
(71,"Lu","Lutetium","174.97",LAN,[2,8,18,32,9,2]),
(72,"Hf","Hafnium","178.49",TM,[2,8,18,32,10,2]),
(73,"Ta","Tantalum","180.95",TM,[2,8,18,32,11,2]),
(74,"W","Tungsten","183.84",TM,[2,8,18,32,12,2]),
(75,"Re","Rhenium","186.21",TM,[2,8,18,32,13,2]),
(76,"Os","Osmium","190.23",TM,[2,8,18,32,14,2]),
(77,"Ir","Iridium","192.22",TM,[2,8,18,32,15,2]),
(78,"Pt","Platinum","195.08",TM,[2,8,18,32,17,1]),
(79,"Au","Gold","196.97",TM,[2,8,18,32,18,1]),
(80,"Hg","Mercury","200.59",TM,[2,8,18,32,18,2]),
(81,"Tl","Thallium","204.38",PT,[2,8,18,32,18,3]),
(82,"Pb","Lead","207.2",PT,[2,8,18,32,18,4]),
(83,"Bi","Bismuth","208.98",PT,[2,8,18,32,18,5]),
(84,"Po","Polonium","[209]",PT,[2,8,18,32,18,6]),
(85,"At","Astatine","[210]",HAL,[2,8,18,32,18,7]),
(86,"Rn","Radon","[222]",NG,[2,8,18,32,18,8]),
(87,"Fr","Francium","[223]",ALK,[2,8,18,32,18,8,1]),
(88,"Ra","Radium","[226]",AE,[2,8,18,32,18,8,2]),
(89,"Ac","Actinium","[227]",ACT,[2,8,18,32,18,9,2]),
(90,"Th","Thorium","232.04",ACT,[2,8,18,32,18,10,2]),
(91,"Pa","Protactinium","231.04",ACT,[2,8,18,32,20,9,2]),
(92,"U","Uranium","238.03",ACT,[2,8,18,32,21,9,2]),
(93,"Np","Neptunium","[237]",ACT,[2,8,18,32,22,9,2]),
(94,"Pu","Plutonium","[244]",ACT,[2,8,18,32,24,8,2]),
(95,"Am","Americium","[243]",ACT,[2,8,18,32,25,8,2]),
(96,"Cm","Curium","[247]",ACT,[2,8,18,32,25,9,2]),
(97,"Bk","Berkelium","[247]",ACT,[2,8,18,32,27,8,2]),
(98,"Cf","Californium","[251]",ACT,[2,8,18,32,28,8,2]),
(99,"Es","Einsteinium","[252]",ACT,[2,8,18,32,29,8,2]),
(100,"Fm","Fermium","[257]",ACT,[2,8,18,32,30,8,2]),
(101,"Md","Mendelevium","[258]",ACT,[2,8,18,32,31,8,2]),
(102,"No","Nobelium","[259]",ACT,[2,8,18,32,32,8,2]),
(103,"Lr","Lawrencium","[266]",ACT,[2,8,18,32,32,8,3]),
(104,"Rf","Rutherfordium","[267]",TM,[2,8,18,32,32,10,2]),
(105,"Db","Dubnium","[268]",TM,[2,8,18,32,32,11,2]),
(106,"Sg","Seaborgium","[269]",TM,[2,8,18,32,32,12,2]),
(107,"Bh","Bohrium","[270]",TM,[2,8,18,32,32,13,2]),
(108,"Hs","Hassium","[269]",TM,[2,8,18,32,32,14,2]),
(109,"Mt","Meitnerium","[278]",TM,[2,8,18,32,32,15,2]),
(110,"Ds","Darmstadtium","[281]",TM,[2,8,18,32,32,16,2]),
(111,"Rg","Roentgenium","[282]",TM,[2,8,18,32,32,17,2]),
(112,"Cn","Copernicium","[285]",TM,[2,8,18,32,32,18,2]),
(113,"Nh","Nihonium","[286]",PT,[2,8,18,32,32,18,3]),
(114,"Fl","Flerovium","[289]",PT,[2,8,18,32,32,18,4]),
(115,"Mc","Moscovium","[290]",PT,[2,8,18,32,32,18,5]),
(116,"Lv","Livermorium","[293]",PT,[2,8,18,32,32,18,6]),
(117,"Ts","Tennessine","[294]",HAL,[2,8,18,32,32,18,7]),
(118,"Og","Oganesson","[294]",NG,[2,8,18,32,32,18,8]),
]

GAS = {"H","He","N","O","F","Ne","Cl","Ar","Kr","Xe","Rn"}
LIQ = {"Br","Hg"}

def period_group(z):
    ends = [2,10,18,36,54,86,118]
    p = next(i+1 for i,e in enumerate(ends) if z <= e)
    start = [0,2,10,18,36,54,86][p-1] + 1
    k = z - start  # 0-based index in period
    if p == 1:
        return p, 1 if z == 1 else 18
    if p in (2,3):
        return p, k+1 if k < 2 else k+11
    if p in (4,5):
        return p, k+1
    if k < 2:
        return p, k+1
    if k < 17:            # La..Lu / Ac..Lr  (f-block series, no group number)
        return p, None
    return p, k-14+1

assert len(E) == 118
lines = []
for i,(z,s,n,m,f,sh) in enumerate(E):
    assert z == i+1, z
    assert sum(sh) == z, (s, sum(sh))
    p, g = period_group(z)
    assert len(sh) == p or s == "Pd", (s, len(sh), p)
    if z >= 104: st = "unknown"
    elif z >= 100: st = "solid*"
    elif s in GAS: st = "gas"
    elif s in LIQ: st = "liquid"
    else: st = "solid"
    lines.append('  {z:%d, sym:%s, name:%s, mass:%s, family:%s, period:%d, group:%s, shells:[%s], state:%s},'
                 % (z, json.dumps(s), json.dumps(n), json.dumps(m), json.dumps(f), p,
                    "null" if g is None else g, ",".join(map(str,sh)), json.dumps(st)))

# spot checks against well-known positions
pg = {e[1]: period_group(e[0]) for e in E}
for sym, want in {"Na":(3,1),"Cl":(3,17),"Fe":(4,8),"Au":(6,11),"Hf":(6,4),"Rn":(6,18),
                  "Og":(7,18),"Al":(3,13),"Ce":(6,None),"Lu":(6,None),"Rf":(7,4)}.items():
    assert pg[sym] == want, (sym, pg[sym], want)
sys.stdout.write("\n".join(lines) + "\n")
