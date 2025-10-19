import pyautogui
import random
import time
import os
import subprocess
from datetime import datetime

class Actions:
    def __init__(self, config):
        self.config = config
        pyautogui.FAILSAFE = True
        self.text_file_opened = False
        self._init_log_file()
        self._create_text_file()
        # Убрано автоматическое открытие файла - будет открываться только при первом действии
    
    def _init_log_file(self):
        """Инициализация файла логов"""
        if not os.path.exists(self.config.LOG_FILE):
            with open(self.config.LOG_FILE, 'w', encoding='utf-8') as f:
                f.write("=== AFK BOT HISTORY LOG ===\n")
                f.write(f"Создан: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 50 + "\n\n")
    
    def _create_text_file(self):
        """Создает текстовый файл если его нет"""
        if not os.path.exists(self.config.TEXT_FILE_PATH):
            with open(self.config.TEXT_FILE_PATH, 'w', encoding='utf-8') as f:
                f.write("=== AFK Activity File ===\n")
                f.write(f"Создан: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("Этот файл используется для имитации активности\n")
                f.write("=" * 50 + "\n\n")
        print(f"✅ Файл создан: {self.config.TEXT_FILE_PATH}")
    
    def _open_text_file(self):
        """Открывает текстовый файл в блокноте"""
        try:
            if not self.text_file_opened:
                print("📁 Открываю текстовый файл в блокноте...")
                
                # Открываем блокнот
                subprocess.Popen(['notepad.exe', self.config.TEXT_FILE_PATH])
                
                # Даем время на открытие
                time.sleep(3)
                
                self.text_file_opened = True
                print("✅ Блокнот открыт")
                return True
            return True
        except Exception as e:
            print(f"❌ Не удалось открыть файл: {e}")
            return False
    
    def _write_to_log(self, action_type, message):
        """Запись действия в лог-файл бота"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {action_type}: {message}\n"
        
        with open(self.config.LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_entry)
        
        return log_entry.strip()
    
    def text_file_action(self):
        """Работа с текстовым файлом - запись и стирание"""
        try:
            # Убедимся что файл открыт (теперь открывается только здесь)
            if not self.text_file_opened:
                success = self._open_text_file()
                if not success:
                    return False, "❌ Не удалось открыть текстовый файл"
                time.sleep(2)
            
            # Выбираем случайное сообщение
            message = random.choice(self.config.TEXT_MESSAGES)
            # Полный формат с датой и временем
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            full_message = f"{timestamp}  {message}"
            
            print(f"📝 Пишу в файл: '{message}'")
            
            # Переходим в конец файла
            pyautogui.hotkey('ctrl', 'end')
            time.sleep(0.5)
            
            # Новая строка если нужно
            pyautogui.press('enter')
            time.sleep(0.2)
            
            # Печатаем сообщение
            pyautogui.write(full_message, interval=0.05)
            time.sleep(1)
            
            # Иногда стираем часть текста (40% вероятности)
            if random.random() < 0.4:
                print("🔙 Стираю часть текста...")
                # Стираем несколько символов
                erase_count = random.randint(2, 8)
                for _ in range(erase_count):
                    pyautogui.press('backspace')
                    time.sleep(0.1)
                
                # Печатаем исправление
                corrections = [" [исправлено]", " [updated]", " [fixed]", " [revised]"]
                correction = random.choice(corrections)
                pyautogui.write(correction, interval=0.05)
            
            # Сохраняем файл
            pyautogui.hotkey('ctrl', 's')
            time.sleep(0.5)
            
            # Логируем действие
            self._write_to_log("TEXT_FILE", f"Записано: '{message}'")
            
            return True, f"Запись в файл: '{message}'"
                
        except Exception as e:
            error_msg = self._write_to_log("ERROR", f"File action failed: {e}")
            return False, f"❌ Ошибка: {e}"
    
    def get_random_action(self):
        """Всегда возвращает действие с текстовым файлом"""
        return self.text_file_action