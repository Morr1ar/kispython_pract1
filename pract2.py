'''# 5.7
print('№ 5.7')

from functools import cache

# Словарь похожих букв (английские : русские)
SIMILAR_LETTERS = {'a':'а', 'e':'е', 'o':'о', 'p':'р', 'c':'с', 'x':'х', 'y':'у'}

def is_similar(a, b):
    if a == b:
        return True
    if a in SIMILAR_LETTERS and SIMILAR_LETTERS[a] == b:
        return True
    if b in SIMILAR_LETTERS and SIMILAR_LETTERS[b] == a:
        return True
    return False

@cache
def lev_dist_custom(a, b):
    if not a or not b:
        return max(len(a), len(b))
    
    # Проверяем транспозицию
    if len(a) >= 2 and len(b) >= 2:
        if a[0] == b[1] and a[1] == b[0]:
            transposition_cost = 1 + lev_dist_custom(a[2:], b[2:])
        else:
            transposition_cost = 999999999
    else:
        transposition_cost = 999999999
    
    # Замена
    if a[0] == b[0]:
        return lev_dist_custom(a[1:], b[1:])
    elif is_similar(a[0], b[0]):
        return lev_dist_custom(a[1:], b[1:])
    
    
    insert_cost = 1 + lev_dist_custom(a, b[1:])
    delete_cost = 1 + lev_dist_custom(a[1:], b)
    replace_cost = 1 + lev_dist_custom(a[1:], b[1:])
    
    return min(insert_cost, delete_cost, replace_cost, transposition_cost)

def find_best_correction(word, dictionary):
    if word in dictionary:
        return word, 0
    
    best_word = word
    best_dist = 999999999
    best_popularity = -1
    
    for dict_word, popularity in dictionary.items():
        dist = lev_dist_custom(word, dict_word)
        
        if dist == 1:
            if popularity > best_popularity:
                best_word = dict_word
                best_dist = dist
                best_popularity = popularity
            elif best_dist > 1:
                best_word = dict_word
                best_dist = dist
                best_popularity = popularity
        elif dist == 2 and best_dist > 1:
            if popularity > best_popularity:
                best_word = dict_word
                best_dist = dist
                best_popularity = popularity
    
    return best_word, best_dist

def spell_advanced(text):
    dictionary = {}
    with open('words.txt', 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            word, freq = parts[0], int(parts[1])
            dictionary[word] = freq
    
    words = text.split()
    corrected_words = []
    
    for word in words:
        corrected, dist = find_best_correction(word, dictionary)
        corrected_words.append(corrected)
    
    return ' '.join(corrected_words)

print(spell_advanced('помоему я напесал усё правильна'))

print(f"lev_dist_custom('написaл', 'написал') = {lev_dist_custom('написaл', 'написал')}")# 0 (англ a : рус а)
print(f"lev_dist_custom('написаа', 'написал') = {lev_dist_custom('написаа', 'написал')}")# 1
print(f"lev_dist_custom('написла', 'написал') = {lev_dist_custom('написла', 'написал')}")# 1
'''


# 7.4
print('№ 7.4')
import re
import os

class WebQuestGenerator:
    def __init__(self):
        self.rooms = {}

    def parse_game_text(self, text):
        room_p = re.compile(r'\[ROOM\s+(\w+)\]\s*(.*)')
        act_p = re.compile(r'\[ACT\s+(\w+)\]\s*(.*)')
        
        current_room = None
        for line in text.strip().split('\n'):
            line = line.strip()
            if not line:
                continue

            room_m = room_p.match(line)
            if room_m:
                label, title = room_m.groups()
                current_room = {'title': title, 'desc': [], 'actions': []}
                self.rooms[label] = current_room
            elif line.startswith('[DESC]'):
                current_room['desc'].append(line.replace('[DESC]', '').strip())
            elif act_p.match(line):
                target, act_text = act_p.match(line).groups()
                current_room['actions'].append((act_text, target))
        

    def generate_site(self, output_folder="web_game_74"):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        style = """
        <style>
            body {
                font-family: 'Segoe UI', sans-serif;
                background-color: #482121;
                color: #fffe00;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
            }
            .room-card {
                background: #53140b;
                padding: 40px;
                border-radius: 15px;
                max-width: 600px;
                width: 60%;
                border: 5px solid #83691c;
            }
            h1 {
                color: #ffb300;
                text-align: center;
                border: 2px solid #ffbf00;
                padding: 15px;
                border-radius: 15px;
            }
            .description {
                font-size: 1.15em;
                line-height: 1.7;
                text-align: justify;
            }

            .actions {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                padding: 0;
            }
            .actions li { list-style: none; }
            .actions a {
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
                text-decoration: none;
                color: #e5dea9;
                background: #73420f;
                height: 60px;
                padding: 10px;
                border-radius: 15px;
                border: 2px solid #ffbf00;
                transition: all 0.3s ease;
                font-weight: bold;
            }
            .actions a:hover {
                background: #a05d18;
            }
        </style>
        """



        def mapp(number):
            for label, data in self.rooms.items():
                content = f"<div class='room-card'><h1>{data['title']}</h1>"
                content += "<div class='description'>"
                for line in data['desc']:
                    content += f"<p>{line}</p>"
                content += "</div>"

                content += "<ul class='actions'>"
                for act_text, target in data['actions']:
                    clean_text = re.sub(r'\(#\d+\)', '', act_text).strip()
                    content += f'<li><a href="{target}.html">{clean_text}</a></li>'
                content += "</ul></div>"
            return f'<li>{number}</li>'

        content2 += "<div><ul>{mapp(1)}</ul></div>"
        

        for label, data in self.rooms.items():
            content = f"<div class='room-card'><h1>{data['title']}</h1>"
            content += "<div class='description'>"
            for line in data['desc']:
                content += f"<p>{line}</p>"
            content += "</div>"

            content += "<ul class='actions'>"
            for act_text, target in data['actions']:
                clean_text = re.sub(r'\(#\d+\)', '', act_text).strip()
                content += f'<li><a href="{target}.html">{clean_text}</a></li>'
            content += "</ul></div>"



            for i in range(4):
                content += "<div><ul>"
                for j in range(4):
                    content += f'<li>{i * 4 + j + 1}</li>'
                content += "</ul></div>"




            full_html = f"<html><head><meta charset='utf-8'><title>{data['title']}</title>{style}</head><body>{content}</body></html>"
            with open(f"{output_folder}/{label}.html", "w", encoding="utf-8") as f:
                f.write(full_html)

        print(f"Проект создан! Откройте {output_folder}/1.html")

game_content = """
[ROOM 1] Комната #1
[DESC] Вы стоите у высоких, древних ворот, ведущих в лабиринт. Воздух прохладный, слышится эхо воды.
[ACT 2] Проход на запад (#2)

[ROOM 2] Комната #2
[DESC] Узкая комната с древними светящимися рунами. Кажется, каждая руна несёт сообщение.
[ACT 3] Проход на запад (#3)
[ACT 1] Проход на восток (#1)

[ROOM 3] Комната #3
[DESC] Подземное озеро. Вода мерцает зелёным светом. В центре стоит каменный алтарь.
[ACT 4] Проход на север (#4)
[ACT 2] Проход на восток (#2)

[ROOM 4] Комната #4
[DESC] Огромная зала с колоннами из чёрного камня и вечным огнём.
[ACT 5] Проход на север (#5)
[ACT 3] Проход на юг (#3)

[ROOM 5] Комната #5
[DESC] Слышен шёпот ветра. На стенах старинные ковры с легендами.
[ACT 4] Проход на юг (#4)
[ACT 6] Проход на восток (#6)

[ROOM 6] Комната #6
[DESC] Воздух пахнет мёдом и лавандой. Повсюду зеркала, искажающие реальность.
[ACT 15] Проход на север (#15)
[ACT 7] Проход на юг (#7)
[ACT 5] Проход на запад (#5)
[ACT 11] Проход на восток (#11)

[ROOM 7] Комната #7
[DESC] Древняя библиотека. Полки уходят высоко вверх в темноту.
[ACT 6] Проход на север (#6)
[ACT 8] Проход на восток (#8)

[ROOM 8] Комната #8
[DESC] Тронный зал. Пустой трон окружён безмолвными статуями стражей.
[ACT 7] Проход на запад (#7)
[ACT 9] Проход на восток (#9)

[ROOM 9] Комната #9
[DESC] Звук водопада. Брызги создают радугу в свете кристаллов.
[ACT 10] Проход на юг (#10)
[ACT 8] Проход на запад (#8)

[ROOM 10] Комната #10
[DESC] Влажная пещера с наскальными рисунками древних цивилизаций.
[ACT 9] Проход на север (#9)

[ROOM 11] Комната #11
[DESC] Подземный сад со светящимися растениями. Здесь очень спокойно.
[ACT 6] Проход на запад (#6)
[ACT 12] Проход на восток (#12)

[ROOM 12] Комната #12
[DESC] Стены украшены мозаиками. В центре бьёт кристально чистый фонтан.
[ACT 13] Проход на север (#13)
[ACT 11] Проход на запад (#11)

[ROOM 13] Комната #13
[DESC] Древний храм. Воздух наэлектризован вокруг центрального монолита.
[ACT 12] Проход на юг (#12)
[ACT 14] Проход на запад (#14)

[ROOM 14] Комната #14
[DESC] Комната покрыта мхом. В центре растёт дерево, чьи корни уходят в бездну.
[ACT 13] Проход на восток (#13)

[ROOM 15] Комната #15
[DESC] Комната залита светом кристаллов. Перед вами сияющий белый портал.
[ACT win] Проход на север (ВЫХОД)
[ACT 6] Проход на юг (#6)
[ACT 16] Проход на запад (#16)

[ROOM 16] Комната #16
[DESC] Кристаллы поют при прикосновении. На плите высечена полная карта лабиринта.
[ACT 15] Проход на восток (#15)

[ROOM win] ФИНАЛ
[DESC] Вы шагнули в портал... Свет ослепил вас, и через мгновение вы почувствовали запах свежей травы и тепло солнца. Вы свободны!
"""

quest = WebQuestGenerator()
quest.parse_game_text(game_content)
quest.generate_site()
















'''

def check_dead_ends(rooms, win_label="win"):
    # Находим все комнаты, из которых нельзя достичь win_label
    no_path_to_win = []
    back_label = -1
    for label in rooms:
        if label == win_label:
            continue

        

        
        # Поиск в глубину, можно ли достичь win_label
        visited = set()
        stack = [label]
        
        reached_win = False
        
        while stack and not reached_win:
            print(stack, visited)
            current = stack.pop()
            if current in visited:
                continue
            visited.add(current)
            
            if current == win_label:
                reached_win = True
                break
                
            if current in rooms:
                for _, target in rooms[current]['actions']:
                    if target == back_label:
                        continue
                    if target not in visited:
                        stack.append(target)
            back_label = current
        
        if not reached_win:
            no_path_to_win.append(label)
    
    # Вывод результата
    if no_path_to_win:
        print(f"Обнаружены тупики: {no_path_to_win}")
    else:
        print("Тупиков не обнаружено")
    
    return no_path_to_win

dead_ends = check_dead_ends(quest.rooms, "win")

'''
