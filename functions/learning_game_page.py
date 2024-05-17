import flet as ft
import sqlite3
import random

from functions.matching_game_page import matching_game_page
from functions.finding_game_page import finding_game_page




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

    # Kelime gösterimi için Text widget'ları
    english_display = ft.Text(value="", size=40, text_align=True)
    turkish_display = ft.Text(value="", size=30, color=0x808080,text_align=True)  # Gri renkli metin

    # Navigasyon butonları
    next_button = ft.ElevatedButton(text="Sonraki", on_click=go_next_word, width=100, height=50)
    previous_button = ft.ElevatedButton(text="Önceki", on_click=go_previous_word, width=100, height=50)
    exit_button = ft.ElevatedButton(text="Çık", on_click=exit_learning, width=100, height=50)

    # Arayüzün düzenlenmesi
    navigation_row = ft.Row([previous_button, next_button], alignment=ft.MainAxisAlignment.CENTER)
    page.add(ft.Row([english_display], alignment=ft.MainAxisAlignment.CENTER))
    page.add(ft.Row([turkish_display], alignment=ft.MainAxisAlignment.CENTER))
    page.add(ft.Row([ navigation_row], alignment=ft.MainAxisAlignment.CENTER))
    page.add(ft.Row([exit_button], alignment=ft.MainAxisAlignment.CENTER))

    update_display()  # İlk kelimeyi göster

