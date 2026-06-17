import math
from build123d import *
from ocp_vscode import show
from OCP.BRepOffsetAPI import BRepOffsetAPI_ThruSections
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakePolygon
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCP.BRepFilletAPI import BRepFilletAPI_MakeFillet
from OCP.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCP.gp import gp_Pnt, gp_Dir, gp_Ax2, gp_Circ, gp_Vec

# 1. First profile (Extrudes from 0 to 25mm)
points_1 = [
    (197.7344, -114.0234, 0.0), (200.9766, -113.8477, 0.0), (204.1406, -113.3398, 0.0),
    (207.2656, -112.4805, 0.0), (210.2344, -111.3086, 0.0), (213.0859, -109.8047, 0.0),
    (215.7812, -108.0078, 0.0), (218.2422, -105.9375, 0.0), (222.9688, -101.3281, 0.0),
    (227.4609, -96.5234, 0.0), (231.7188, -91.5039, 0.0), (235.7812, -86.2891, 0.0),
    (239.5703, -80.8984, 0.0), (243.125, -75.3516, 0.0), (246.4062, -69.6289, 0.0),
    (249.8828, -62.9102, 0.0), (252.8906, -56.1914, 0.0), (255.5859, -49.3555, 0.0),
    (257.8906, -42.3828, 0.0), (259.8828, -35.293, 0.0), (261.4844, -28.125, 0.0),
    (262.7344, -20.8789, 0.0), (263.5938, -13.5742, 0.0), (264.1016, -6.2305, 0.0),
    (264.2188, 1.1133, 0.0), (263.9844, 8.457, 0.0), (263.3594, 15.8008, 0.0),
    (262.3828, 23.0859, 0.0), (261.0156, 30.3125, 0.0), (259.2969, 37.4609, 0.0),
    (257.2266, 44.5117, 0.0), (254.8047, 51.4453, 0.0), (251.9922, 58.2422, 0.0),
    (248.8672, 64.9023, 0.0), (245.4297, 71.3867, 0.0), (241.6406, 77.6953, 0.0),
    (237.5391, 83.8086, 0.0), (233.1641, 89.6875, 0.0), (228.4375, 95.3516, 0.0),
    (223.4766, 100.7617, 0.0), (218.2422, 105.918, 0.0), (215.7812, 107.9883, 0.0),
    (213.0859, 109.7852, 0.0), (210.2344, 111.2891, 0.0), (207.2656, 112.4609, 0.0),
    (204.1406, 113.3203, 0.0), (200.9766, 113.8281, 0.0), (197.7344, 114.0039, 0.0),
    (190.2344, 114.0039, 0.0), (186.9141, 113.8281, 0.0), (183.6328, 113.2617, 0.0),
    (180.4297, 112.3633, 0.0), (177.3438, 111.0938, 0.0), (174.4141, 109.5117, 0.0),
    (171.7188, 107.5977, 0.0), (169.2188, 105.4102, 0.0), (166.9531, 102.9492, 0.0),
    (165.0, 100.2539, 0.0), (163.3594, 97.3633, 0.0), (162.0703, 94.3164, 0.0),
    (161.0938, 91.1328, 0.0), (160.4688, 87.8711, 0.0), (160.2344, 84.5508, 0.0),
    (160.3516, 81.2305, 0.0), (160.8594, 77.9297, 0.0), (161.7188, 74.7266, 0.0),
    (162.8906, 71.6211, 0.0), (164.4531, 68.6719, 0.0), (166.2891, 65.918, 0.0),
    (168.4375, 63.3789, 0.0), (174.7656, 57.5586, 0.0), (178.4375, 53.7891, 0.0),
    (170.8594, 61.0938, 0.0), (181.8359, 49.7852, 0.0), (184.9609, 45.5664, 0.0),
    (187.8125, 41.1523, 0.0), (190.3906, 36.543, 0.0), (192.6172, 31.7969, 0.0),
    (194.5703, 26.8945, 0.0), (196.1719, 21.8945, 0.0), (197.4609, 16.7969, 0.0),
    (198.3594, 11.6211, 0.0), (198.9844, 6.3867, 0.0), (199.2188, 1.1328, 0.0),
    (199.1797, -2.3242, 0.0), (198.8281, -7.9102, 0.0), (198.0859, -13.4766, 0.0),
    (196.9531, -18.9453, 0.0), (195.4297, -24.3359, 0.0), (193.5547, -29.6094, 0.0),
    (191.2891, -34.7461, 0.0), (188.6719, -39.707, 0.0), (185.7422, -44.4531, 0.0),
    (182.4609, -49.0039, 0.0), (178.9062, -53.3008, 0.0), (175.0, -57.3438, 0.0),
    (170.8594, -61.1133, 0.0), (168.4375, -63.3984, 0.0), (166.2891, -65.9375, 0.0),
    (164.4531, -68.6914, 0.0), (162.8906, -71.6406, 0.0), (161.7188, -74.7461, 0.0),
    (160.8594, -77.9688, 0.0), (160.3516, -81.25, 0.0), (160.2344, -84.5703, 0.0),
    (160.4688, -87.8906, 0.0), (161.0938, -91.1523, 0.0), (162.0703, -94.3359, 0.0),
    (163.3594, -97.4023, 0.0), (165.0, -100.293, 0.0), (166.9531, -102.9688, 0.0),
    (169.2188, -105.4297, 0.0), (171.7188, -107.6367, 0.0), (174.4141, -109.5312, 0.0),
    (177.3438, -111.1328, 0.0), (180.4297, -112.3828, 0.0), (183.6328, -113.3008, 0.0),
    (186.9141, -113.8477, 0.0), (190.2344, -114.0234, 0.0),
]

# 2. Second profile (Extrudes from 25 to 30mm)
points_2 = [
    (169.2578, -105.4688, 25.0), (166.9922, -103.0273, 25.0), (165.0391, -100.332, 25.0),
    (163.3984, -97.4414, 25.0), (162.0703, -94.375, 25.0), (161.0938, -91.1914, 25.0),
    (160.4688, -87.9297, 25.0), (160.2344, -84.6094, 25.0), (160.8594, -77.9883, 25.0),
    (161.6797, -74.7656, 25.0), (162.8906, -71.6602, 25.0), (160.3516, -81.2695, 25.0),
    (164.4531, -68.7109, 25.0), (166.2891, -65.9375, 25.0), (168.4375, -63.3984, 25.0),
    (170.8594, -61.1133, 25.0), (175.0, -57.3828, 25.0), (178.8281, -53.3594, 25.0),
    (182.3828, -49.1016, 25.0), (185.6641, -44.5898, 25.0), (188.5938, -39.8633, 25.0),
    (191.2109, -34.9414, 25.0), (193.4375, -29.8633, 25.0), (195.3516, -24.6289, 25.0),
    (196.875, -19.2969, 25.0), (198.0078, -13.8477, 25.0), (198.7891, -8.3398, 25.0),
    (199.1797, -2.793, 25.0), (199.1797, 2.7734, 25.0), (198.7891, 8.3203, 25.0),
    (198.0078, 13.8281, 25.0), (196.875, 19.2578, 25.0), (195.3516, 24.6094, 25.0),
    (193.4375, 29.8438, 25.0), (191.2109, 34.9219, 25.0), (188.5938, 39.8438, 25.0),
    (185.6641, 44.5703, 25.0), (182.3828, 49.082, 25.0), (178.8281, 53.3398, 25.0),
    (175.0, 57.3633, 25.0), (170.8594, 61.0938, 25.0), (168.4375, 63.3789, 25.0),
    (166.2891, 65.918, 25.0), (164.4531, 68.6914, 25.0), (162.8906, 71.6406, 25.0),
    (161.6797, 74.7461, 25.0), (160.8594, 77.9688, 25.0), (160.3516, 81.25, 25.0),
    (160.2344, 84.5898, 25.0), (160.4688, 87.9102, 25.0), (161.0938, 91.1719, 25.0),
    (162.0703, 94.3555, 25.0), (163.3984, 97.4219, 25.0), (165.0391, 100.3125, 25.0),
    (166.9922, 102.9883, 25.0), (169.2578, 105.4492, 25.0), (175.2734, 102.3828, 25.0),
    (181.0938, 98.9648, 25.0), (186.7188, 95.2344, 25.0), (192.1094, 91.1719, 25.0),
    (197.2656, 86.7969, 25.0), (202.1484, 82.1484, 25.0), (206.7578, 77.2266, 25.0),
    (211.0547, 72.0312, 25.0), (215.0781, 66.6016, 25.0), (218.7891, 60.957, 25.0),
    (222.1094, 55.0977, 25.0), (225.1562, 49.043, 25.0), (227.8125, 42.8516, 25.0),
    (230.0781, 36.5039, 25.0), (232.0312, 30.0195, 25.0), (233.5547, 23.457, 25.0),
    (234.7266, 16.8164, 25.0), (235.8984, 3.3594, 25.0), (235.8984, -3.3789, 25.0),
    (235.5078, -10.1172, 25.0), (235.5078, 10.0977, 25.0), (233.5547, -23.4766, 25.0),
    (232.0312, -30.0586, 25.0), (234.7266, -16.8359, 25.0), (230.0781, -36.5234, 25.0),
    (227.8125, -42.8711, 25.0), (225.1562, -49.082, 25.0), (222.1094, -55.1172, 25.0),
    (218.7891, -60.9766, 25.0), (215.0781, -66.6211, 25.0), (211.0547, -72.0508, 25.0),
    (206.7578, -77.2461, 25.0), (202.1484, -82.168, 25.0), (197.2656, -86.8359, 25.0),
    (192.1094, -91.1914, 25.0), (186.7188, -95.2539, 25.0), (181.0938, -99.0039, 25.0),
    (175.2734, -102.4023, 25.0),
]

# 3. Third profile (Extrudes from 30 to 397.5mm)
points_3 = [
    (169.2578, 105.4492, 30.0), (175.2734, 102.3828, 30.0), (181.0938, 98.9648, 30.0),
    (186.7188, 95.2344, 30.0), (192.1094, 91.1719, 30.0), (197.2656, 86.7969, 30.0),
    (202.1484, 82.1484, 30.0), (206.7578, 77.2266, 30.0), (211.0547, 72.0312, 30.0),
    (215.0781, 66.6016, 30.0), (218.7891, 60.957, 30.0), (222.1094, 55.0977, 30.0),
    (225.1562, 49.043, 30.0), (227.8125, 42.8516, 30.0), (230.0781, 36.5039, 30.0),
    (232.0312, 30.0195, 30.0), (233.5547, 23.457, 30.0), (234.7266, 16.8164, 30.0),
    (235.5078, 10.0977, 30.0), (235.8984, 3.3594, 30.0), (235.8984, -3.3789, 30.0),
    (235.5078, -10.1172, 30.0), (234.7266, -16.8359, 30.0), (233.5547, -23.4766, 30.0),
    (232.0312, -30.0586, 30.0), (230.0781, -36.5234, 30.0), (227.8125, -42.8711, 30.0),
    (225.1562, -49.082, 30.0), (222.1094, -55.1172, 30.0), (218.7891, -60.9766, 30.0),
    (215.0781, -66.6211, 30.0), (211.0547, -72.0508, 30.0), (206.7578, -77.2461, 30.0),
    (202.1484, -82.168, 30.0), (197.2656, -86.8359, 30.0), (192.1094, -91.1914, 30.0),
    (186.7188, -95.2539, 30.0), (181.0938, -99.0039, 30.0), (175.2734, -102.4023, 30.0),
    (169.2578, -105.4688, 30.0), (163.2031, -108.1445, 30.0), (156.9922, -110.4688, 30.0),
    (150.6641, -112.4219, 30.0), (144.2188, -114.0234, 30.0), (137.7344, -115.2539, 30.0),
    (131.1719, -116.1328, 30.0), (124.5703, -116.6211, 30.0), (117.9297, -116.7383, 30.0),
    (111.3281, -116.4648, 30.0), (104.7266, -115.8398, 30.0), (98.2031, -114.8242, 30.0),
    (91.7188, -113.4375, 30.0), (85.3125, -111.6992, 30.0), (82.6562, -110.8594, 30.1546),
    (79.9219, -109.9219, 30.0368), (77.1875, -108.9062, 30.0), (71.2109, -106.4062, 30.0),
    (65.3516, -103.5742, 30.0), (59.6875, -100.4102, 30.0), (54.2188, -96.9531, 30.0),
    (48.9062, -93.1836, 30.0), (43.8672, -89.1406, 30.0), (39.0234, -84.8047, 30.0),
    (34.4141, -80.2148, 30.0), (30.1172, -75.3906, 30.0), (26.0547, -70.3125, 30.0),
    (22.3047, -65.0391, 30.0), (18.8281, -59.5508, 30.0), (15.6641, -53.8672, 30.0),
    (12.8516, -48.0469, 30.0), (10.3516, -42.0508, 30.0), (9.3359, -39.3164, 30.0368),
    (8.3984, -36.582, 30.1546), (7.5391, -33.9258, 30.0), (5.7812, -27.4219, 30.0),
    (4.375, -20.8398, 30.0), (3.3594, -14.1797, 30.0), (2.7344, -7.4609, 30.0),
    (2.5, -0.7422, 30.0), (2.6562, 5.9961, 30.0), (3.2031, 12.7148, 30.0),
    (4.1406, 19.375, 30.0), (5.4297, 25.9961, 30.0), (7.1094, 32.5, 30.0),
    (9.1797, 38.9258, 30.0), (11.6016, 45.1953, 30.0), (14.4141, 51.3281, 30.0),
    (17.5391, 57.3047, 30.0), (21.0156, 63.0664, 30.0), (24.8047, 68.6328, 30.0),
    (28.9453, 73.9648, 30.0), (33.3594, 79.043, 30.0), (38.0469, 83.8672, 30.0),
    (43.0078, 88.3984, 30.0), (48.2422, 92.6562, 30.0), (53.7109, 96.6016, 30.0),
    (59.4141, 100.2148, 30.0), (65.2734, 103.4961, 30.0), (71.3281, 106.4453, 30.0),
    (77.5391, 109.0234, 30.0), (83.9062, 111.25, 30.0), (90.3906, 113.1055, 30.0),
    (96.9531, 114.5703, 30.0), (103.5938, 115.6641, 30.0), (110.3125, 116.3672, 30.0),
    (117.0312, 116.6992, 30.0), (123.75, 116.6211, 30.0), (130.5078, 116.1719, 30.0),
    (137.1875, 115.332, 30.0), (143.7891, 114.1016, 30.0), (150.3516, 112.5, 30.0),
    (156.7578, 110.5078, 30.0), (163.0859, 108.1641, 30.0),
]

# 4. Cutting v1 coordinates (Depth 370.0mm cut)
points_cut_v1 = [
    (33.1641, -36.582, 397.5), (82.6562, -86.0938, 397.5), (110.9375, -57.793, 397.5),
    (61.4453, -8.3008, 397.5), (145.3906, 1.8945, 397.5), (145.4297, -1.3086, 397.5),
    (145.0781, -4.4727, 397.5), (144.375, -7.5977, 397.5), (143.2422, -10.5859, 397.5),
    (141.7969, -13.4375, 397.5), (140.0, -16.0742, 397.5), (137.8906, -18.4766, 397.5),
    (135.5078, -20.6055, 397.5), (132.8906, -22.4414, 397.5), (130.0391, -23.9258, 397.5),
    (127.0703, -25.0586, 397.5), (120.7812, -26.2109, 397.5), (117.5781, -26.2109, 397.5),
    (114.4141, -25.8203, 397.5), (111.3281, -25.0391, 397.5), (108.3203, -23.8867, 397.5),
    (123.9453, -25.8398, 397.5), (105.5078, -22.3828, 397.5), (102.8906, -20.5664, 397.5),
    (98.3984, -16.0156, 397.5), (100.5078, -18.418, 397.5), (96.6406, -13.3594, 397.5),
    (95.1562, -10.5078, 397.5), (94.0625, -7.5195, 397.5), (93.3594, -4.3945, 397.5),
    (93.0078, -1.2109, 397.5), (93.0469, 1.9727, 397.5), (93.4766, 5.1367, 397.5),
    (94.2969, 8.2422, 397.5), (95.5078, 11.1914, 397.5), (97.0312, 14.0039, 397.5),
    (98.9062, 16.6016, 397.5), (101.0547, 18.9453, 397.5), (103.5156, 21.0156, 397.5),
    (106.1719, 22.7734, 397.5), (109.0625, 24.1797, 397.5), (112.0703, 25.2344, 397.5),
    (115.1953, 25.918, 397.5), (118.3594, 26.2305, 397.5), (121.5625, 26.1328, 397.5),
]

# 5. Cutting v2 coordinates (Depth 48.5mm pocket cut)
points_cut_v2 = [
    (151.9922, -54.668, 397.5), (152.9688, -57.1094, 397.5), (154.2578, -59.375, 397.5),
    (155.8984, -61.4062, 397.5), (157.8125, -63.1836, 397.5), (162.3438, -65.8008, 397.5),
    (159.9609, -64.668, 397.5), (164.8438, -66.5625, 397.5), (167.4219, -66.9531, 397.5),
    (170.0391, -66.9531, 397.5), (172.6172, -66.5625, 397.5), (175.1172, -65.8008, 397.5),
    (177.4609, -64.668, 397.5), (179.6484, -63.1836, 397.5), (181.5625, -61.4062, 397.5),
    (183.2031, -59.375, 397.5), (184.4922, -57.1094, 397.5), (185.4297, -54.668, 397.5),
    (186.0156, -52.1094, 397.5), (186.2109, -49.5117, 397.5), (186.0156, -46.8945, 397.5),
    (185.4297, -44.3555, 397.5), (184.4922, -41.9141, 397.5), (183.2031, -39.6484, 397.5),
    (181.5625, -37.5977, 397.5), (179.6484, -35.8203, 397.5), (177.4609, -34.3555, 397.5),
    (175.1172, -33.2227, 397.5), (172.6172, -32.4414, 397.5), (170.0391, -32.0508, 397.5),
    (167.4219, -32.0508, 397.5), (164.8438, -32.4414, 397.5), (162.3438, -33.2227, 397.5),
    (159.9609, -34.3555, 397.5), (157.8125, -35.8203, 397.5), (155.8984, -37.5977, 397.5),
    (154.2578, -39.6484, 397.5), (152.9688, -41.9141, 397.5), (151.9922, -44.3555, 397.5),
    (151.4062, -46.8945, 397.5), (151.2109, -49.5117, 397.5), (151.4062, -52.1094, 397.5),
    (56.9141, 37.5781, 397.5), (58.8281, 35.8008, 397.5), (60.9766, 34.3359, 397.5),
    (63.3203, 33.2031, 397.5), (65.8203, 32.4219, 397.5), (68.4375, 32.0312, 397.5),
    (71.0547, 32.0312, 397.5), (73.6328, 32.4219, 397.5), (76.1328, 33.2031, 397.5),
    (78.4766, 34.3359, 397.5), (80.625, 35.8008, 397.5), (82.5781, 37.5781, 397.5),
    (84.1797, 39.6289, 397.5), (85.5078, 41.8945, 397.5), (86.4453, 44.3359, 397.5),
    (87.0312, 46.875, 397.5), (87.2266, 49.4922, 397.5), (87.0312, 52.0898, 397.5),
    (86.4453, 54.6484, 397.5), (85.5078, 57.0703, 397.5), (84.1797, 59.3359, 397.5),
    (82.5781, 61.3867, 397.5), (80.625, 63.1641, 397.5), (78.4766, 64.6484, 397.5),
    (76.1328, 65.7812, 397.5), (73.6328, 66.543, 397.5), (71.0547, 66.9336, 397.5),
    (68.4375, 66.9336, 397.5), (65.8203, 66.543, 397.5), (63.3203, 65.7812, 397.5),
    (60.9766, 64.6484, 397.5), (56.9141, 61.3867, 397.5), (55.2734, 59.3359, 397.5),
    (53.9453, 57.0703, 397.5), (53.0078, 54.6484, 397.5), (52.4219, 52.0898, 397.5),
    (52.2266, 49.4922, 397.5), (52.4219, 46.875, 397.5), (53.0078, 44.3359, 397.5),
    (53.9453, 41.8945, 397.5), (55.2734, 39.6289, 397.5), (58.8281, 63.1641, 397.5),
]

# 6. Separate Solid profile coordinates (Slanted Body)
points_cut_v3 = [
    (167.4609, 1.2695, 397.5), (120.5078, 48.2031, 397.5), (120.5078, 48.2031, 100.0),
    (132.2266, 36.4648, 71.25), (155.7031, 13.0078, 71.25), (167.4609, 1.2695, 100.0),
]

# 7. Cutting v4 coordinates
points_cut_v4 = [
    (136.6406, -40.918, 322.5),
    (145.2344, -72.9883, 322.5),
    (174.8828, -102.6172, 322.5),
    (188.582, -116.3073, 322.5),
    (239.1073, -65.7487, 322.5),
    (221.8359, -55.6641, 322.5),
    (192.1875, -26.0352, 322.5),
    (160.1172, -17.4414, 322.5),
]

# 8. Cutting v5 coordinates (depth of 222.5mm)
points_cut_v5 = [
    (156.3672, -37.1289, 322.5), (154.6484, -39.1211, 322.5), (153.2422, -41.3281, 322.5),
    (152.2266, -43.7305, 322.5), (151.5234, -46.25, 322.5), (151.25, -48.8477, 322.5),
    (151.3281, -51.4648, 322.5), (151.8359, -54.043, 322.5), (152.6953, -56.5039, 322.5),
    (155.4688, -60.918, 322.5), (153.9062, -58.8281, 322.5), (157.3047, -62.7734, 322.5),
    (159.4141, -64.3359, 322.5), (161.7188, -65.5469, 322.5), (164.1797, -66.4062, 322.5),
    (169.375, -66.9922, 322.5), (166.7578, -66.8945, 322.5), (171.9922, -66.6992, 322.5),
    (174.4922, -66.0352, 322.5), (176.9141, -64.9805, 322.5), (179.1016, -63.5938, 322.5),
    (181.0938, -61.875, 322.5), (182.8125, -59.9023, 322.5), (184.1797, -57.6953, 322.5),
    (185.2344, -55.293, 322.5), (185.9375, -52.7539, 322.5), (186.2109, -49.5117, 322.5),
    (186.1328, -47.5586, 322.5), (185.625, -44.9805, 322.5), (184.7656, -42.5195, 322.5),
    (183.5547, -40.1953, 322.5), (181.9922, -38.0859, 322.5), (180.1562, -36.25, 322.5),
    (178.0469, -34.6875, 322.5), (175.7422, -33.4766, 322.5), (173.2422, -32.5977, 322.5),
    (170.7031, -32.1289, 322.5), (168.0859, -32.0312, 322.5), (165.4688, -32.3242, 322.5),
    (162.9297, -32.9883, 322.5), (160.5469, -34.043, 322.5), (158.3203, -35.4297, 322.5),
]


def sort_and_sanitize_points(pts):
    """
    Spatially sorts a list of 3D coordinates into a continuous,
    non-self-intersecting 2D boundary path using a Nearest-Neighbor algorithm.
    """
    if not pts:
        return []
    coords = []
    for p in pts:
        c = (p[0], p[1])
        if not coords or c != coords[-1]:
            coords.append(c)
    if len(coords) > 1 and coords[0] == coords[-1]:
        coords.pop()
    if not coords:
        return []
    unvisited = list(coords)
    sorted_coords = [unvisited.pop(0)]
    while unvisited:
        current = sorted_coords[-1]
        nearest_idx = min(
            range(len(unvisited)),
            key=lambda i: (unvisited[i][0] - current[0]) ** 2
            + (unvisited[i][1] - current[1]) ** 2,
        )
        sorted_coords.append(unvisited.pop(nearest_idx))
    return sorted_coords


# Clean and sort main extrude profiles
plane_points_1 = sort_and_sanitize_points(points_1)
plane_points_2 = sort_and_sanitize_points(points_2)
plane_points_3 = sort_and_sanitize_points(points_3)

# Separate the cutting profiles (v1): First 4 points are rectangle, remainder are circle
points_cut_v1_rect = points_cut_v1[:4]
points_cut_v1_circ = points_cut_v1[4:]
plane_points_cut_v1_rect = sort_and_sanitize_points(points_cut_v1_rect)
plane_points_cut_v1_circ = sort_and_sanitize_points(points_cut_v1_circ)

# Separate the cutting profiles (v2): First 42 points are Pocket 1; remainder are Pocket 2
points_cut_v2_1 = points_cut_v2[:42]
points_cut_v2_2 = points_cut_v2[42:]
plane_points_cut_v2_1 = sort_and_sanitize_points(points_cut_v2_1)
plane_points_cut_v2_2 = sort_and_sanitize_points(points_cut_v2_2)

# Sort Cut v4 octagonal points
plane_points_cut_v4 = sort_and_sanitize_points(points_cut_v4)

# Sort Cut v5 circular points
plane_points_cut_v5 = sort_and_sanitize_points(points_cut_v5)

# --- Construct the slanted sketch plane ---
cut_plane = Plane(
    origin=(120.5078, 48.2031, 0.0),
    x_dir=(1.0, -1.0, 0.0),
    z_dir=(-1.0, -1.0, 0.0)
)

# Project the 3D coordinates into local 2D sketch coordinate space (U, V)
u_dir = (1.0, -1.0, 0.0)
u_len = math.sqrt(u_dir[0]**2 + u_dir[1]**2 + u_dir[2]**2)
u_unit = (u_dir[0]/u_len, u_dir[1]/u_len, u_dir[2]/u_len)

plane_points_cut_v3 = []
for p in points_cut_v3:
    dx = p[0] - 120.5078
    dy = p[1] - 48.2031
    u = dx * u_unit[0] + dy * u_unit[1]
    v = p[2]
    plane_points_cut_v3.append((u, v))

# Extrude profile from extrude.txt
plane_points_extrude = [
    (61.1719, 6.0156), (60.8594, 1.2305), (60.9375, -3.5547), (61.4453, -8.3008),
    (110.9375, -57.793), (115.7031, -58.2812), (120.4688, -58.3789), (125.2344, -58.0859),
    (129.9609, -57.4023), (134.6484, -56.3281), (139.1797, -54.8633), (143.6328, -53.0469),
    (147.8906, -50.8789), (151.9531, -48.3594), (155.7812, -45.5273), (159.375, -42.3828),
    (162.7344, -38.9453), (165.7812, -35.2539), (168.4766, -31.3281), (170.8984, -27.207),
    (172.9297, -22.8906), (174.6484, -18.418), (175.9375, -13.8086), (176.875, -9.1211),
    (177.4609, -4.375), (177.6172, 0.4102), (177.3828, 5.1758), (176.7578, 9.9219),
    (175.7422, 14.5898), (174.375, 19.1797), (172.6172, 23.6133), (170.5078, 27.9102),
    (168.0469, 32.0117), (165.2734, 35.8984), (162.1484, 39.5508), (158.7891, 42.9297),
    (155.1562, 46.0156), (151.25, 48.8086), (147.1484, 51.25), (142.8516, 53.3789),
    (138.3984, 55.1367), (133.8281, 56.5039), (129.1797, 57.5195), (124.4141, 58.1445),
    (119.6484, 58.3594), (114.8828, 58.2031), (110.1172, 57.6562), (105.4297, 56.7188),
    (100.8203, 55.3906), (96.3672, 53.7109), (92.0312, 51.6602), (87.8906, 49.2578),
    (83.9844, 46.5234), (80.2734, 43.4766), (76.875, 40.1562), (73.7109, 36.543),
    (70.8594, 32.6953), (68.3594, 28.6328), (66.1719, 24.375), (64.375, 19.9609),
    (62.9297, 15.3906), (61.8359, 10.7422),
]

# Cut profile from Cut.txt
plane_points_cut_extrude = [
    (94.0625, -7.5195), (95.1562, -10.5078), (96.6406, -13.3594), (98.3984, -16.0156),
    (100.5078, -18.418), (102.8906, -20.5664), (105.5078, -22.3828), (108.3203, -23.8867),
    (111.3281, -25.0391), (114.4141, -25.8203), (117.5781, -26.2109), (120.7812, -26.2109),
    (123.9453, -25.8398), (127.0703, -25.0586), (130.0391, -23.9258), (132.8906, -22.4414),
    (135.5078, -20.6055), (137.8906, -18.4766), (140.0, -16.0742), (141.7969, -13.4375),
    (143.2422, -10.5859), (144.375, -7.5977), (145.0781, -4.4727), (145.4297, -1.3086),
    (145.3906, 1.8945), (121.5625, 26.1328), (118.3594, 26.2305), (115.1953, 25.918),
    (112.0703, 25.2344), (109.0625, 24.1797), (106.1719, 22.7734), (103.5156, 21.0156),
    (101.0547, 18.9453), (98.9062, 16.6016), (97.0312, 14.0039), (95.5078, 11.1914),
    (94.2969, 8.2422), (93.4766, 5.1367), (93.0469, 1.9727), (93.0078, -1.2109),
    (93.3594, -4.3945),
]

# 8. Build the Main Part (First Body)
with BuildPart() as my_part:
    # --- Profile 1 ---
    with BuildSketch() as sketch1:
        with BuildLine() as line1:
            Polyline(plane_points_1, close=True)
        make_face()
    extrude(amount=25.0)

    # --- Profile 2 ---
    with BuildSketch(Plane.XY.offset(25.0)) as sketch2:
        with BuildLine() as line2:
            Polyline(plane_points_2, close=True)
        make_face()
    extrude(amount=5.0)

    # --- Profile 3 ---
    with BuildSketch(Plane.XY.offset(30.0)) as sketch3:
        with BuildLine() as line3:
            Polyline(plane_points_3, close=True)
        make_face()
    extrude(amount=367.5)

    # --- Cut v1: Deep Cuts (Rectangle & Circle, depth -370.0mm) ---
    with BuildSketch(Plane.XY.offset(397.5)) as sketch_cut_v1_rect:
        with BuildLine() as line_cut_v1_rect:
            Polyline(plane_points_cut_v1_rect, close=True)
        make_face()
    extrude(amount=-370.0, mode=Mode.SUBTRACT)

    with BuildSketch(Plane.XY.offset(397.5)) as sketch_cut_v1_circ:
        with BuildLine() as line_cut_v1_circ:
            Polyline(plane_points_cut_v1_circ, close=True)
        make_face()
    extrude(amount=-370.0, mode=Mode.SUBTRACT)

    # --- Cut v2: Pocket Cuts (Pocket 1 & Pocket 2, depth -48.5mm) ---
    with BuildSketch(Plane.XY.offset(397.5)) as sketch_cut_v2_1:
        with BuildLine() as line_cut_v2_1:
            Polyline(plane_points_cut_v2_1, close=True)
        make_face()
    extrude(amount=-48.5, mode=Mode.SUBTRACT)

    with BuildSketch(Plane.XY.offset(397.5)) as sketch_cut_v2_2:
        with BuildLine() as line_cut_v2_2:
            Polyline(plane_points_cut_v2_2, close=True)
        make_face()
    extrude(amount=-48.5, mode=Mode.SUBTRACT)

    # --- Cut v3: Slanted Notch Cut (Depth 25mm extrude cut) ---
    with BuildSketch(cut_plane) as sketch_cut_v3:
        with BuildLine() as line_cut_v3:
            Polyline(plane_points_cut_v3, close=True)
        make_face()
    extrude(amount=-25.0, mode=Mode.SUBTRACT)

    # --- Cut v4b: New polygon cut at Z=322.5, depth 25mm ---
    with BuildSketch(Plane.XY.offset(322.5)) as sketch_cut_v4b:
        with BuildLine() as line_cut_v4b:
            Polyline([
                (101.7969, 40.918), (93.2031, 72.9883), (56.4813, 109.6859),
                (9.5719, 62.7375), (46.25, 26.0352), (78.3203, 17.4414),
            ], close=True)
        make_face()
    extrude(amount=25.0, mode=Mode.SUBTRACT)

    # --- Cut v4: Octagonal Internal Cut ---
    with BuildSketch(Plane.XY.offset(347.5)) as sketch_cut_v4:
        with BuildLine() as line_cut_v4:
            Polyline(plane_points_cut_v4, close=True)
        make_face()
    extrude(amount=-25.0, mode=Mode.SUBTRACT)

    # --- Cut v5: Circular Internal Cut ---
    with BuildSketch(Plane.XY.offset(322.5)) as sketch_cut_v5:
        with BuildLine() as line_cut_v5:
            Polyline(plane_points_cut_v5, close=True)
        make_face()
    extrude(amount=-222.5, mode=Mode.SUBTRACT)

    # --- Cut v5b: Circular cut at Z=322.5, depth 222.5mm ---
    with BuildSketch(Plane.XY.offset(322.5)) as sketch_cut_v5b:
        with BuildLine() as line_cut_v5b:
            Polyline(sort_and_sanitize_points([
                (82.1094, 37.1289, 322.5), (83.8281, 39.1211, 322.5),
                (85.1953, 41.3281, 322.5), (86.25, 43.7305, 322.5),
                (86.9141, 46.25, 322.5), (87.2266, 48.8477, 322.5),
                (87.1094, 51.4648, 322.5), (86.6406, 54.043, 322.5),
                (85.7812, 56.5039, 322.5), (84.5312, 58.8086, 322.5),
                (83.0078, 60.918, 322.5), (81.1328, 62.7734, 322.5),
                (79.0234, 64.3164, 322.5), (76.7188, 65.5469, 322.5),
                (74.2578, 66.4062, 322.5), (69.0625, 66.9922, 322.5),
                (71.6797, 66.8945, 322.5), (66.4844, 66.6992, 322.5),
                (63.9453, 66.0156, 322.5), (61.5625, 64.9805, 322.5),
                (59.3359, 63.5938, 322.5), (57.3438, 61.875, 322.5),
                (55.6641, 59.9023, 322.5), (54.2578, 57.6758, 322.5),
                (53.2031, 55.293, 322.5), (52.5391, 52.7539, 322.5),
                (52.2266, 50.1562, 322.5), (52.3438, 47.5391, 322.5),
                (52.8125, 44.9805, 322.5), (53.6719, 42.5, 322.5),
                (54.9219, 40.1953, 322.5), (56.4844, 38.0859, 322.5),
                (58.3203, 36.25, 322.5), (60.4297, 34.6875, 322.5),
                (62.7344, 33.457, 322.5), (65.1953, 32.5977, 322.5),
                (67.7734, 32.1094, 322.5), (70.3906, 32.0117, 322.5),
                (72.9688, 32.3047, 322.5), (75.5078, 32.9883, 322.5),
                (77.8906, 34.0234, 322.5), (80.1172, 35.4297, 322.5),
            ]), close=True)
        make_face()
    extrude(amount=-222.5, mode=Mode.SUBTRACT)

    # --- Cut Outer: Circular cut on diagonal plane ---
    outer_plane = Plane(
        origin=(179.3267, 60.0941, 100.0),
        x_dir=(1.0, -1.0, 0.0),
        z_dir=(-1.0, -1.0, 0.0),
    )
    with BuildSketch(outer_plane) as sketch_outer:
        Circle(radius=30.0)
    extrude(amount=-50.0, mode=Mode.SUBTRACT)

    # --- Cut Inner: Circular cut on diagonal plane ---
    inner_plane = Plane(
        origin=(167.5502, 48.3073, 100.0),
        x_dir=(1.0, -1.0, 0.0),
        z_dir=(-1.0, -1.0, 0.0),
    )
    with BuildSketch(inner_plane) as sketch_inner:
        Circle(radius=17.5)
    extrude(amount=50.0, mode=Mode.SUBTRACT)

    # --- Chamfer Loft Cut ---
    _inv_sq2 = 1.0 / math.sqrt(2)
    _normal_dir = gp_Dir(-_inv_sq2, -_inv_sq2, 0.0)
    _x_dir      = gp_Dir( _inv_sq2, -_inv_sq2, 0.0)

    _ax2_outer = gp_Ax2(gp_Pnt(179.3267, 60.0941, 100.0), _normal_dir, _x_dir)
    _circ_outer = gp_Circ(_ax2_outer, 30.0)
    _edge_outer = BRepBuilderAPI_MakeEdge(_circ_outer).Edge()
    _wire_outer = BRepBuilderAPI_MakeWire(_edge_outer).Wire()

    _ax2_inner = gp_Ax2(gp_Pnt(167.5502, 48.3073, 100.0), _normal_dir, _x_dir)
    _circ_inner = gp_Circ(_ax2_inner, 17.5)
    _edge_inner = BRepBuilderAPI_MakeEdge(_circ_inner).Edge()
    _wire_inner = BRepBuilderAPI_MakeWire(_edge_inner).Wire()

    _ts = BRepOffsetAPI_ThruSections(True, True)
    _ts.AddWire(_wire_outer)
    _ts.AddWire(_wire_inner)
    _ts.Build()
    _chamfer_solid = Solid(_ts.Shape())

    _body = my_part.solids()[0]
    _cut_op = BRepAlgoAPI_Cut(_body.wrapped, _chamfer_solid.wrapped)
    _cut_op.Build()
    my_part = Solid(_cut_op.Shape())

    # --- Fillet rectangular cut edges at Z=30 ---
    midpoints = [
        Vector((33.1641 + 82.6562)/2, (-36.582 - 86.0938)/2, 30.0),
        Vector((82.6562 + 110.9375)/2, (-86.0938 - 57.793)/2, 30.0),
        Vector((110.9375 + 61.4453)/2, (-57.793 - 8.3008)/2, 30.0),
        Vector((61.4453 + 33.1641)/2, (-8.3008 - 36.582)/2, 30.0)
    ]

    selected_edges = []
    for edge in my_part.edges():
        c = edge.center()
        for mid in midpoints:
            d = math.sqrt((c.X - mid.X)**2 + (c.Y - mid.Y)**2 + (c.Z - mid.Z)**2)
            if d < 2.0:
                selected_edges.append(edge)
                break

    if selected_edges:
        _fillet_op = BRepFilletAPI_MakeFillet(my_part.wrapped)
        for edge in selected_edges:
            _fillet_op.Add(20.0, edge.wrapped)
        _fillet_op.Build()
        if _fillet_op.IsDone():
            my_part = Solid(_fillet_op.Shape())

# 8b. Fillet top face rectangular cut edges at Z=397.5 (22mm radius)
_top_midpoints = [
    Vector((61.4453 + 110.9375)/2,  (-8.3008 - 57.793)/2,  397.5),
    Vector((110.9375 - 61.4453)/2,  (-57.793 + 8.3008)/2,  397.5),
    Vector((-61.4453 - 110.9375)/2, (-8.3008 - 57.793)/2,  397.5),
    Vector((-110.9375 + 61.4453)/2, (-57.793 + 8.3008)/2,  397.5),
]

_top_fillet_edges = []
for edge in my_part.edges():
    c = edge.center()
    for mid in _top_midpoints:
        d = math.sqrt((c.X - mid.X)**2 + (c.Y - mid.Y)**2 + (c.Z - mid.Z)**2)
        if d < 5.0:
            _top_fillet_edges.append(edge)
            break

if _top_fillet_edges:
    _top_fillet_op = BRepFilletAPI_MakeFillet(my_part.wrapped)
    for edge in _top_fillet_edges:
        _top_fillet_op.Add(20.0, edge.wrapped)
    _top_fillet_op.Build()
    if _top_fillet_op.IsDone():
        my_part = Solid(_top_fillet_op.Shape())

# 9. Extrude Profile: standalone solid fused into my_part
from OCP.BRepAlgoAPI import BRepAlgoAPI_Fuse

with BuildPart() as extrude_part:
    with BuildSketch(Plane.XY) as sketch_extrude:
        with BuildLine() as line_extrude:
            Polyline(plane_points_extrude, close=True)
        make_face()
    extrude(amount=50.2)

_fuse_op = BRepAlgoAPI_Fuse(my_part.wrapped, extrude_part.solids()[0].wrapped)
_fuse_op.Build()
my_part = Solid(_fuse_op.Shape())

# 10. Cut.txt extrude cut 55mm upward from Z=0
with BuildPart() as cut_extrude_part:
    with BuildSketch(Plane.XY) as sketch_cut_extrude:
        with BuildLine() as line_cut_extrude:
            Polyline(plane_points_cut_extrude, close=True)
        make_face()
    extrude(amount=55.0)

_cut_op2 = BRepAlgoAPI_Cut(my_part.wrapped, cut_extrude_part.solids()[0].wrapped)
_cut_op2.Build()
my_part = Solid(_cut_op2.Shape())

# 11. 8-point non-convex profile cut 45mm upward from Z=0
_cut2_pts = [
    (145.0781, -4.4727), (145.4297, -1.3086), (145.3906,  1.8945),
    (160.4297, 16.6602), (136.5625, 40.8984), (121.5625, 26.1328),
    (118.3594, 26.2305), (115.1953, 25.918),
]

_cut2_wire_builder = BRepBuilderAPI_MakeWire()
for i in range(len(_cut2_pts)):
    p1 = _cut2_pts[i]
    p2 = _cut2_pts[(i + 1) % len(_cut2_pts)]
    _e = BRepBuilderAPI_MakeEdge(gp_Pnt(p1[0], p1[1], 0.0), gp_Pnt(p2[0], p2[1], 0.0)).Edge()
    _cut2_wire_builder.Add(_e)
_cut2_wire = _cut2_wire_builder.Wire()

from OCP.gp import gp_Pln
from OCP.BRep import BRep_Builder
_cut2_face = BRepBuilderAPI_MakeFace(gp_Pln(gp_Pnt(0,0,0), gp_Dir(0,0,1)), _cut2_wire, True).Shape()
_cut2_solid = BRepPrimAPI_MakePrism(_cut2_face, gp_Vec(0.0, 0.0, 45.0)).Shape()

_cut_op3 = BRepAlgoAPI_Cut(my_part.wrapped, _cut2_solid)
_cut_op3.Build()
my_part = Solid(_cut_op3.Shape())

# 12. Mirror setup (applied after all cuts to my_part)
from OCP.gp import gp_Trsf, gp_Ax1
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp

_mirror_trsf = gp_Trsf()
_mirror_trsf.SetMirror(gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(1, 0, 0), gp_Dir(0, 1, 0)))  # YZ plane

# 13. Build 'TOP' text solid — cut into both solids
def _wire_area(wire):
    _f = BRepBuilderAPI_MakeFace(gp_Pln(gp_Pnt(0,0,0), gp_Dir(0,0,1)), wire.wrapped, True)
    if not _f.IsDone(): return 0.0
    _p = GProp_GProps()
    BRepGProp.SurfaceProperties_s(_f.Shape(), _p)
    return abs(_p.Mass())

_xy_pln = gp_Pln(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1))
_text_compounds = []

for _letter, _offset_x in [("T", -50), ("O", 0), ("P", 50)]:
    with BuildSketch(Plane(origin=(_offset_x, 0, 0))) as _sk:
        Text(_letter, font_size=70, align=(Align.CENTER, Align.CENTER))
    _letter_wires = list(_sk.sketch.wires())
    if not _letter_wires:
        continue
    _letter_wires.sort(key=_wire_area, reverse=True)
    _outer = _letter_wires[0]
    _holes = _letter_wires[1:]
    _face_maker = BRepBuilderAPI_MakeFace(_xy_pln, _outer.wrapped, True)
    if not _face_maker.IsDone():
        continue
    for _hole_wire in _holes:
        _face_maker.Add(_hole_wire.wrapped)
    _letter_solid = BRepPrimAPI_MakePrism(_face_maker.Shape(), gp_Vec(0.0, 0.0, 5.0)).Shape()
    _text_compounds.append(_letter_solid)

_text_solid_shape = _text_compounds[0]
for _tc in _text_compounds[1:]:
    _fuse = BRepAlgoAPI_Fuse(_text_solid_shape, _tc)
    _fuse.Build()
    _text_solid_shape = _fuse.Shape()

text_solid = Solid(_text_solid_shape)

# Flip, rotate and position text
_text_flip_trsf = gp_Trsf()
_text_flip_trsf.SetMirror(gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(0, 1, 0), gp_Dir(1, 0, 0)))  # mirror in XY plane (flip Z)
text_solid = Solid(BRepBuilderAPI_Transform(text_solid.wrapped, _text_flip_trsf, True).Shape())

_text_rot_trsf = gp_Trsf()
_text_rot_trsf.SetRotation(gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1)), -math.pi / 2)
text_solid = Solid(BRepBuilderAPI_Transform(text_solid.wrapped, _text_rot_trsf, True).Shape())

_text_translate_trsf = gp_Trsf()
_text_translate_trsf.SetTranslation(gp_Vec(225.0, 0.0, 0.0))
text_solid = Solid(BRepBuilderAPI_Transform(text_solid.wrapped, _text_translate_trsf, True).Shape())

# Rotate 180 degrees around Z axis at final position (225, 0, 0)
_text_rot180_trsf = gp_Trsf()
_text_rot180_trsf.SetRotation(gp_Ax1(gp_Pnt(225.0, 0.0, 0.0), gp_Dir(0, 0, 1)), math.pi)
text_solid = Solid(BRepBuilderAPI_Transform(text_solid.wrapped, _text_rot180_trsf, True).Shape())



# 14. R text cut on top face (Z=397.5), 5mm downward in -Z
_xy_pln_top = gp_Pln(gp_Pnt(0, 0, 397.5), gp_Dir(0, 0, 1))
with BuildSketch(Plane(origin=(0, 0, 397.5))) as _sk_r:
    Text("R", font_size=34, align=(Align.CENTER, Align.CENTER))

_r_wires = list(_sk_r.sketch.wires())
_r_wires.sort(key=_wire_area, reverse=True)
_face_maker_r = BRepBuilderAPI_MakeFace(_xy_pln_top, _r_wires[0].wrapped, True)
for _hw in _r_wires[1:]:
    _face_maker_r.Add(_hw.wrapped)
text_R_solid = Solid(BRepPrimAPI_MakePrism(_face_maker_r.Shape(), gp_Vec(0.0, 0.0, -5.0)).Shape())

_r_rot_trsf = gp_Trsf()
_r_rot_trsf.SetRotation(gp_Ax1(gp_Pnt(0, 0, 397.5), gp_Dir(0, 0, 1)), -math.pi / 2)
text_R_solid = Solid(BRepBuilderAPI_Transform(text_R_solid.wrapped, _r_rot_trsf, True).Shape())

_r_translate_trsf = gp_Trsf()
_r_translate_trsf.SetTranslation(gp_Vec(170.0, -15.0, 0.0))
text_R_solid = Solid(BRepBuilderAPI_Transform(text_R_solid.wrapped, _r_translate_trsf, True).Shape())

# 15. L text cut (goes into my_part_mirrored)
with BuildSketch(Plane(origin=(0, 0, 397.5))) as _sk_l:
    Text("L", font_size=34, align=(Align.CENTER, Align.CENTER))

_l_wires = list(_sk_l.sketch.wires())
_l_wires.sort(key=_wire_area, reverse=True)
_face_maker_l = BRepBuilderAPI_MakeFace(_xy_pln_top, _l_wires[0].wrapped, True)
for _hw in _l_wires[1:]:
    _face_maker_l.Add(_hw.wrapped)
text_L_solid = Solid(BRepPrimAPI_MakePrism(_face_maker_l.Shape(), gp_Vec(0.0, 0.0, -5.0)).Shape())

_l_rot_trsf = gp_Trsf()
_l_rot_trsf.SetRotation(gp_Ax1(gp_Pnt(0, 0, 397.5), gp_Dir(0, 0, 1)), -math.pi / 2)
text_L_solid = Solid(BRepBuilderAPI_Transform(text_L_solid.wrapped, _l_rot_trsf, True).Shape())

_l_translate_trsf = gp_Trsf()
_l_translate_trsf.SetTranslation(gp_Vec(-200.0, -5.0, -5.0))
text_L_solid = Solid(BRepBuilderAPI_Transform(text_L_solid.wrapped, _l_translate_trsf, True).Shape())

# 16. Mirror my_part after all cuts
my_part_mirrored = Solid(BRepBuilderAPI_Transform(my_part.wrapped, _mirror_trsf, True).Shape())

# Cut TOP text into my_part only (after mirror, so mirrored solid is unaffected)
_cut_text_s1a = BRepAlgoAPI_Cut(my_part.wrapped, text_solid.wrapped)
_cut_text_s1a.Build()
my_part = Solid(_cut_text_s1a.Shape())

# Cut R into my_part only (after mirror, so mirrored solid is unaffected)
_r_cut_op = BRepAlgoAPI_Cut(my_part.wrapped, text_R_solid.wrapped)
_r_cut_op.Build()
my_part = Solid(_r_cut_op.Shape())

# 17. Cut TOP text into my_part_mirrored (mirrored copy at X=-225, rotated 180 in place)
_text_solid_mirrored = Solid(BRepBuilderAPI_Transform(text_solid.wrapped, _mirror_trsf, True).Shape())
_text_s2_rot180_trsf = gp_Trsf()
_text_s2_rot180_trsf.SetRotation(gp_Ax1(gp_Pnt(-225.0, 0.0, 0.0), gp_Dir(0, 0, 1)), math.pi)
_text_solid_mirrored = Solid(BRepBuilderAPI_Transform(_text_solid_mirrored.wrapped, _text_s2_rot180_trsf, True).Shape())

_text_s2_rot180x_trsf = gp_Trsf()
_text_s2_rot180x_trsf.SetRotation(gp_Ax1(gp_Pnt(-225.0, 0.0, 0.0), gp_Dir(1, 0, 0)), math.pi)
_text_solid_mirrored = Solid(BRepBuilderAPI_Transform(_text_solid_mirrored.wrapped, _text_s2_rot180x_trsf, True).Shape())

# Reverse cut direction: mirror through XY plane at the text position
_text_s2_flip_z_trsf = gp_Trsf()
_text_s2_flip_z_trsf.SetMirror(gp_Ax2(gp_Pnt(-225.0, 0.0, 0.0), gp_Dir(0, 0, 1), gp_Dir(1, 0, 0)))
_text_solid_mirrored = Solid(BRepBuilderAPI_Transform(_text_solid_mirrored.wrapped, _text_s2_flip_z_trsf, True).Shape())
_cut_text_s2 = BRepAlgoAPI_Cut(my_part_mirrored.wrapped, _text_solid_mirrored.wrapped)
_cut_text_s2.Build()
my_part_mirrored = Solid(_cut_text_s2.Shape())

# Cut L into my_part_mirrored
_l_cut_op = BRepAlgoAPI_Cut(my_part_mirrored.wrapped, text_L_solid.wrapped)
_l_cut_op.Build()
my_part_mirrored = Solid(_l_cut_op.Shape())

# 18. New cut from Cut.txt — flat polygon on top face (Z=397.5), 5mm downward
_cut_top_pts = [
    (-49.7266, 11.9922),
    (-49.7266, -3.6328),
    (-46.7578, -3.6328),
    (-46.7578,  8.6719),
    (-24.7266,  8.6719),
    (-24.7266, 11.9922),
]

_cut_top_wire_builder = BRepBuilderAPI_MakeWire()
for i in range(len(_cut_top_pts)):
    p1 = _cut_top_pts[i]
    p2 = _cut_top_pts[(i + 1) % len(_cut_top_pts)]
    _e = BRepBuilderAPI_MakeEdge(gp_Pnt(p1[0], p1[1], 397.5), gp_Pnt(p2[0], p2[1], 397.5)).Edge()
    _cut_top_wire_builder.Add(_e)
_cut_top_wire = _cut_top_wire_builder.Wire()

_cut_top_pln = gp_Pln(gp_Pnt(0, 0, 397.5), gp_Dir(0, 0, 1))
_cut_top_face = BRepBuilderAPI_MakeFace(_cut_top_pln, _cut_top_wire, True).Shape()
_cut_top_solid = BRepPrimAPI_MakePrism(_cut_top_face, gp_Vec(0.0, 0.0, -5.0)).Shape()

_cut_top_op = BRepAlgoAPI_Cut(my_part.wrapped, _cut_top_solid)
_cut_top_op.Build()
my_part = Solid(_cut_top_op.Shape())

_cut_top_op2 = BRepAlgoAPI_Cut(my_part_mirrored.wrapped, _cut_top_solid)
_cut_top_op2.Build()
my_part_mirrored = Solid(_cut_top_op2.Shape())

# 19. Letter R solid — font size 250, extruded 6mm, placed on XZ plane at origin
# Step 1: build on XY plane with correct XY normal
_xy_pln_r = gp_Pln(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1))
with BuildSketch(Plane.XY) as _sk_r_big:
    Text("R", font_size=140, align=(Align.CENTER, Align.CENTER))

_r_big_wires = list(_sk_r_big.sketch.wires())
_r_big_wires.sort(key=_wire_area, reverse=True)
_face_maker_r_big = BRepBuilderAPI_MakeFace(_xy_pln_r, _r_big_wires[0].wrapped, True)
for _hw in _r_big_wires[1:]:
    _face_maker_r_big.Add(_hw.wrapped)

# Step 2: extrude 6mm in +Z on XY plane → solid R
_r_big_solid_xy = BRepPrimAPI_MakePrism(_face_maker_r_big.Shape(), gp_Vec(0.0, 0.0, 50.0)).Shape()

# Step 3: rotate solid -90 degrees around X axis → moves XY face onto XZ plane
_r_big_to_xz = gp_Trsf()
_r_big_to_xz.SetRotation(gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(1, 0, 0)), -math.pi / 2)
text_R_big_solid = Solid(BRepBuilderAPI_Transform(_r_big_solid_xy, _r_big_to_xz, True).Shape())

# Translate to final position (170 in X, 281.5 in Z)
_r_big_translate_trsf = gp_Trsf()
_r_big_translate_trsf.SetTranslation(gp_Vec(120.0, -152.0, 210))
text_R_big_solid = Solid(BRepBuilderAPI_Transform(text_R_big_solid.wrapped, _r_big_translate_trsf, True).Shape())

# Cut R solid into my_part (solid 1)
_r_big_cut_op = BRepAlgoAPI_Cut(my_part.wrapped, text_R_big_solid.wrapped)
_r_big_cut_op.Build()
my_part = Solid(_r_big_cut_op.Shape())

# 20. Letter L solid — same size and position as big R, cut into my_part_mirrored
_xy_pln_l = gp_Pln(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1))
with BuildSketch(Plane.XY) as _sk_l_big:
    Text("L", font_size=140, align=(Align.CENTER, Align.CENTER))

_l_big_wires = list(_sk_l_big.sketch.wires())
_l_big_wires.sort(key=_wire_area, reverse=True)
_face_maker_l_big = BRepBuilderAPI_MakeFace(_xy_pln_l, _l_big_wires[0].wrapped, True)
for _hw in _l_big_wires[1:]:
    _face_maker_l_big.Add(_hw.wrapped)

_l_big_solid_xy = BRepPrimAPI_MakePrism(_face_maker_l_big.Shape(), gp_Vec(0.0, 0.0, 50.0)).Shape()

_l_big_to_xz = gp_Trsf()
_l_big_to_xz.SetRotation(gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(1, 0, 0)), -math.pi / 2)
text_L_big_solid = Solid(BRepBuilderAPI_Transform(_l_big_solid_xy, _l_big_to_xz, True).Shape())

_l_big_translate_trsf = gp_Trsf()
_l_big_translate_trsf.SetTranslation(gp_Vec(-120.0, -152.0, 210))
text_L_big_solid = Solid(BRepBuilderAPI_Transform(text_L_big_solid.wrapped, _l_big_translate_trsf, True).Shape())

# Cut L solid into my_part_mirrored (solid 2)
_l_big_cut_op = BRepAlgoAPI_Cut(my_part_mirrored.wrapped, text_L_big_solid.wrapped)
_l_big_cut_op.Build()
my_part_mirrored = Solid(_l_big_cut_op.Shape())

# 21. New extrude body from profiles.json — height 27.5mm in +Z, separate body
import json as _json

_profile_pts = [
    (-153.711, 72.188, 0.0),
    (-158.203, 69.844, 0.0),
    (-156.914, 73.32, 0.0),
    (-155.938, 76.914, 0.0),
    (-155.391, 80.586, 0.0),
    (-155.234, 84.297, 0.0),
    (-155.469, 88.008, 0.0),
    (-156.055, 91.66, 0.0),
    (-157.07, 95.254, 0.0),
    (-158.477, 98.691, 0.0),
    (-160.195, 101.992, 0.0),
    (-162.266, 105.059, 0.0),
    (-164.648, 107.91, 0.0),
    (-167.344, 110.488, 0.0),
    (-161.602, 112.812, 0.0),
    (-155.742, 114.844, 0.0),
    (-149.805, 116.562, 0.0),
    (-143.789, 117.969, 0.0),
    (-137.695, 119.082, 0.0),
    (-131.562, 119.883, 0.0),
    (-125.391, 120.352, 0.0),
    (-119.219, 120.508, 0.0),
    (119.219, 120.508, 0.0),
    (125.43, 120.352, 0.0),
    (131.562, 119.883, 0.0),
    (137.734, 119.082, 0.0),
    (143.789, 117.969, 0.0),
    (149.805, 116.562, 0.0),
    (155.781, 114.844, 0.0),
    (161.602, 112.812, 0.0),
    (167.344, 110.488, 0.0),
    (164.648, 107.91, 0.0),
    (162.266, 105.059, 0.0),
    (160.195, 101.992, 0.0),
    (158.477, 98.691, 0.0),
    (157.07, 95.254, 0.0),
    (156.094, 91.66, 0.0),
    (155.469, 88.008, 0.0),
    (155.234, 84.297, 0.0),
    (155.391, 80.586, 0.0),
    (155.938, 76.914, 0.0),
    (156.914, 73.32, 0.0),
    (158.242, 69.844, 0.0),
    (153.711, 72.188, 0.0),
    (149.023, 74.219, 0.0),
    (144.258, 75.977, 0.0),
    (139.375, 77.402, 0.0),
    (134.414, 78.535, 0.0),
    (129.375, 79.336, 0.0),
    (124.297, 79.824, 0.0),
    (119.219, 79.98, 0.0),
    (119.219, 62.871, 0.0),
    (114.297, 62.676, 0.0),
    (109.375, 62.09, 0.0),
    (104.531, 61.133, 0.0),
    (99.805, 59.785, 0.0),
    (95.156, 58.086, 0.0),
    (90.664, 56.016, 0.0),
    (86.367, 53.594, 0.0),
    (82.266, 50.859, 0.0),
    (78.398, 47.793, 0.0),
    (74.766, 44.453, 0.0),
    (71.406, 40.82, 0.0),
    (68.359, 36.953, 0.0),
    (65.625, 32.852, 0.0),
    (63.203, 28.535, 0.0),
    (61.133, 24.043, 0.0),
    (59.414, 19.414, 0.0),
    (58.086, 14.668, 0.0),
    (57.109, 9.824, 0.0),
    (56.562, 4.922, 0.0),
    (56.367, -0.02, 0.0),
    (56.562, -4.941, 0.0),
    (57.109, -9.844, 0.0),
    (58.086, -14.688, 0.0),
    (59.414, -19.434, 0.0),
    (61.133, -24.082, 0.0),
    (63.203, -28.555, 0.0),
    (65.625, -32.871, 0.0),
    (68.359, -36.973, 0.0),
    (71.406, -40.84, 0.0),
    (74.766, -44.473, 0.0),
    (78.398, -47.832, 0.0),
    (82.266, -50.879, 0.0),
    (86.367, -53.633, 0.0),
    (90.664, -56.035, 0.0),
    (95.156, -58.105, 0.0),
    (99.805, -59.805, 0.0),
    (104.531, -61.152, 0.0),
    (109.375, -62.109, 0.0),
    (114.297, -62.695, 0.0),
    (119.219, -62.891, 0.0),
    (119.219, -80.02, 0.0),
    (124.297, -79.844, 0.0),
    (129.375, -79.355, 0.0),
    (134.414, -78.555, 0.0),
    (139.375, -77.441, 0.0),
    (144.258, -75.996, 0.0),
    (149.023, -74.258, 0.0),
    (153.711, -72.207, 0.0),
    (158.242, -69.863, 0.0),
    (156.914, -73.34, 0.0),
    (155.938, -76.934, 0.0),
    (155.391, -80.605, 0.0),
    (155.234, -84.316, 0.0),
    (155.469, -88.027, 0.0),
    (156.094, -91.699, 0.0),
    (157.07, -95.273, 0.0),
    (158.477, -98.73, 0.0),
    (160.195, -102.012, 0.0),
    (162.266, -105.098, 0.0),
    (164.648, -107.93, 0.0),
    (167.344, -110.508, 0.0),
    (161.602, -112.832, 0.0),
    (155.781, -114.863, 0.0),
    (149.805, -116.582, 0.0),
    (143.789, -118.008, 0.0),
    (137.734, -119.102, 0.0),
    (131.562, -119.902, 0.0),
    (125.43, -120.371, 0.0),
    (119.219, -120.527, 0.0),
    (-119.219, -120.527, 0.0),
    (-125.391, -120.371, 0.0),
    (-131.562, -119.902, 0.0),
    (-137.695, -119.102, 0.0),
    (-143.789, -118.008, 0.0),
    (-149.805, -116.582, 0.0),
    (-155.742, -114.863, 0.0),
    (-161.602, -112.832, 0.0),
    (-167.344, -110.508, 0.0),
    (-164.648, -107.93, 0.0),
    (-162.266, -105.098, 0.0),
    (-160.195, -102.012, 0.0),
    (-158.477, -98.73, 0.0),
    (-157.07, -95.273, 0.0),
    (-156.055, -91.699, 0.0),
    (-155.469, -88.027, 0.0),
    (-155.234, -84.316, 0.0),
    (-155.391, -80.605, 0.0),
    (-155.938, -76.934, 0.0),
    (-156.914, -73.34, 0.0),
    (-158.203, -69.863, 0.0),
    (-153.711, -72.207, 0.0),
    (-149.023, -74.258, 0.0),
    (-144.258, -75.996, 0.0),
    (-139.375, -77.441, 0.0),
    (-134.414, -78.555, 0.0),
    (-129.375, -79.355, 0.0),
    (-124.297, -79.844, 0.0),
    (-119.219, -80.02, 0.0),
    (-119.219, -62.891, 0.0),
    (-114.297, -62.695, 0.0),
    (-109.375, -62.109, 0.0),
    (-104.531, -61.152, 0.0),
    (-99.805, -59.805, 0.0),
    (-95.156, -58.105, 0.0),
    (-90.664, -56.035, 0.0),
    (-86.367, -53.633, 0.0),
    (-82.266, -50.879, 0.0),
    (-78.398, -47.832, 0.0),
    (-74.766, -44.473, 0.0),
    (-71.406, -40.84, 0.0),
    (-68.359, -36.973, 0.0),
    (-65.625, -32.871, 0.0),
    (-63.203, -28.555, 0.0),
    (-61.133, -24.082, 0.0),
    (-59.414, -19.434, 0.0),
    (-58.086, -14.688, 0.0),
    (-57.109, -9.844, 0.0),
    (-56.523, -4.941, 0.0),
    (-56.328, -0.02, 0.0),
    (-56.523, 4.922, 0.0),
    (-57.109, 9.824, 0.0),
    (-58.086, 14.668, 0.0),
    (-59.414, 19.414, 0.0),
    (-61.133, 24.043, 0.0),
    (-63.203, 28.535, 0.0),
    (-65.625, 32.852, 0.0),
    (-68.359, 36.953, 0.0),
    (-71.406, 40.82, 0.0),
    (-74.766, 44.453, 0.0),
    (-78.398, 47.793, 0.0),
    (-82.266, 50.859, 0.0),
    (-86.367, 53.594, 0.0),
    (-90.664, 56.016, 0.0),
    (-95.156, 58.086, 0.0),
    (-99.805, 59.785, 0.0),
    (-104.531, 61.133, 0.0),
    (-109.375, 62.09, 0.0),
    (-114.297, 62.676, 0.0),
    (-119.219, 62.871, 0.0),
    (-119.219, 79.98, 0.0),
    (-124.297, 79.824, 0.0),
    (-129.375, 79.336, 0.0),
    (-134.414, 78.535, 0.0),
    (-139.375, 77.402, 0.0),
    (-144.258, 75.977, 0.0),
    (-149.023, 74.219, 0.0),
]

# Identify the 3 wires using same index split as established from coordinate analysis:
# Outer frame: idx 0-37 + 79-136 + 178-197
# Right hole:  idx 38-78
# Left hole:   idx 137-177

def _make_wire_from_indices(pts_list, indices):
    wb = BRepBuilderAPI_MakeWire()
    for i in range(len(indices)):
        p1 = pts_list[indices[i]]
        p2 = pts_list[indices[(i + 1) % len(indices)]]
        _e = BRepBuilderAPI_MakeEdge(gp_Pnt(p1[0], p1[1], 0.0), gp_Pnt(p2[0], p2[1], 0.0)).Edge()
        wb.Add(_e)
    return wb.Wire()

# Correct index splits based on JSON segment order:
# Outer frame: 0-50 + 92-149 + 191-197 (skipping inner arcs)
# Right hole:  51-91
# Left hole:   150-190
_prof_outer_idx = list(range(0, 51)) + list(range(92, 150)) + list(range(191, 198))
_prof_rhole_idx = list(range(51, 92))
_prof_lhole_idx = list(range(150, 191))

_prof_pln = gp_Pln(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1))
_prof_outer_wire = _make_wire_from_indices(_profile_pts, _prof_outer_idx)
_prof_rhole_wire = _make_wire_from_indices(_profile_pts, _prof_rhole_idx)
_prof_lhole_wire = _make_wire_from_indices(_profile_pts, _prof_lhole_idx)

# Extrude outer solid 27.5mm
_prof_outer_face = BRepBuilderAPI_MakeFace(_prof_pln, _prof_outer_wire, True).Shape()
profile_solid = Solid(BRepPrimAPI_MakePrism(_prof_outer_face, gp_Vec(0.0, 0.0, 27.5)).Shape())

# Boolean cut the two circular holes
_prof_rhole_face = BRepBuilderAPI_MakeFace(_prof_pln, _prof_rhole_wire, True).Shape()
_prof_rhole_solid = BRepPrimAPI_MakePrism(_prof_rhole_face, gp_Vec(0.0, 0.0, 27.5)).Shape()
_prof_lhole_face = BRepBuilderAPI_MakeFace(_prof_pln, _prof_lhole_wire, True).Shape()
_prof_lhole_solid = BRepPrimAPI_MakePrism(_prof_lhole_face, gp_Vec(0.0, 0.0, 27.5)).Shape()

_prof_rcut = BRepAlgoAPI_Cut(profile_solid.wrapped, _prof_rhole_solid)
_prof_rcut.Build()
profile_solid = Solid(_prof_rcut.Shape())

_prof_lcut = BRepAlgoAPI_Cut(profile_solid.wrapped, _prof_lhole_solid)
_prof_lcut.Build()
profile_solid = Solid(_prof_lcut.Shape())

# 22. View in OCP CAD Viewer
show(my_part, my_part_mirrored, profile_solid)

# 23. Export to STEP and STL on Desktop
import tkinter as tk
from tkinter import filedialog
from build123d import Compound, export_step, export_stl

_assembly = Compound([my_part, my_part_mirrored, profile_solid])

_desktop = "/Users/softage/Desktop"
_step_path = f"{_desktop}/Set_3.step"
_stl_path  = f"{_desktop}/Set_3.stl"

export_step(_assembly, _step_path)
print(f"STEP exported: {_step_path}")

export_stl(_assembly, _stl_path)
print(f"STL exported:  {_stl_path}")