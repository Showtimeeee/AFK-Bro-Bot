import unittest
import sys
import os
from datetime import datetime
from unittest.mock import patch  # Правильный импорт mock

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.bot import Bot

class TestBot(unittest.TestCase):
    
    def set_up(self):
        """Настройка перед каждым тестом"""
        from config import Config
        
        self.config = Config()
        self.config.INTERVAL = 1
        
        # Создаем mock для actions
        class MockActions:
            def __init__(self):
                pass
            
            def _write_to_log(self, action_type, message):
                pass
        
        self.mock_actions = MockActions()
        self.bot = Bot(self.mock_actions, self.config)
    
    def test_bot_creation(self):
        """Тест создания бота"""
        self.set_up()
        self.assertIsNotNone(self.bot)
        self.assertEqual(self.bot.actions, self.mock_actions)
        self.assertEqual(self.bot.config, self.config)
        self.assertFalse(self.bot.is_running)
        self.assertEqual(self.bot.action_count, 0)
        self.assertIsNone(self.bot.start_time)
    
    def test_stop_method_without_start(self):
        """Тест остановки бота без предварительного запуска"""
        self.set_up()
        
        # Останавливаем бота который не был запущен
        self.bot.stop()
        
        # Проверяем что не произошло ошибок
        self.assertFalse(self.bot.is_running)
    
    def test_stop_method_with_start_time(self):
        """Тест остановки бота с установленным временем старта"""
        self.set_up()
        self.bot.start_time = datetime.now()
        self.bot.action_count = 5
        
        # Используем правильный импорт patch
        with patch.object(self.bot.actions, '_write_to_log') as mock_log:
            self.bot.stop()
        
        self.assertFalse(self.bot.is_running)
        # Проверяем что был вызван лог
        mock_log.assert_called_once()
    
    def test_config_values(self):
        """Тест значений конфигурации"""
        self.set_up()
        self.assertEqual(self.config.INTERVAL, 1)
        self.assertIsInstance(self.config.TEXT_MESSAGES, list)
        self.assertGreater(len(self.config.TEXT_MESSAGES), 0)
        self.assertTrue(hasattr(self.config, 'LOG_FILE'))

if __name__ == '__main__':
    unittest.main()
