district_list = (
    (0, "尚未选择"),
    (1, '北京'), (2, '重庆'), (3, '上海'), (4, '天津'), (5, '长春'), (6, '长沙'), (7, '常州'), (8, '成都'), (9, '大连'),
    (10, '东莞'), (11, '佛山'), (12, '福州'), (13, '广州'), (14, '贵阳'), (15, '哈尔滨'), (16, '海口'), (17, '邯郸'),
    (18, '杭州'), (19, '合肥'), (20, '惠州'), (21, '焦作'), (22, '嘉兴'), (23, '吉林'), (24, '济南'), (25, '昆明'),
    (26, '兰州'), (27, '柳州'), (28, '洛阳'), (29, '南昌'), (30, '南京'), (31, '南宁'), (32, '南通'), (33, '宁波'),
    (34, '青岛'), (35, '泉州'), (36, '沈阳'), (37, '深圳'), (38, '石家庄'), (39, '苏州'), (40, '台州'), (41, '唐山'),
    (42, '潍坊'), (43, '威海'), (44, '武汉'), (45, '无锡'), (46, '厦门'), (47, '西安'), (48, '许昌'), (49, '徐州'),
    (50, '扬州'), (51, '烟台'), (52, '漳州'), (53, '郑州'), (54, '中山'), (55, '珠海'), (56, '阿坝'), (57, '阿克苏'),
    (58, '阿拉善盟'), (59, '阿勒泰'), (60, '阿里'), (61, '安康'), (62, '安庆'), (63, '鞍山'), (64, '安顺'),
    (65, '安阳'),
    (66, '白城'), (67, '百色'), (68, '白山'), (69, '白银'), (70, '蚌埠'), (71, '保定'), (72, '宝鸡'), (73, '保山'),
    (74, '包头'), (75, '巴彦淖尔'), (76, '巴音郭楞'), (77, '巴中'), (78, '北海'), (79, '本溪'), (80, '毕节'),
    (81, '滨州'),
    (82, '博尔塔拉'), (83, '亳州'), (84, '沧州'), (85, '常德'), (86, '昌都'), (87, '昌吉'), (88, '长治'), (89, '巢湖'),
    (90, '朝阳'), (91, '潮州'), (92, '承德'), (93, '郴州'), (94, '赤峰'), (95, '池州'), (96, '崇左'), (97, '楚雄'),
    (98, '滁州'), (99, '大理'), (100, '丹东'), (101, '大庆'), (102, '大同'), (103, '大兴安岭'), (104, '达州'),
    (105, '德宏'), (106, '德阳'), (107, '德州'), (108, '定西'), (109, '迪庆'), (110, '东营'), (111, '鄂尔多斯'),
    (112, '恩施'), (113, '鄂州'), (114, '防城港'), (115, '抚顺'), (116, '阜新'), (117, '阜阳'), (118, '抚州'),
    (119, '甘南'), (120, '赣州'), (121, '甘孜'), (122, '广安'), (123, '广元'), (124, '贵港'), (125, '桂林'),
    (126, '果洛'),
    (127, '固原'), (128, '海北'), (129, '海东'), (130, '海南'), (131, '海西'), (132, '哈密'), (133, '汉中'),
    (134, '鹤壁'),
    (135, '河池'), (136, '鹤岗'), (137, '黑河'), (138, '衡水'), (139, '衡阳'), (140, '和田地'), (141, '河源'),
    (142, '菏泽'), (143, '贺州'), (144, '红河'), (145, '淮安'), (146, '淮北'), (147, '怀化'), (148, '淮南'),
    (149, '黄冈'),
    (150, '黄南'), (151, '黄山'), (152, '黄石'), (153, '呼和浩特'), (154, '葫芦岛'), (155, '呼伦贝尔'), (156, '湖州'),
    (157, '佳木斯'), (158, '江门'), (159, '吉安'), (160, '嘉峪关'), (161, '揭阳'), (162, '金昌'), (163, '晋城'),
    (164, '景德镇'), (165, '荆门'), (166, '荆州'), (167, '金华'), (168, '济宁'), (169, '晋中'), (170, '锦州'),
    (171, '九江'), (172, '酒泉'), (173, '鸡西'), (174, '开封'), (175, '喀什地'), (176, '克拉玛依'), (177, '克孜勒'),
    (178, '来宾'), (179, '莱芜'), (180, '廊坊'), (181, '拉萨'), (182, '乐山'), (183, '凉山'), (184, '连云港'),
    (185, '聊城'), (186, '辽阳'), (187, '辽源'), (188, '丽江'), (189, '临沧'), (190, '临汾'), (191, '临夏'),
    (192, '临沂'),
    (193, '林芝'), (194, '丽水'), (195, '六安'), (196, '六盘水'), (197, '陇南'), (198, '龙岩'), (199, '娄底'),
    (200, '漯河'), (201, '泸州'), (202, '吕梁'), (203, '马鞍山'), (204, '茂名'), (205, '眉山'), (206, '梅州'),
    (207, '绵阳'), (208, '牡丹江'), (209, '南充'), (210, '南平'), (211, '南阳'), (212, '那曲'), (213, '内江'),
    (214, '宁德'), (215, '怒江'), (216, '盘锦'), (217, '攀枝花'), (218, '平顶山'), (219, '平凉'), (220, '萍乡'),
    (221, '普洱'), (222, '莆田'), (223, '濮阳'), (224, '黔东'), (225, '黔南'), (226, '黔西南'), (227, '庆阳'),
    (228, '清远'), (229, '秦皇岛'), (230, '钦州'), (231, '齐齐哈尔'), (232, '七台河'), (233, '曲靖'), (234, '衢州'),
    (235, '日喀则'), (236, '日照'), (237, '三门峡'), (238, '三明'), (239, '三亚'), (240, '商洛'), (241, '商丘'),
    (242, '上饶'), (243, '山南'), (244, '汕头'), (245, '汕尾'), (246, '韶关'), (247, '绍兴'), (248, '邵阳'),
    (249, '十堰'),
    (250, '石嘴山'), (251, '双鸭山'), (252, '朔州'), (253, '四平'), (254, '松原'), (255, '绥化'), (256, '遂宁'),
    (257, '随州'), (258, '宿迁'), (259, '宿州'), (260, '塔城地'), (261, '泰安'), (262, '太原'), (263, '泰州'),
    (264, '天水'), (265, '铁岭'), (266, '铜川'), (267, '通化'), (268, '通辽'), (269, '铜陵'), (270, '铜仁'),
    (271, '吐鲁番'), (272, '渭南'), (273, '文山'), (274, '温州'), (275, '乌海'), (276, '芜湖'), (277, '乌兰察布'),
    (278, '乌鲁木齐'), (279, '武威'), (280, '吴忠'), (281, '梧州'), (282, '襄樊'), (283, '湘潭'), (284, '湘西'),
    (285, '咸宁'), (286, '咸阳'), (287, '孝感'), (288, '锡林郭勒盟'), (289, '兴安盟'), (290, '邢台'), (291, '西宁'),
    (292, '新乡'), (293, '信阳'), (294, '新余'), (295, '忻州'), (296, '西双版纳'), (297, '宣城'), (298, '雅安'),
    (299, '延安'), (300, '延边'), (301, '盐城'), (302, '阳江'), (303, '阳泉'), (304, '宜宾'), (305, '宜昌'),
    (306, '伊春'),
    (307, '宜春'), (308, '伊犁哈萨克'), (309, '银川'), (310, '营口'), (311, '鹰潭'), (312, '益阳'), (313, '永州'),
    (314, '岳阳'), (315, '玉林'), (316, '榆林'), (317, '运城'), (318, '云浮'), (319, '玉树'), (320, '玉溪'),
    (321, '枣庄'),
    (322, '张家界'), (323, '张家口'), (324, '张掖'), (325, '湛江'), (326, '肇庆'), (327, '昭通'), (328, '镇江'),
    (329, '中卫'), (330, '周口'), (331, '舟山'), (332, '驻马店'), (333, '株洲'), (334, '淄博'), (335, '自贡'),
    (336, '资阳'), (337, '遵义'), (338, '阿城'), (339, '安福'), (340, '安吉'), (341, '安宁'), (342, '安丘'),
    (343, '安溪'),
    (344, '安义'), (345, '安远'), (346, '宝应'), (347, '巴彦'), (348, '滨海'), (349, '宾县'), (350, '宾阳'),
    (351, '璧山'),
    (352, '博爱'), (353, '博罗'), (354, '博兴'), (355, '苍南'), (356, '苍山'), (357, '曹县'), (358, '长岛'),
    (359, '长丰'),
    (360, '长海'), (361, '长乐'), (362, '昌乐'), (363, '常山'), (364, '常熟'), (365, '长泰'), (366, '长汀'),
    (367, '长兴'),
    (368, '昌邑'), (369, '潮安'), (370, '呈贡'), (371, '城口'), (372, '成武'), (373, '茌平'), (374, '崇仁'),
    (375, '崇义'),
    (376, '崇州'), (377, '淳安'), (378, '慈溪'), (379, '从化'), (380, '枞阳'), (381, '大丰'), (382, '岱山'),
    (383, '砀山'),
    (384, '当涂'), (385, '单县'), (386, '丹阳'), (387, '大埔'), (388, '大田'), (389, '大邑'), (390, '大余'),
    (391, '大足'),
    (392, '德安'), (393, '德化'), (394, '德惠'), (395, '登封'), (396, '德清'), (397, '德庆'), (398, '德兴'),
    (399, '电白'),
    (400, '垫江'), (401, '定南'), (402, '定陶'), (403, '定远'), (404, '东阿'), (405, '东海'), (406, '东明'),
    (407, '东平'),
    (408, '东山'), (409, '东台'), (410, '洞头'), (411, '东乡'), (412, '东阳'), (413, '东源'), (414, '东至'),
    (415, '都昌'),
    (416, '都江堰'), (417, '恩平'), (418, '法库'), (419, '繁昌'), (420, '方正'), (421, '肥城'), (422, '肥东'),
    (423, '肥西'), (424, '费县'), (425, '丰城'), (426, '丰都'), (427, '奉化'), (428, '奉节'), (429, '封开'),
    (430, '丰顺'),
    (431, '凤台'), (432, '丰县'), (433, '奉新'), (434, '凤阳'), (435, '分宜'), (436, '佛冈'), (437, '福安'),
    (438, '福鼎'),
    (439, '浮梁'), (440, '富民'), (441, '阜南'), (442, '阜宁'), (443, '福清'), (444, '富阳'), (445, '赣县'),
    (446, '赣榆'),
    (447, '高安'), (448, '藁城'), (449, '高淳'), (450, '皋兰'), (451, '高陵'), (452, '高密'), (453, '高青'),
    (454, '高唐'),
    (455, '高要'), (456, '高邑'), (457, '高邮'), (458, '高州'), (459, '巩义'), (460, '广昌'), (461, '广德'),
    (462, '广丰'),
    (463, '广宁'), (464, '广饶'), (465, '光泽'), (466, '灌南'), (467, '冠县'), (468, '灌云'), (469, '贵溪'),
    (470, '古田'),
    (471, '固镇'), (472, '海安'), (473, '海丰'), (474, '海门'), (475, '海宁'), (476, '海盐'), (477, '海阳'),
    (478, '含山'),
    (479, '合川'), (480, '横峰'), (481, '横县'), (482, '和平'), (483, '鹤山'), (484, '和县'), (485, '洪泽'),
    (486, '华安'),
    (487, '桦甸'), (488, '怀集'), (489, '怀宁'), (490, '怀远'), (491, '桓台'), (492, '化州'), (493, '惠安'),
    (494, '会昌'),
    (495, '惠东'), (496, '惠来'), (497, '惠民'), (498, '湖口'), (499, '呼兰'), (500, '霍邱'), (501, '霍山'),
    (502, '户县'),
    (503, '建德'), (504, '江都'), (505, '江津'), (506, '将乐'), (507, '江山'), (508, '姜堰'), (509, '江阴'),
    (510, '建湖'),
    (511, '建宁'), (512, '建瓯'), (513, '建阳'), (514, '吉安'), (515, '蛟河'), (516, '蕉岭'), (517, '胶南'),
    (518, '胶州'),
    (519, '嘉善'), (520, '嘉祥'), (521, '揭东'), (522, '界首'), (523, '揭西'), (524, '即墨'), (525, '靖安'),
    (526, '旌德'),
    (527, '井冈山'), (528, '靖江'), (529, '景宁'), (530, '泾县'), (531, '井陉'), (532, '金湖'), (533, '晋江'),
    (534, '金门'), (535, '晋宁'), (536, '金坛'), (537, '金堂'), (538, '进贤'), (539, '金溪'), (540, '金乡'),
    (541, '缙云'),
    (542, '金寨'), (543, '晋州'), (544, '吉水'), (545, '九江'), (546, '九台'), (547, '绩溪'), (548, '济阳'),
    (549, '济源'),
    (550, '鄄城'), (551, '莒南'), (552, '句容'), (553, '莒县'), (554, '巨野'), (555, '开化'), (556, '开平'),
    (557, '开县'),
    (558, '开阳'), (559, '康平'), (560, '垦利'), (561, '昆山'), (562, '来安'), (563, '莱西'), (564, '莱阳'),
    (565, '莱州'),
    (566, '郎溪'), (567, '蓝田'), (568, '兰溪'), (569, '乐安'), (570, '乐昌'), (571, '雷州'), (572, '乐陵'),
    (573, '乐平'),
    (574, '乐清'), (575, '乐亭'), (576, '连城'), (577, '梁平'), (578, '梁山'), (579, '莲花'), (580, '连江'),
    (581, '廉江'),
    (582, '连南'), (583, '连平'), (584, '连山'), (585, '涟水'), (586, '连州'), (587, '辽中'), (588, '黎川'),
    (589, '利津'),
    (590, '临安'), (591, '灵璧'), (592, '灵寿'), (593, '陵县'), (594, '临海'), (595, '临清'), (596, '临泉'),
    (597, '临朐'),
    (598, '临沭'), (599, '临邑'), (600, '溧水'), (601, '柳城'), (602, '柳江'), (603, '浏阳'), (604, '利辛'),
    (605, '溧阳'),
    (606, '隆安'), (607, '龙川'), (608, '龙海'), (609, '龙口'), (610, '龙门'), (611, '龙南'), (612, '龙泉'),
    (613, '龙游'),
    (614, '栾城'), (615, '栾川'), (616, '滦南'), (617, '滦县'), (618, '陆丰'), (619, '陆河'), (620, '庐江'),
    (621, '罗定'),
    (622, '洛宁'), (623, '罗源'), (624, '鹿泉'), (625, '禄劝'), (626, '芦溪'), (627, '鹿寨'), (628, '马山'),
    (629, '梅县'),
    (630, '蒙城'), (631, '孟津'), (632, '蒙阴'), (633, '孟州'), (634, '明光'), (635, '明溪'), (636, '闽侯'),
    (637, '闽清'),
    (638, '木兰'), (639, '南安'), (640, '南澳'), (641, '南城'), (642, '南川'), (643, '南丰'), (644, '南靖'),
    (645, '南康'),
    (646, '南陵'), (647, '南雄'), (648, '宁都'), (649, '宁国'), (650, '宁海'), (651, '宁化'), (652, '宁津'),
    (653, '宁乡'),
    (654, '宁阳'), (655, '农安'), (656, '磐安'), (657, '磐石'), (658, '沛县'), (659, '蓬莱'), (660, '彭水'),
    (661, '彭泽'),
    (662, '彭州'), (663, '平度'), (664, '平和'), (665, '平湖'), (666, '屏南'), (667, '平山'), (668, '平潭'),
    (669, '平阳'),
    (670, '平阴'), (671, '平邑'), (672, '平原'), (673, '平远'), (674, '郫县'), (675, '邳州'), (676, '鄱阳'),
    (677, '浦城'),
    (678, '浦江'), (679, '蒲江'), (680, '普兰店'), (681, '普宁'), (682, '迁安'), (683, '潜山'), (684, '铅山'),
    (685, '迁西'), (686, '启东'), (687, '齐河'), (688, '綦江'), (689, '祁门'), (690, '清流'), (691, '青田'),
    (692, '清新'),
    (693, '青阳'), (694, '庆元'), (695, '庆云'), (696, '清镇'), (697, '青州'), (698, '沁阳'), (699, '邛崃'),
    (700, '栖霞'),
    (701, '全椒'), (702, '全南'), (703, '曲阜'), (704, '曲江'), (705, '饶平'), (706, '仁化'), (707, '融安'),
    (708, '荣昌'),
    (709, '荣成'), (710, '融水'), (711, '如东'), (712, '如皋'), (713, '瑞安'), (714, '瑞昌'), (715, '瑞金'),
    (716, '乳山'),
    (717, '汝阳'), (718, '乳源'), (719, '三江'), (720, '三门'), (721, '诏安'), (722, '上高'), (723, '上杭'),
    (724, '商河'),
    (725, '上栗'), (726, '上林'), (727, '上饶'), (728, '上犹'), (729, '上虞'), (730, '尚志'), (731, '邵武'),
    (732, '绍兴'),
    (733, '沙县'), (734, '嵊泗'), (735, '嵊州'), (736, '莘县'), (737, '深泽'), (738, '歙县'), (739, '射阳'),
    (740, '石城'),
    (741, '石林'), (742, '石狮'), (743, '石台'), (744, '始兴'), (745, '石柱'), (746, '寿光'), (747, '寿宁'),
    (748, '寿县'),
    (749, '双城'), (750, '双流'), (751, '舒城'), (752, '舒兰'), (753, '顺昌'), (754, '沭阳'), (755, '泗洪'),
    (756, '四会'),
    (757, '泗水'), (758, '泗县'), (759, '泗阳'), (760, '嵩明'), (761, '松溪'), (762, '嵩县'), (763, '松阳'),
    (764, '遂昌'),
    (765, '遂川'), (766, '睢宁'), (767, '濉溪'), (768, '遂溪'), (769, '宿松'), (770, '宿豫'), (771, '太仓'),
    (772, '太和'),
    (773, '泰和'), (774, '太湖'), (775, '泰宁'), (776, '台山'), (777, '泰顺'), (778, '泰兴'), (779, '郯城'),
    (780, '唐海'),
    (781, '滕州'), (782, '天长'), (783, '天台'), (784, '桐城'), (785, '铜鼓'), (786, '通河'), (787, '铜梁'),
    (788, '铜陵'),
    (789, '桐庐'), (790, '潼南'), (791, '铜山'), (792, '桐乡'), (793, '通州'), (794, '瓦房店'), (795, '万安'),
    (796, '望城'), (797, '望江'), (798, '万年'), (799, '万载'), (800, '微山'), (801, '文成'), (802, '文登'),
    (803, '翁源'),
    (804, '温岭'), (805, '汶上'), (806, '温县'), (807, '涡阳'), (808, '五常'), (809, '武城'), (810, '吴川'),
    (811, '无棣'),
    (812, '五河'), (813, '芜湖'), (814, '五华'), (815, '无极'), (816, '吴江'), (817, '五莲'), (818, '武隆'),
    (819, '武鸣'),
    (820, '武宁'), (821, '武平'), (822, '巫山'), (823, '无为'), (824, '巫溪'), (825, '武义'), (826, '武夷山'),
    (827, '婺源'), (828, '武陟'), (829, '峡江'), (830, '夏津'), (831, '象山'), (832, '响水'), (833, '仙居'),
    (834, '仙游'),
    (835, '萧县'), (836, '霞浦'), (837, '息烽'), (838, '新安'), (839, '新昌'), (840, '信丰'), (841, '新丰'),
    (842, '新干'),
    (843, '兴国'), (844, '兴化'), (845, '兴宁'), (846, '行唐'), (847, '荥阳'), (848, '星子'), (849, '辛集'),
    (850, '新建'),
    (851, '新津'), (852, '新乐'), (853, '新民'), (854, '新密'), (855, '新泰'), (856, '新兴'), (857, '新沂'),
    (858, '信宜'),
    (859, '新郑'), (860, '休宁'), (861, '秀山'), (862, '修水'), (863, '修文'), (864, '修武'), (865, '寻甸'),
    (866, '寻乌'),
    (867, '徐闻'), (868, '盱眙'), (869, '阳春'), (870, '阳东'), (871, '阳谷'), (872, '阳山'), (873, '阳信'),
    (874, '阳西'),
    (875, '扬中'), (876, '偃师'), (877, '延寿'), (878, '兖州'), (879, '伊川'), (880, '宜丰'), (881, '宜黄'),
    (882, '依兰'),
    (883, '宜良'), (884, '沂南'), (885, '英德'), (886, '颍上'), (887, '沂水'), (888, '义乌'), (889, '黟县'),
    (890, '宜兴'),
    (891, '弋阳'), (892, '宜阳'), (893, '沂源'), (894, '仪征'), (895, '永安'), (896, '永川'), (897, '永春'),
    (898, '永登'),
    (899, '永定'), (900, '永丰'), (901, '永吉'), (902, '永嘉'), (903, '永康'), (904, '邕宁'), (905, '永泰'),
    (906, '永新'),
    (907, '永修'), (908, '尤溪'), (909, '酉阳'), (910, '元氏'), (911, '禹城'), (912, '于都'), (913, '岳西'),
    (914, '余干'),
    (915, '玉环'), (916, '余江'), (917, '郁南'), (918, '云安'), (919, '郓城'), (920, '云和'), (921, '云霄'),
    (922, '云阳'),
    (923, '玉山'), (924, '榆树'), (925, '鱼台'), (926, '玉田'), (927, '余姚'), (928, '榆中'), (929, '赞皇'),
    (930, '增城'),
    (931, '张家港'), (932, '漳平'), (933, '漳浦'), (934, '章丘'), (935, '樟树'), (936, '沾化'), (937, '赵县'),
    (938, '招远'), (939, '正定'), (940, '政和'), (941, '柘荣'), (942, '中牟'), (943, '忠县'), (944, '周宁'),
    (945, '周至'),
    (946, '庄河'), (947, '诸城'), (948, '诸暨'), (949, '紫金'), (950, '资溪'), (951, '邹城'), (952, '邹平'),
    (953, '遵化'))

district_dictionary = {}
for item in district_list:
    district_dictionary[item[0]] = item[1]
