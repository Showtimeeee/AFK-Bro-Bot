import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
from datetime import datetime

class AFKBotGUI:
    def __init__(self, bot):
        self.bot = bot
        self.root = tk.Tk()
        self.root.title("AFK Bot - Умный помощник активности")
        self.root.geometry("800x600")
        self.is_running = False
        
        self.setup_gui()
    
    def setup_gui(self):
        """Настраивает интерфейс"""
        # Заголовок
        title_label = ttk.Label(self.root, text="🤖 AFK Bot", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Описание
        desc_label = ttk.Label(self.root, 
                              text="Автоматически поддерживает активность системы\nимитируя работу с текстовым файлом",
                              font=("Arial", 10))
        desc_label.pack(pady=5)
        
        # Статус
        self.status_frame = ttk.LabelFrame(self.root, text="Статус", padding=10)
        self.status_frame.pack(fill="x", padx=10, pady=5)
        
        self.status_label = ttk.Label(self.status_frame, text="❌ Бот остановлен", font=("Arial", 10))
        self.status_label.pack(side="left")
        
        # Кнопки управления
        self.control_frame = ttk.Frame(self.root)
        self.control_frame.pack(fill="x", padx=10, pady=10)
        
        self.start_button = ttk.Button(self.control_frame, text="▶️ Запустить бота", 
                                      command=self.start_bot)
        self.start_button.pack(side="left", padx=5)
        
        self.stop_button = ttk.Button(self.control_frame, text="⏹️ Остановить бота", 
                                     command=self.stop_bot, state="disabled")
        self.stop_button.pack(side="left", padx=5)
        
        # Статистика
        stats_frame = ttk.LabelFrame(self.root, text="Статистика", padding=10)
        stats_frame.pack(fill="x", padx=10, pady=5)
        
        self.stats_text = tk.Text(stats_frame, height=4, font=("Arial", 9))
        self.stats_text.pack(fill="x")
        self.update_stats()
        
        # Лог действий
        log_frame = ttk.LabelFrame(self.root, text="Лог действий", padding=10)
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, font=("Arial", 9))
        self.log_text.pack(fill="both", expand=True)
        
        # Информация о файлах
        files_frame = ttk.LabelFrame(self.root, text="Файлы", padding=10)
        files_files = ttk.Frame(files_frame)
        files_files.pack(fill="x")
        
        ttk.Label(files_files, text="Текстовый файл:").pack(side="left")
        ttk.Label(files_files, text=self.bot.config.TEXT_FILE_PATH, 
                 foreground="blue").pack(side="left", padx=5)
        
        ttk.Label(files_files, text="Лог файл:").pack(side="left", padx=(20,0))
        ttk.Label(files_files, text=self.bot.config.LOG_FILE, 
                 foreground="blue").pack(side="left", padx=5)
        
        files_frame.pack(fill="x", padx=10, pady=5)
        
        # Протокол закрытия окна
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def log_message(self, message):
        """Добавляет сообщение в лог"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def update_stats(self):
        """Обновляет статистику"""
        stats = f"""Действий выполнено: {self.bot.action_count}
Интервал: {self.bot.config.INTERVAL} секунд
Режим: Работа с текстовым файлом
Файл активности: {self.bot.config.TEXT_FILE_PATH}"""
        
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, stats)
    
    def start_bot(self):
        """Запускает бота в отдельном потоке"""
        if not self.is_running:
            self.is_running = True
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            self.status_label.config(text="✅ Бот запущен")
            
            self.log_message("🚀 Запуск AFK бота...")
            self.log_message(f"📁 Файл: {self.bot.config.TEXT_FILE_PATH}")
            self.log_message(f"⏰ Интервал: {self.bot.config.INTERVAL} сек")
            
            # Запускаем бота в отдельном потоке
            self.bot_thread = threading.Thread(target=self.run_bot)
            self.bot_thread.daemon = True
            self.bot_thread.start()
    
    def stop_bot(self):
        """Останавливает бота"""
        if self.is_running:
            self.is_running = False
            self.bot.is_running = False
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            self.status_label.config(text="❌ Бот остановлен")
            
            self.log_message("🛑 Остановка бота...")
            self.update_stats()
    
    def run_bot(self):
        """Запускает основную логику бота"""
        self.bot.is_running = True
        self.bot.action_count = 0
        self.bot.start_time = datetime.now()
        
        # Логируем старт
        self.bot.actions._write_to_log("SYSTEM", "=== AFK BOT STARTED ===")
        
        try:
            while self.bot.is_running and self.is_running:
                self.bot._do_action()
                self.update_stats()
                
                # Ждем интервал, но проверяем флаг остановки
                for _ in range(self.bot.config.INTERVAL):
                    if not self.bot.is_running or not self.is_running:
                        break
                    self.root.after(1000)  # Ждем 1 секунду
                    
        except Exception as e:
            self.log_message(f"❌ Ошибка: {e}")
        
        # Завершаем работу
        self.bot.stop()
        self.log_message("👋 Работа бота завершена")
    
    def on_closing(self):
        """Обработчик закрытия окна"""
        if self.is_running:
            self.stop_bot()
        self.root.destroy()
    
    def run(self):
        """Запускает GUI"""
        self.root.mainloop()