import random
import os
from datetime import datetime

class Actions:
    def __init__(self, config):
        self.config = config
        self._init_log_file()
    
    def _init_log_file(self):
        """Инициализация файла логов"""
        if not os.path.exists(self.config.LOG_FILE):
            with open(self.config.LOG_FILE, 'w', encoding='utf-8') as f:
                f.write("=== AFK BRO BOT HISTORY LOG ===\n")
                f.write(f"Создан: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 50 + "\n\n")
    
    def _write_to_log(self, action_type, message):
        """Запись действия в лог-файл бота"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {action_type}: {message}\n"
        
        with open(self.config.LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_entry)
        
        return log_entry.strip()
    
    def get_random_action(self):
        """Возвращает действие (для совместимости)"""
        return self.dummy_action
    
    def dummy_action(self):
        """Заглушка - действия теперь в GUI"""
        return True, "Действие выполнено в GUI"
