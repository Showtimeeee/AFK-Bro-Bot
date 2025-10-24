import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.actions import Actions

class TestActions(unittest.TestCase):
    
    def set_up(self):
        """Настройка перед каждым тестом"""
        from config import Config
        self.config = Config()
        self.config.LOG_FILE = "logs/test.log"
        
        self.actions = Actions(self.config)
    
    def test_actions_creation(self):
        """Тест что объект создается правильно"""
        self.set_up()
        self.assertIsNotNone(self.actions)
        self.assertEqual(self.actions.config, self.config)
    
    def test_write_to_log(self):
        """Тест записи в лог"""
        self.set_up()
        
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
        self.set_up()
        action = self.actions.get_random_action()
        
        # Должен возвращать dummy_action
        self.assertEqual(action.__name__, 'dummy_action')
    
    def test_dummy_action(self):
        """Тест заглушки действия"""
        self.set_up()
        success, message = self.actions.dummy_action()
        
        self.assertTrue(success)
        self.assertEqual(message, "Действие выполнено в GUI")
    
    def test_log_file_creation(self):
        """Тест создания лог-файла при инициализации"""
        self.set_up()
        self.assertTrue(os.path.exists(self.config.LOG_FILE))
    
    def tearDown(self):
        """Очистка после тестов"""
        # Удаляем тестовые файлы если они существуют
        if os.path.exists("logs/test.log"):
            os.remove("logs/test.log")
        
        # Удаляем папку logs если пустая
        if os.path.exists("logs") and not os.listdir("logs"):
            os.rmdir("logs")

if __name__ == '__main__':
    unittest.main()
