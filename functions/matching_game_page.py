import flet as ft
import sqlite3
import random

from functions.matching_game_page import matching_game_page
from functions.finding_game_page import finding_game_page


def matching_game_page(page, test_table_name):

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
            english_word, correct_turkish = words[current_index[0]]
            options = [correct_turkish] + random.sample([word[1] for word in words if word[1] != correct_turkish], 3)
            random.shuffle(options)
            update_question(english_word, options, correct_turkish)
        else:
            complete_test()

    def update_question(english_word, options, correct_turkish):
        page.controls.clear()
        question = ft.Text(value=english_word, size=40)
        option_buttons = [
            ft.ElevatedButton(
                text=option,
                on_click=lambda e, opt=option: check_answer(opt, correct_turkish),
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
            score[0] -= 2
            score_display.value = f"Skor: {score[0]}"
            page.update()
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Yanlış cevap, tekrar deneyin!")))

    def complete_test():
        page.controls.clear()
        test_type_page(page, test_table_name)  # Test türü sayfasına geri dön

    show_next_word()

