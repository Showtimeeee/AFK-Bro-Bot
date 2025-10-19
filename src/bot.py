import time
import random
from datetime import datetime

class Bot:
    def __init__(self, actions, config):
        self.actions = actions
        self.config = config
        self.is_running = False
        self.action_count = 0
        self.start_time = None
    
    def start(self):
        self.is_running = True
        self.action_count = 0
        self.start_time = datetime.now()
        
        # Логируем старт
        self.actions._write_to_log("SYSTEM", "=== AFK BOT STARTED ===")
        
        print("🚀 AFK Бот запущен!")
        print("📋 Действие: Работа с текстовым файлом")
        print(f"📁 Файл: {self.config.TEXT_FILE_PATH}")
        print(f"📊 Логи: {self.config.LOG_FILE}")
        print(f"⏰ Интервал: {self.config.INTERVAL} секунд")
        print("🎯 Будет писать и стирать текст в блокноте")
        print("💾 Блокнот останется открытым после остановки")
        print("🛑 Остановка: Ctrl+C")
        print("-" * 50)
        
        try:
            while self.is_running:
                self._do_action()
                time.sleep(self.config.INTERVAL)
        except KeyboardInterrupt:
            self.stop()
    
    def _do_action(self):
        self.action_count += 1
        action_func = self.actions.get_random_action()
        
        success, message = action_func()
        
        if success:
            print(f"✅ Действие #{self.action_count}: {message}")
        else:
            print(f"❌ Действие #{self.action_count}: {message}")
    
    def stop(self):
        self.is_running = False
        
        if self.start_time is not None:
            end_time = datetime.now()
            duration = end_time - self.start_time
            
            # Логируем остановку
            self.actions._write_to_log("SYSTEM", 
                f"AFK BOT STOPPED. Duration: {duration}, Actions: {self.action_count}")
            
            print(f"\n📊 Статистика:")
            print(f"   Выполнено действий: {self.action_count}")
            print(f"   Продолжительность: {duration}")
            print(f"   Файл: {self.config.TEXT_FILE_PATH}")
            print(f"   Логи: {self.config.LOG_FILE}")
        else:
            print(f"\n📊 Выполнено действий: {self.action_count}")
        
        print("💾 Блокнот остался открытым - сохраните файл если нужно")
        print("👋 Бот остановлен")