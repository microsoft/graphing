from geopy.geocoders import Nominatim
import numpy as np
import networkx as nx
from PIL import Image, ImageDraw, ImageFont


ukr_grph_ts = {
        'staging-1': {'chernihiv': 5},
        'chernihiv': {'brovary': 4},
        'brovary': {'kyiv': 1},
        'boryspil': {'kyiv': 1.3, 'pereiaslav': 2.3},
        'pereiaslav': {'boryspil': 3.3, 'kremenchuk': 2.5},
        'kremenchuk': {'cherkasy': 2.3, 'pereiaslav': 3.1, 'poltava': 2.6, 'dnipro': 2.4, 'kropyvnytskyi': 2.0},
        'cherkasy': {'kyiv': 3.2, 'kremenchuk': 2.2},
        'bila_tserkva': {'kyiv': 3.1, 'uman': 2.5},
        'irpin': {'kyiv': 5.0, 'zhytomyr': 2.0},
        'kyiv': {'brovary': 1.0, 'irpin': 1.0, 'bila_tserkva': 1.8, 'cherkasy': 2.0, 'boryspil': 1.4, 'pyriatyn': 2.1},
        'uman': {'vinnytsia': 2.0, 'odesa': 2.2, 'kropyvnytskyi': 2.1, 'bila_tserkva': 2.1},
        'vinnytsia': {'zhytomyr': 1.7, 'uman': 1.5, 'odesa': 2.1},
        'odesa': {'vinnytsia': 2.4, 'uman': 2.1, 'mykolaiv': 1.8},
        'kropyvnytskyi': {'kryvyi_rih': 1.2, 'kremenchuk': 1.5, 'uman': 2.2, 'mykolaiv': 1.8},
        'dnipro': {'kryvyi_rih': 1.9, 'zaporizhzhia': 1.1, 'pavlohrad': 1.6, 'kharkiv': 2.1, 'kremenchuk': 2.3},
        'staging-2': {'sumy': 1.4},
        'sumy': {'kyiv': 4.5, 'kharkiv': 2.4},
        'staging-3': {'kharkiv': 0.8},
        'kharkiv': {'sumy': 1.9, 'okhtyrka': 1.5, 'poltava': 1.5, 'dnipro': 2.8, 'luhansk': 2.2},
        'staging-4': {'luhansk': 0.4},
        'staging-5': {'donetsk': 0.5},
        'luhansk': {'kharkiv': 1.7, 'donetsk': 0.8},
        'donetsk': {'mariupol': 1.4, 'zaporizhzhia': 1.8, 'pokrovsk': 1.1, 'luhansk': 2.0},
        'mariupol': {'berdyansk': 0.4, 'donetsk': 0.7},
        'berdyansk': {'mariupol': 0.4, 'melitopol': 0.5, 'zaporizhzhia': 1.4},
        'staging-6': {'melitopol': 0.1},
        'staging-7': {'kherson': 0.3},
        'kherson': {'mykolaiv': 1.0, 'melitopol': 1.3},
        'mykolaiv': {'odesa': 1.3, 'kherson': 1.1, 'kryvyi_rih': 0.9, 'kropyvnytskyi': 0.85},
        'poltava': {'lubny': 2, 'kremenchuk': 2.5, 'kharkiv': 2.2},
        'lubny': {'pyriatyn': 1.4, 'poltava': 1.8},
        'zhytomyr': {'vinnytsia': 2.1, 'irpin': 1.6},
        'pyriatyn': {'okhtyrka': 1.7, 'kyiv': 2.8, 'lubny': 0.9},
        'okhtyrka': {'pyriatyn': 2.1, 'kharkiv': 2.2},
        'kryvyi_rih': {'mykolaiv': 1.8, 'kropyvnytskyi': 0.9, 'dnipro': 2.4},
        'zaporizhzhia': {'dnipro': 0.8, 'donetsk': 2.1, 'berdyansk': 1.8, 'melitopol': 1.5},
        'pavlohrad': {'dnipro': 2.1, 'pokrovsk': 0.8},
        'pokrovsk': {'pavlohrad': 0.8, 'donetsk': 0.7},
        'melitopol': {'berdyansk': 0.7, 'zaporizhzhia': 1.1, 'kherson': 2.3}
        }

geolocator = Nominatim(user_agent="MyApp")

coord = {
        'staging-1': (362, 47),
        'staging-2': (908, 140),
        'staging-3': (1130, 260),
        'staging-4': (1374, 672),
        'staging-5': (1260, 824),
        'staging-6': (828, 993),
        'staging-7': (692, 1013),
        'chernihiv': (383, 172),
        'brovary': (295, 273),
        'kyiv': (258,315),
        'irpin': (218, 314),
        'zhytomyr': (110,346),
        'vinnytsia': (105,542),
        'odesa': (262,869),
        'mykolaiv': (494,781),
        'kherson': (623,878),
        'kryvyi_rih': (666,733),
        'kropyvnytskyi': (583,662),
        'kremenchuk': (693, 535),
        'pereiaslav': (508,444),
        'cherkasy': (442,479),
        'boryspil': (346,364),
        'pokrovsk': (1070, 692),
        'uman': (260,654),
        'luhansk': (1265,661),
        'donetsk': (1076,773),
        'mariupol': (1032,868),
        'berdyansk': (949,865),
        'sumy': (817,252),
        'kharkiv': (1049,382),
        'poltava': (827,415),
        'melitopol': (837,862),
        'zaporizhzhia': (838,718),
        'dnipro': (838, 614),
        'pavlohrad': (996,629),
        'kremanchuk': (694,536),
        'pyriatyn': (560,329),
        'lubny': (666,369),
        'bila_tserkva': (250,479),
        'okhtyrka': (815,348)
        }


posns = {}
x = []
y1 = []
y2 = []
for k in ukr_grph_ts.keys():
    if 'staging' not in k:
        location = geolocator.geocode(k)
        lati, longi = location.latitude, location.longitude
        posns[k] = (lati, longi)
        if k in coord:
            x.append([1, lati, longi])
            y1.append(coord[k][0])
            y2.append(coord[k][1])

x = np.array(x)
y1 = np.array(y1)
y2 = np.array(y2)

beta1 = np.linalg.solve(np.dot(x.T,x),np.dot(x.T,y1))
beta2 = np.linalg.solve(np.dot(x.T,x),np.dot(x.T,y2))

for k in ukr_grph_ts.keys():
    if k not in coord:
        lati, longi = posns[k]
        x_ht = np.array([1, lati, longi])
        y1 = np.dot(beta1, x_ht)
        y2 = np.dot(beta2, x_ht)
        coord[k] = (y1, y2)


im = Image.new("RGB", (1500, 1500), (0, 0, 0))
draw = ImageDraw.Draw(im, "RGBA")

for k in coord.keys():
    pt = coord[k]
    draw.ellipse(
        (pt[0] - 8, pt[1] - 8, pt[0] + 8, pt[1] + 8),
        fill=(255, 0, 0, 150),
        outline=(0, 0, 0),
    )
    font = ImageFont.truetype("Arial.ttf", 20)
    draw.text((pt[0] + 2, pt[1] + 2), k, "orange", font=font)

for k in ukr_grph_ts.keys():
    for kk in ukr_grph_ts[k].keys():
        pt1 = coord[k]
        pt2 = coord[kk]
        draw.line((pt1[0], pt1[1], pt2[0], pt2[1]), (102, 255, 51, 120), width=2)


G = nx.DiGraph()

for k in ukr_grph_ts.keys():
    for kk in ukr_grph_ts[k].keys():
        G.add_edge(k, kk, weight=int(100*ukr_grph_ts[k][kk]), capacity=720)

G.add_edge("s", 'staging-1', weight=0, capacity=np.inf)
G.add_edge("s", 'staging-2', weight=0, capacity=np.inf)
G.add_edge("s", 'staging-3', weight=0, capacity=np.inf)
G.add_edge("s", 'staging-4', weight=0, capacity=np.inf)
G.add_edge("s", 'staging-5', weight=0, capacity=np.inf)
G.add_edge("s", 'staging-6', weight=0, capacity=np.inf)
G.add_edge("s", 'staging-7', weight=0, capacity=np.inf)

G.add_node("s", demand=-5000)
G.add_node("kyiv", demand=3000)
G.add_node("kharkiv", demand=1000)
G.add_node("mariupol", demand=500)
G.add_node("odesa", demand=500)

flowDict = nx.min_cost_flow(G)

for k in flowDict.keys():
    if k != 's':
        for kk in flowDict[k].keys():
            if flowDict[k][kk]>0:
                pt1 = coord[k]
                pt2 = coord[kk]
                draw.line((pt1[0], pt1[1], pt2[0], pt2[1]), (255, 10, 51, 80), width=int(30/720*flowDict[k][kk]))

im.show()
