import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.actions import Actions

class TestActions(unittest.TestCase):
    
    def set_up(self, open_file=False):
        """Настройка перед каждым тестом"""
        from config import Config
        self.config = Config()
        self.config.TEXT_FILE_PATH = "test_activity.txt"
        self.config.LOG_FILE = "logs/test.log"
        
        # Создаем actions без автоматического открытия файла
        self.actions = Actions(self.config)
        if not open_file:
            # Отменяем автоматическое открытие для тестов
            self.actions.text_file_opened = False
    
    def test_actions_creation(self):
        """Тест что объект создается правильно"""
        self.set_up(open_file=False)
        self.assertIsNotNone(self.actions)
        self.assertEqual(self.actions.config, self.config)
        self.assertFalse(self.actions.text_file_opened)  # Теперь должно быть False
    
    def test_create_text_file(self):
        """Тест создания файла"""
        self.set_up(open_file=False)
        
        # Проверяем что файл создается
        self.actions._create_text_file()
        self.assertTrue(os.path.exists(self.config.TEXT_FILE_PATH))
        
        # Проверяем содержимое файла
        with open(self.config.TEXT_FILE_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("AFK Activity File", content)
    
    def test_write_to_log(self):
        """Тест записи в лог"""
        self.set_up(open_file=False)
        
        # Записываем тестовое сообщение
        self.actions._write_to_log("TEST", "тестовое сообщение")
        
        # Проверяем что файл существует
        self.assertTrue(os.path.exists(self.config.LOG_FILE))
        
        # Проверяем что сообщение записалось
        with open(self.config.LOG_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("тестовое сообщение", content)
    
    def test_get_random_action(self):
        """Тест выбора действия"""
        self.set_up(open_file=False)
        action = self.actions.get_random_action()
        
        # Должен всегда возвращать text_file_action
        self.assertEqual(action, self.actions.text_file_action)
    
    def test_text_messages_exist(self):
        """Тест что есть сообщения для записи"""
        self.set_up(open_file=False)
        self.assertGreater(len(self.config.TEXT_MESSAGES), 0)
        self.assertIsInstance(self.config.TEXT_MESSAGES, list)
    
    def clean_up(self):
        """Очистка после тестов"""
        # Удаляем тестовые файлы если они существуют
        if os.path.exists(self.config.TEXT_FILE_PATH):
            os.remove(self.config.TEXT_FILE_PATH)
        if os.path.exists(self.config.LOG_FILE):
            os.remove(self.config.LOG_FILE)
        
        # Удаляем папку logs если пустая
        if os.path.exists("logs") and not os.listdir("logs"):
            os.rmdir("logs")

if __name__ == '__main__':
    unittest.main()