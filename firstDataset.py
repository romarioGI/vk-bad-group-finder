def __set_tag(screen_names, tag_name):
    return dict(map(lambda s: (s, tag_name), screen_names))


opposite_group_screen_names = ['teamnavalny', 'navalny.group', 'navalny_live', 'vesna_democrat',
                               'rusrise', 'european_path', 'oppositionofrussia',
                               'limonov_eduard', 'navalnyclub', 'corrupcia_in_russia', 'rf_pravda', 'rospil',
                               'youth_civsoc', 'civsociety', 'lpr_vk', 'club463266', 'against_the_system_ua',
                               'vopros_naz_bez', 'edrovvedro', 'yabloko_ru', 'ruopp', 'dimon_ekat', 'corrupcia_rf']
opposite_tag = 'OPPOSITE'
opposite_dataset = __set_tag(opposite_group_screen_names, opposite_tag)

erotic_group_screen_names = ['tutsexx', 'posliye', 'pornobrazzersvk', 'nu_art_erotica',
                             'erotique_journal', 'ledesirerotique', 'derzkach', 'eroticheskie_gifki',
                             'sexliborg', 'vids_dolboyoba', 'pornofamiliya', 'pornhub_porn_hub',
                             'club136599045', 'aliporn', 'iwantyou', 'posloe', 'my_name_and_plhk', 'meass', 'xyduwki',
                             'cekc_sex', 'so.vkusom1', 'erotical_fantasy', 'podposyar', '50sogv', 'vulgar76',
                             'tf.erotica']
erotic_tag = 'EROTIC'
erotic_dataset = __set_tag(erotic_group_screen_names, erotic_tag)

non_group_screen_names = ['yarchat', 'baza_chto_gde_kogda', 'voprosi.svoya.igra',
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
                          'wgpubg', 'club144652144', 'club149838562', 'bigdataconf', 'coub', 'club30100935', 'nt_manic',
                          'krunpub'
                          ]
non_tag = 'NON'
non_dataset = __set_tag(non_group_screen_names, non_tag)

dataset = dict(opposite_dataset, **erotic_dataset, **non_dataset)
