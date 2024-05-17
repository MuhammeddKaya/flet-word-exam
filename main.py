import flet as ft
import sqlite3
import random

def get_word_groups(words, group_size=5):
    for i in range(0, len(words), group_size):
        yield words[i:i + group_size]

def matching_game_page(page, test_table_name):
    conn = sqlite3.connect('kelimeler.db')
    cur = conn.cursor()
    cur.execute(f"SELECT English, Türkce FROM {test_table_name}")
    words = cur.fetchall()
    conn.close()

    word_groups = list(get_word_groups(words))
    current_group_index = [0]
    matched_pairs = []
    selected_words = []

    def show_next_group():
        if current_group_index[0] < len(word_groups):
            current_group = word_groups[current_group_index[0]]
            display_words(current_group)
        else:
            complete_test()

    def display_words(words):
        page.controls.clear()

        english_words = [word[0] for word in words]
        turkish_words = [word[1] for word in words]

        random.shuffle(english_words)
        random.shuffle(turkish_words)

        english_buttons = [
            ft.ElevatedButton(text=word, on_click=lambda e, word=word: on_word_selected(word, "english"), width=150, height=50)
            for word in english_words]
        turkish_buttons = [
            ft.ElevatedButton(text=word, on_click=lambda e, word=word: on_word_selected(word, "turkish"), width=150, height=50)
            for word in turkish_words]

        page.add(ft.Row([ft.Column(english_buttons), ft.Column(turkish_buttons)], alignment=ft.MainAxisAlignment.CENTER))

        exit_button = ft.ElevatedButton(text="Testten Çık", on_click=lambda e: complete_test(), width=180, height=50)
        page.add(ft.Row([exit_button], alignment=ft.MainAxisAlignment.CENTER))
        page.update()

    def on_word_selected(word, language):
        selected_words.append((word, language))

        if len(selected_words) == 2:
            if selected_words[0][1] != selected_words[1][1]:  # Aynı dilde değilse
                english_word = selected_words[0][0] if selected_words[0][1] == "english" else selected_words[1][0]
                turkish_word = selected_words[0][0] if selected_words[0][1] == "turkish" else selected_words[1][0]

                if is_correct_pair(english_word, turkish_word):
                    matched_pairs.append((english_word, turkish_word))
                    update_word_colors(english_word, turkish_word, "green")
                else:
                    update_word_colors(english_word, turkish_word, "red")

            selected_words.clear()

        if len(matched_pairs) == 5:
            current_group_index[0] += 1
            matched_pairs.clear()  # Yeni kelime grubu için eşleşen kelimeleri temizle
            show_next_group()

    def is_correct_pair(english_word, turkish_word):
        return any(english_word == word[0] and turkish_word == word[1] for word in words)

    def update_word_colors(english_word, turkish_word, color):
        for control in page.controls[0].controls[0].controls:
            if control.text == english_word:
                control.bgcolor = color
                if color == "green":
                    control.on_click = None
        for control in page.controls[0].controls[1].controls:
            if control.text == turkish_word:
                control.bgcolor = color
                if color == "green":
                    control.on_click = None
        page.update()

    def complete_test():
        page.controls.clear()
        test_type_page(page, test_table_name)  # Test türü sayfasına geri dön

    show_next_group()

def finding_game_page(page, test_table_name):
    conn = sqlite3.connect('kelimeler.db')
    cur = conn.cursor()
    cur.execute(f"SELECT English, Türkce FROM {test_table_name}")
    words = cur.fetchall()
    conn.close()

    current_index = [0]  # Mevcut kelime indeksi
    score = [0]  # Başlangıçta skor 0

    score_display = ft.Text(value=f"Skor: {score[0]}", size=20, color=0x0000FF)

    def show_next_word():
        if current_index[0] < len(words):
            english_word, turkish_word = words[current_index[0]]
            options = [english_word] + random.sample([word[0] for word in words if word[0] != english_word], 3)
            random.shuffle(options)
            update_question(turkish_word, options, english_word)
        else:
            complete_test()

    def update_question(turkish_word, options, correct_english):
        page.controls.clear()
        question = ft.Text(value=turkish_word, size=40)
        option_buttons = [
            ft.ElevatedButton(
                text=option,
                on_click=lambda e, opt=option: check_answer(opt, correct_english),
                width=180,
                height=50
            ) for option in options
        ]
        exit_button = ft.ElevatedButton(text="Testten Çık", on_click=lambda e: complete_test(), width=180, height=50)
        page.add(score_display)
        page.add(question)
        for btn in option_buttons:
            page.add(btn)
        page.add(exit_button)
        page.update()

    def check_answer(selected_option, correct_answer):
        if selected_option == correct_answer:
            score[0] += 4
            score_display.value = f"Skor: {score[0]}"
            page.update()
            current_index[0] += 1
            show_next_word()
        else:
            score[0] -= 1
            score_display.value = f"Skor: {score[0]}"
            page.update()
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Yanlış cevap, tekrar deneyin!")))

    def complete_test():
        page.controls.clear()
        test_type_page(page, test_table_name)  # Test türü sayfasına geri dön

    show_next_word()

def learning_game_page(page, test_table_name):
    print("Kelime öğrenme modülü başlatıldı.")
    conn = sqlite3.connect('kelimeler.db')
    cur = conn.cursor()
    cur.execute(f"SELECT English, Türkce FROM {test_table_name}")
    words = cur.fetchall()
    conn.close()

    current_index = [0]  # Mevcut kelime indeksi

    def update_display():
        if 0 <= current_index[0] < len(words):
            english_word, turkish_word = words[current_index[0]]
            english_display.value = english_word
            turkish_display.value = turkish_word
            page.update()

    def go_next_word(e):
        if current_index[0] < len(words) - 1:
            current_index[0] += 1
            update_display()

    def go_previous_word(e):
        if current_index[0] > 0:
            current_index[0] -= 1
            update_display()

    def exit_learning(e):
        page.controls.clear()
        test_type_page(page, test_table_name)

    english_display = ft.Text(value="", size=40, text_align=True)
    turkish_display = ft.Text(value="", size=30, color=0x808080, text_align=True)  # Gri renkli metin

    next_button = ft.ElevatedButton(text="Sonraki", on_click=go_next_word, width=100, height=50)
    previous_button = ft.ElevatedButton(text="Önceki", on_click=go_previous_word, width=100, height=50)
    exit_button = ft.ElevatedButton(text="Çık", on_click=exit_learning, width=100, height=50)

    navigation_row = ft.Row([previous_button, next_button], alignment=ft.MainAxisAlignment.CENTER)
    page.add(ft.Row([english_display], alignment=ft.MainAxisAlignment.CENTER))
    page.add(ft.Row([turkish_display], alignment=ft.MainAxisAlignment.CENTER))
    page.add(ft.Row([navigation_row], alignment=ft.MainAxisAlignment.CENTER))
    page.add(ft.Row([exit_button], alignment=ft.MainAxisAlignment.CENTER))

    update_display()

def main(page: ft.Page):
    page.title = "Kelime Ezberleme"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def check_item_clicked(e):
        e.control.checked = not e.control.checked
        page.update()

    page.appbar = ft.AppBar(
        title=ft.Text("Yds kelime Ezber", text_align=ft.TextAlign.CENTER),
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.IconButton(ft.icons.APPS),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="Item 1"),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(
                        text="Checked item", checked=False, on_click=check_item_clicked
                    ),
                ]
            ),
        ],
    )

    page.window_width = 400
    page.window_height = 500

    def go_to_tests(e):
        page.controls.clear()
        test_selection_page(page)

    def go_to_learning(e):
        page.controls.clear()
        learning_page(page)

    test_button = ft.ElevatedButton(text="TEST SEÇME", on_click=go_to_tests, width=300, height=50)
    start_button = ft.ElevatedButton(text="HIZLI BAŞLA", on_click=go_to_tests, width=300, height=50)
    learned_button = ft.ElevatedButton(text="ÖĞRENDİĞİM KELİMELER", on_click=go_to_learning, width=300, height=50)

    page.add(ft.Column([test_button, start_button, learned_button]))

def test_selection_page(page):
    conn = sqlite3.connect('kelimeler.db')
    cur = conn.cursor()
    cur.execute("SELECT TableName, TotalWordsCount FROM TableInfo")
    tests = cur.fetchall()
    conn.close()

    def go_back(e):
        page.controls.clear()
        main(page)

    def on_test_selected(e, test_table_name):
        page.controls.clear()
        test_type_page(page, test_table_name)

    test_cards = []
    for test in tests:
        test_table_name, total_words = test
        card = ft.Card(
            content=ft.Column(
                [
                    ft.Text(f"{test_table_name}", weight="bold", size=16),
                    ft.Text(f"{total_words} Kelime", size=14),
                    ft.ElevatedButton(
                        text="Seç",
                        on_click=lambda e, test_table_name=test_table_name: on_test_selected(e, test_table_name),
                        width=100,
                        height=40
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10
            ),
            width=120,
            height=150,
            elevation=5,
            margin=10
        )
        test_cards.append(card)

    rows = []
    for i in range(0, len(test_cards), 3):
        row = ft.Row(controls=test_cards[i:i + 3], alignment=ft.MainAxisAlignment.SPACE_AROUND)
        rows.append(row)

    back_button = ft.ElevatedButton(bgcolor='#68c943', text="Geri Dön", on_click=go_back, width=180, height=40)

    page.add(ft.Column(controls=rows, alignment=ft.MainAxisAlignment.CENTER, scroll=ft.ScrollMode.ALWAYS, height=page.height * 0.75))
    page.add(ft.Row([back_button], alignment=ft.MainAxisAlignment.CENTER, scroll=ft.ScrollMode.ALWAYS))

def test_type_page(page, test_table_name):
    conn = sqlite3.connect('kelimeler.db')
    cur = conn.cursor()
    cur.execute(f"SELECT English, Türkce FROM {test_table_name}")
    words = cur.fetchall()
    conn.close()

    def start_matching_game(e):
        matching_game_page(page, test_table_name)

    def start_learning_game(e):
        learning_game_page(page, test_table_name)

    def start_finding_game(e):
        finding_game_page(page, test_table_name)

    def go_back(e):
        page.controls.clear()
        test_selection_page(page)

    testtype1 = ft.ElevatedButton(text="Kelime Öğrenme", on_click=start_learning_game, width=180, height=50)
    testtype2 = ft.ElevatedButton(text="Kelime Seçme", on_click=start_matching_game, width=180, height=50)
    testtype3 = ft.ElevatedButton(text="Kelime Bulma", on_click=start_finding_game, width=180, height=50)
    testtype4 = ft.ElevatedButton(text="Kelime Eşleştirme", on_click=start_matching_game, width=180, height=50)
    testtype5 = ft.ElevatedButton(text="Dinleme ve Seçme", on_click=lambda e: page.show_snack_bar(ft.SnackBar(content=ft.Text("Yakında Aktif Edilecek"))), width=180, height=50)
    testtype6 = ft.ElevatedButton(text="Dinleme ve Bulma", on_click=lambda e: page.show_snack_bar(ft.SnackBar(content=ft.Text("Yakında Aktif Edilecek"))), width=180, height=50)

    back_button = ft.ElevatedButton(text="Geri Dön", on_click=go_back, width=180, height=50)

    page.add(ft.Row([
        ft.Column([testtype1, testtype3, testtype5]),
        ft.Column([testtype2, testtype4, testtype6]),
    ], alignment=ft.MainAxisAlignment.CENTER))

    page.add(ft.Row([back_button], alignment=ft.MainAxisAlignment.CENTER))

def learning_page(page):
    def go_back(e):
        page.controls.clear()
        test_selection_page(page)

    learned_info = ft.Text(value="Burada öğrenilen kelimeler listelenecektir.")
    back_button = ft.ElevatedButton(text="Geri Dön", on_click=go_back, width=200, height=50)
    page.add(ft.Column([learned_info, back_button]))

ft.app(target=main)
