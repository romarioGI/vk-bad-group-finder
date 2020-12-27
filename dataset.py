from abstractClassifier import OPPOSITE_TAG, EROTIC_TAG, OTHER_TAG
from vkApiWrapper import VkApiWrapper

opposite_group_screen_names = ['teamnavalny', 'navalny.group', 'navalny_live', 'vesna_democrat',
                               'rusrise', 'european_path', 'oppositionofrussia',
                               'limonov_eduard', 'navalnyclub', 'corrupcia_in_russia', 'rf_pravda', 'rospil',
                               'youth_civsoc', 'civsociety', 'lpr_vk', 'club463266', 'against_the_system_ua',
                               'vopros_naz_bez', 'edrovvedro', 'yabloko_ru', 'ruopp', 'dimon_ekat', 'corrupcia_rf',
                               'kprf_oz', 'corrupcia_rf', 'club1528146', 'clublevayoppoziciy', 'newopposition_official',
                               'anticrisismeeting', 'realopposition'
                               ]

erotic_group_screen_names = ['tutsexx', 'posliye', 'pornobrazzersvk', 'nu_art_erotica',
                             'erotique_journal', 'ledesirerotique', 'derzkach', 'eroticheskie_gifki',
                             'sexliborg', 'vids_dolboyoba', 'pornofamiliya', 'pornhub_porn_hub',
                             'club136599045', 'aliporn', 'iwantyou', 'posloe', 'my_name_and_plhk', 'meass', 'xyduwki',
                             'cekc_sex', 'so.vkusom1', 'erotical_fantasy', 'podposyar', '50sogv', 'vulgar76',
                             'tf.erotica', 'sexy_world_one', 'paradise_for_men_01', 'erotic_pics', 'seksualnye_modeli',
                             'nsk_models', 'eros_pub', 'erotica_so_vkusom']

other_group_screen_names = ['yarchat', 'baza_chto_gde_kogda', 'voprosi.svoya.igra',
                            'math.uniyar.contest', 'yaroslavl_state_university', 'just_str',
                            'tproger', 'kuplinovplay', 'olimpiprofi', 'citiesskylines', 'openyarru',
                            'cerceau', 'ctranno', 'autoclub76', 'demid.icpc', 'postgrad76',
                            'questions_of_chgk', 'acmnarfu', 'kinoteatr.rodina.yaroslavl',
                            'roboshturm', 'catcafe_yar', 'istok_yargu', 'yaracm', 'math_yargu',
                            'vsalbum', 'mathcontent', 'transport76', 'strikalonp', 'abivt',
                            'studclub_yargu', 'cis_yarsu', 'club_champion_yaroslavl', 'nercnews',
                            'olymp_maths', 'acmmisis', 'naukadetiyar', 'sdushor10yar', 'math_dosug',
                            'typ_math', 'yar500600', 'demidinfo', 'akvelon_russia',
                            'yaroslavl_school_86', 'honorru', 'lays_russia', 'msi_russia',
                            'scholarships', 'strikalogroup', 'vkteam', 'stigmataworld',
                            'yandex.academy', 'yandexbrowser', 'serezhadelal', 'rakovar_yar',
                            'retro_yar', 'moscowicpc', 'overhear_yargu', 'nutbar_games', 'yarkzc',
                            'yar.show', 'cryptandcod', 'tensor_company', 'yarsladostiiradosti',
                            'codeforces', 'npokrista', 'uniyar_abitur', 'demidpoint76', 'vktexbot',
                            'nbyargupublic', 'spguide', 'botaninvestments', 'labmedia_su',
                            'snoivtuniyar', 'podvezu_ysu', 'snomath', 'crypto_nsu', 'komnata163',
                            'psy_sluzhba', 'public178021929', 'beauty_bar_ed_style',
                            'confirmit_yaroslavl', 'event133646054', 'devbattle.official',
                            'club44019163', 'vii_ko', 'mykorean', 'jfestival', 'nippon_gatari', '5minutestotokyo',
                            'howtonihongo', 'jumoreski', 'bmstu_ctf', 'club116038017', 'gianluigi_buffon_the_best',
                            'fairwindpage', 'tachikotv', 'public10933209', 'newartphotography', 'v.kote',
                            'humor_schrodinger', 'stopagent', 'livetasty', 'tripdiary', 'sport_stat', 'transurfing_vk',
                            'homeideaz', 'mir_vkusa', 'ti_eto_mojesh', 'tumengranat', 'tnshow', 'club84999705',
                            'sisvideo', 'club32464921', 'club127781518', 'catism', 'pozor', 'dubsteplight', 'just_cook',
                            'kta_travel_ekb', 'zmshzmsh', 'mogilat_ph', 'pixel_bldjad', 'malyakikalyaki', 'sugrobart',
                            'kazanmath', 'kvant_tournament', 'math_games', 'tichiypiket', 'foto.blog', 'neva33',
                            'wgpubg', 'club144652144', 'club149838562', 'bigdataconf', 'coub', 'club30100935',
                            'nt_manic',
                            'krunpub', 'bad_novosti', 'tennissss', 'pod83', 'pikabu', 'mensrecipes', 'programmistov',
                            'for.mens', 'smexo', 'adkuhnya', 'nice_food', 'litrpg_book'
                            ]


def get_screen_name_dataset():
    for s_n in opposite_group_screen_names:
        yield s_n, OPPOSITE_TAG

    for s_n in erotic_group_screen_names:
        yield s_n, EROTIC_TAG

    for s_n in other_group_screen_names:
        yield s_n, OTHER_TAG


def make(vkApiWrapper: VkApiWrapper, use_extend_group_info=True):
    screen_name_dataset = dict(get_screen_name_dataset())
    if use_extend_group_info:
        groups_info = vkApiWrapper.get_groups_extended_info(list(screen_name_dataset.keys()))
    else:
        groups_info = vkApiWrapper.get_groups_info(list(screen_name_dataset.keys()))
    tags = [screen_name_dataset[g_i['screen_name']] for g_i in groups_info]
    return groups_info, tags
