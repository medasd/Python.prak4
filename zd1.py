import requests
import json
from typing import List, Dict

class RickAndMortyClient:
    BASE_URL = "https://rickandmortyapi.com/api"

    # Получение информации о случайном персонаже
    def get_random_character(self) -> Dict[str, any]:
        response = requests.get(f"{self.BASE_URL}/character")
        if response.status_code == 200:
            data = json.loads(response.text)
            print(data)
            total_characters = data['info']['count']  # Узнаем общее количество персонажей
            random_id = random.randint(1, total_characters)  # Генерируем случайный ID
            random_character_response = requests.get(f"{self.BASE_URL}/character/{random_id}")
            if random_character_response.status_code == 200:
                return json.loads(random_character_response.text)
            else:
                return {"error": "Failed to fetch random character"}
        else:
            return {"error": "Failed to fetch characters"}

    # Поиск персонажей по имени
    def search_characters(self, name: str) -> List[Dict[str, any]]:
        response = requests.get(f"{self.BASE_URL}/character/?name={name}")
        if response.status_code == 200:
            return json.loads(response.text)['results']
        else:
            return [{"error": "Персонаж не найден"}]

    # Получение списка всех локаций
    def get_all_locations(self) -> List[Dict[str, any]]:
        response = requests.get(f"{self.BASE_URL}/location")
        if response.status_code == 200:
            return json.loads(response.text)['results']
        else:
            return [{"error": "Failed to fetch locations"}]

    # Поиск эпизодов по названию
    def search_episodes(self, name: str) -> List[Dict[str, any]]:
        response = requests.get(f"{self.BASE_URL}/episode/?name={name}")
        if response.status_code == 200:
            return json.loads(response.text)['results']
        else:
            return [{"error": "Эпизод не найден"}]

    # Анализ статусов персонажей (жив/мертв/неизвестно)
    def analyze_character_status(self) -> Dict[str, int]:
        response = requests.get(f"{self.BASE_URL}/character")
        if response.status_code == 200:
            data = json.loads(response.text)
            characters = data['results']
            status_count = {"alive": 0, "dead": 0, "unknown": 0}
            for character in characters:
                status = character['status'].lower()
                if status in status_count:
                    status_count[status] += 1
                else:
                    status_count["unknown"] += 1
            return status_count
        else:
            return {"error": "Failed to analyze character status"}

import random

# Пример использования
def main():
    client = RickAndMortyClient()

    while True:
        print("\n--- Rick and Morty API ---")
        print("1. Получить случайного персонажа")
        print("2. Поиск персонажей по имени")
        print("3. Поиск эпизодов по названию")
        print("4. Выход")
        choice = input("Выберите опцию (1-4): ")

        if choice == '1':
            random_character = client.get_random_character()
            if "error" in random_character:
                print(f"Ошибка: {random_character['error']}")
            else:
                print(f"\nСлучайный персонаж: {random_character.get('name', 'Неизвестно')}")
                print(f"Пол: {random_character.get('gender', 'Неизвестно')}")
                print(f"Вид: {random_character.get('species', 'Неизвестно')}")
                print(f"Тип: {random_character.get('type', 'Неизвестно')}")
        elif choice == '2':
            name = input("\nВведите имя персонажа для поиска: ")
            characters = client.search_characters(name)
            if "error" in characters[0]:
                print(f"Ошибка: {characters[0]['error']}")
            else:
                print(f"\nНайдено персонажей по имени '{name}': {len(characters)}")
                for character in characters:
                    print(f"Имя: {character['name']}, Статус: {character['status']}, Локация: {character['location']['name']}, "
                          f"Пол: {character['gender']}, Вид: {character['species']}, Тип: {character.get('type', 'Неизвестно')}")
        elif choice == '3':
            episode_name = input("\nВведите название эпизода для поиска: ")
            episodes = client.search_episodes(episode_name)
            if "error" in episodes[0]:
                print(f"Ошибка: {episodes[0]['error']}")
            else:
                print(f"\nНайдено эпизодов с названием '{episode_name}': {len(episodes)}")
                for episode in episodes:
                    print(f"Название: {episode['name']}, Дата выхода: {episode['air_date']}, Эпизод: {episode['episode']}")
        elif choice == '4':
            print("Выход из программы. До свидания!")
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите опцию от 1 до 4.")

if __name__ == "__main__":
    main()
