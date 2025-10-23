import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
from datetime import datetime, timedelta
import random
import time

class DarkTheme:
    """Настройки темной темы"""
    BG_COLOR = "#2b2b2b"
    FG_COLOR = "#ffffff"
    ACCENT_COLOR = "#bb86fc"
    SECONDARY_BG = "#3c3c3c"
    TEXT_BG = "#1e1e1e"
    TEXT_FG = "#d4d4d4"
    SUCCESS_COLOR = "#4caf50"
    ERROR_COLOR = "#f44336"
    WARNING_COLOR = "#ff9800"
    BUTTON_BG = "#404040"
    BUTTON_FG = "#ffffff"

class AFKBroBotGUI:
    def __init__(self, bot):
        self.bot = bot
        self.root = tk.Tk()
        self.root.title("AFK Bro Bot - Умный помощник активности")
        self.root.geometry("900x700")
        self.root.configure(bg=DarkTheme.BG_COLOR)
        
        # Переменные состояния
        self.is_running = False
        self.bot_thread = None
        self.start_time = None
        self.timer_running = False
        
        # Настраиваем стиль для темной темы
        self.setup_dark_theme()
        self.setup_gui()
    
    def setup_dark_theme(self):
        """Настраивает темную тему для виджетов"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Базовые настройки
        style.configure(".", 
                       background=DarkTheme.BG_COLOR,
                       foreground=DarkTheme.FG_COLOR)
        
        # Стили для конкретных виджетов
        style.configure("TFrame", background=DarkTheme.BG_COLOR)
        style.configure("TLabel", 
                       background=DarkTheme.BG_COLOR, 
                       foreground=DarkTheme.FG_COLOR)
        
        style.configure("TButton", 
                       background=DarkTheme.BUTTON_BG,
                       foreground=DarkTheme.BUTTON_FG,
                       focuscolor=DarkTheme.ACCENT_COLOR)
        
        style.configure("TLabelframe", 
                       background=DarkTheme.BG_COLOR,
                       foreground=DarkTheme.ACCENT_COLOR)
        
        style.configure("TLabelframe.Label", 
                       background=DarkTheme.BG_COLOR,
                       foreground=DarkTheme.ACCENT_COLOR)
        
        # Стиль для кнопок при наведении
        style.map("TButton",
                 background=[('active', DarkTheme.ACCENT_COLOR),
                           ('pressed', DarkTheme.ACCENT_COLOR)],
                 foreground=[('active', DarkTheme.BUTTON_FG),
                           ('pressed', DarkTheme.BUTTON_FG)])
    
    def setup_gui(self):
        """Настраивает интерфейс"""
        # Заголовок
        title_label = ttk.Label(self.root, 
                               text="🤖 AFK Bro Bot", 
                               font=("Arial", 18, "bold"),
                               foreground=DarkTheme.ACCENT_COLOR)
        title_label.pack(pady=15)
        
        # Описание
        desc_label = ttk.Label(self.root, 
                              text="Автоматически поддерживает активность системы\nимитируя работу с текстовым файлом",
                              font=("Arial", 10),
                              foreground=DarkTheme.FG_COLOR)
        desc_label.pack(pady=5)
        
        # Статус и таймер
        self.status_frame = ttk.LabelFrame(self.root, text="📊 Статус", padding=10)
        self.status_frame.pack(fill="x", padx=15, pady=10)
        
        status_content = ttk.Frame(self.status_frame)
        status_content.pack(fill="x")
        
        self.status_label = ttk.Label(status_content, 
                                     text="❌ Бот остановлен", 
                                     font=("Arial", 11, "bold"),
                                     foreground=DarkTheme.ERROR_COLOR)
        self.status_label.pack(side="left")
        
        self.timer_label = ttk.Label(status_content, 
                                    text="⏱️ Время работы: 00:00:00", 
                                    font=("Arial", 10),
                                    foreground=DarkTheme.ACCENT_COLOR)
        self.timer_label.pack(side="right")
        
        # Кнопки управления
        self.control_frame = ttk.Frame(self.root)
        self.control_frame.pack(fill="x", padx=15, pady=10)
        
        self.start_button = ttk.Button(self.control_frame, 
                                      text="▶️ Запустить бота", 
                                      command=self.start_bot)
        self.start_button.pack(side="left", padx=5)
        
        self.stop_button = ttk.Button(self.control_frame, 
                                     text="⏹️ Остановить бота", 
                                     command=self.stop_bot, 
                                     state="disabled")
        self.stop_button.pack(side="left", padx=5)
        
        # Статистика
        stats_frame = ttk.LabelFrame(self.root, text="📈 Статистика", padding=10)
        stats_frame.pack(fill="x", padx=15, pady=10)
        
        self.stats_text = tk.Text(stats_frame, 
                                 height=4, 
                                 font=("Arial", 9),
                                 bg=DarkTheme.TEXT_BG,
                                 fg=DarkTheme.TEXT_FG,
                                 insertbackground=DarkTheme.FG_COLOR,
                                 relief="flat",
                                 borderwidth=1)
        self.stats_text.pack(fill="x")
        self.stats_text.config(state="disabled")
        self.update_stats()
        
        # Текстовый редактор
        editor_frame = ttk.LabelFrame(self.root, text="📝 Текстовый редактор", padding=10)
        editor_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Панель инструментов редактора
        toolbar = ttk.Frame(editor_frame)
        toolbar.pack(fill="x", pady=5)
        
        ttk.Button(toolbar, 
                  text="📝 Добавить текст", 
                  command=self.add_sample_text).pack(side="left", padx=5)
        ttk.Button(toolbar, 
                  text="🧹 Очистить", 
                  command=self.clear_editor).pack(side="left", padx=5)
        ttk.Button(toolbar, 
                  text="💾 Сохранить в файл", 
                  command=self.save_to_file).pack(side="left", padx=5)
        
        # Поле текстового редактора
        self.text_editor = scrolledtext.ScrolledText(editor_frame, 
                                                    height=15, 
                                                    font=("Consolas", 10),
                                                    bg=DarkTheme.TEXT_BG,
                                                    fg=DarkTheme.TEXT_FG,
                                                    insertbackground=DarkTheme.FG_COLOR,
                                                    selectbackground=DarkTheme.ACCENT_COLOR,
                                                    relief="flat",
                                                    wrap="word",
                                                    borderwidth=1)
        self.text_editor.pack(fill="both", expand=True)
        
        # Добавляем начальный текст
        self.add_sample_text()
        
        # Лог действий
        log_frame = ttk.LabelFrame(self.root, text="📋 Лог действий", padding=10)
        log_frame.pack(fill="x", padx=15, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, 
                                                 height=8, 
                                                 font=("Arial", 9),
                                                 bg=DarkTheme.TEXT_BG,
                                                 fg=DarkTheme.TEXT_FG,
                                                 insertbackground=DarkTheme.FG_COLOR,
                                                 selectbackground=DarkTheme.ACCENT_COLOR,
                                                 relief="flat",
                                                 borderwidth=1)
        self.log_text.pack(fill="x")
        self.log_text.config(state="disabled")
        
        # Протокол закрытия окна
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def format_time_delta(self, delta):
        """Форматирует timedelta в читаемый формат"""
        total_seconds = int(delta.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def update_timer(self):
        """Обновляет таймер работы"""
        if self.is_running and self.start_time:
            current_time = datetime.now()
            elapsed = current_time - self.start_time
            time_str = self.format_time_delta(elapsed)
            self.timer_label.config(text=f"⏱️ Время работы: {time_str}")
        
        # Планируем следующее обновление через 1 секунду
        if self.timer_running:
            self.root.after(1000, self.update_timer)
    
    def start_timer(self):
        """Запускает таймер"""
        self.timer_running = True
        self.start_time = datetime.now()
        self.update_timer()
    
    def stop_timer(self):
        """Останавливает таймер"""
        self.timer_running = False
        if self.start_time:
            current_time = datetime.now()
            elapsed = current_time - self.start_time
            time_str = self.format_time_delta(elapsed)
            self.timer_label.config(text=f"⏱️ Общее время: {time_str}")
    
    def add_sample_text(self):
        """Добавляет образец текста в редактор"""
        sample_text = """=== AFK Bro Bot Activity File ===
Создан: {datetime}
Этот файл используется для имитации активности
==================================================

Здесь будет автоматически добавляться текст...
""".format(datetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        self.text_editor.config(state="normal")
        self.text_editor.delete(1.0, tk.END)
        self.text_editor.insert(1.0, sample_text)
        self.text_editor.see(tk.END)
        self.text_editor.config(state="normal")
    
    def clear_editor(self):
        """Очищает текстовый редактор"""
        self.text_editor.config(state="normal")
        self.text_editor.delete(1.0, tk.END)
        self.text_editor.config(state="normal")
    
    def save_to_file(self):
        """Сохраняет содержимое редактора в файл"""
        try:
            self.text_editor.config(state="normal")
            content = self.text_editor.get(1.0, tk.END)
            self.text_editor.config(state="normal")
            
            filename = f"afk_bro_bot_activity_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            self.log_message("💾 Файл сохранен", DarkTheme.SUCCESS_COLOR)
            self.log_message(f"📁 Имя файла: {filename}", DarkTheme.FG_COLOR)
        except Exception as e:
            self.log_message(f"❌ Ошибка сохранения: {e}", DarkTheme.ERROR_COLOR)
    
    def simulate_typing(self):
        """Имитирует набор текста в редакторе"""
        try:
            # Выбираем случайное сообщение
            message = random.choice(self.bot.config.TEXT_MESSAGES)
            
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            full_message = f"{timestamp}  {message}"
            
            # Добавляем текст в редактор
            self.text_editor.config(state="normal")
            self.text_editor.insert(tk.END, f"\n{full_message}")
            self.text_editor.see(tk.END)
            self.text_editor.config(state="normal")
            
            # Иногда имитируем исправления (30% вероятности)
            if random.random() < 0.3:
                time.sleep(0.5)  # Пауза для реалистичности
                self.text_editor.config(state="normal")
                # Добавляем пометку об исправлении
                self.text_editor.insert(tk.END, " [исправлено]")
                self.text_editor.see(tk.END)
                self.text_editor.config(state="normal")
            
            # Логируем действие
            self.bot.actions._write_to_log("TEXT_EDITOR", f"Записано: '{message}'")
            
            return True, f"Запись в редактор: '{message}'"
            
        except Exception as e:
            error_msg = f"❌ Ошибка имитации: {e}"
            self.bot.actions._write_to_log("ERROR", f"GUI action failed: {e}")
            return False, error_msg
    
    def log_message(self, message, color=None):
        """Добавляет сообщение в лог"""
        if color is None:
            color = DarkTheme.FG_COLOR
            
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Сохраняем текущее состояние
        self.log_text.config(state="normal")
        
        # Вставляем сообщение с цветом
        self.log_text.insert(tk.END, f"[{timestamp}] ", DarkTheme.ACCENT_COLOR)
        self.log_text.insert(tk.END, f"{message}\n", color)
        
        # Делаем лог только для чтения
        self.log_text.config(state="disabled")
        self.log_text.see(tk.END)
        
        # Принудительно обновляем интерфейс
        self.root.update()
    
    def update_stats(self):
        """Обновляет статистику"""
        if self.start_time and self.is_running:
            current_time = datetime.now()
            elapsed = current_time - self.start_time
            time_str = self.format_time_delta(elapsed)
            time_info = f"Время работы: {time_str}\n"
        else:
            time_info = "Время работы: 00:00:00\n"
        
        stats = f"""{time_info}Действий выполнено: {self.bot.action_count}
Интервал: {self.bot.config.INTERVAL} секунд
Режим: Работа с текстовым редактором"""
        
        self.stats_text.config(state="normal")
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, stats)
        self.stats_text.config(state="disabled")
        
        # Принудительно обновляем интерфейс
        self.root.update()
    
    def start_bot(self):
        """Запускает бота в отдельном потоке"""
        if not self.is_running:
            self.is_running = True
            self.bot.is_running = True
            
            # Обновляем интерфейс
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            self.status_label.config(text="✅ Бот запущен", foreground=DarkTheme.SUCCESS_COLOR)
            
            self.log_message("🚀 Запуск AFK Bro Bot...", DarkTheme.ACCENT_COLOR)
            self.log_message("📝 Режим: Встроенный текстовый редактор", DarkTheme.FG_COLOR)
            self.log_message(f"⏰ Интервал: {self.bot.config.INTERVAL} сек", DarkTheme.FG_COLOR)
            
            # Сбрасываем счетчик и запускаем таймер
            self.bot.action_count = 0
            self.bot.start_time = datetime.now()
            self.start_timer()
            
            # Логируем старт
            self.bot.actions._write_to_log("SYSTEM", "=== AFK BRO BOT STARTED ===")
            
            # Запускаем бота в отдельном потоке
            self.bot_thread = threading.Thread(target=self.run_bot, daemon=True)
            self.bot_thread.start()
            
            self.log_message("✅ AFK Bro Bot успешно запущен", DarkTheme.SUCCESS_COLOR)
            self.update_stats()
    
    def stop_bot(self):
        """Останавливает бота"""
        if self.is_running:
            self.is_running = False
            self.bot.is_running = False
            
            # Останавливаем таймер
            self.stop_timer()
            
            # Обновляем интерфейс
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            self.status_label.config(text="❌ Бот остановлен", foreground=DarkTheme.ERROR_COLOR)
            
            self.log_message("🛑 Остановка AFK Bro Bot...", DarkTheme.WARNING_COLOR)
            
            # Логируем остановку
            if self.bot.start_time is not None:
                self.bot.stop()
            
            self.update_stats()
            self.log_message("👋 Работа AFK Bro Bot завершена", DarkTheme.ACCENT_COLOR)
    
    def run_bot(self):
        """Запускает основную логику бота в отдельном потоке"""
        self.log_message("🔄 AFK Bro Bot начал работу...", DarkTheme.SUCCESS_COLOR)
        
        try:
            while self.is_running and self.bot.is_running:
                # Выполняем действие
                success, message = self.simulate_typing()
                
                if success:
                    self.bot.action_count += 1
                    self.log_message(f"✅ {message}", DarkTheme.SUCCESS_COLOR)
                    self.update_stats()
                else:
                    self.log_message(message, DarkTheme.ERROR_COLOR)
                
                # Ждем указанный интервал
                for i in range(self.bot.config.INTERVAL):
                    if not self.is_running or not self.bot.is_running:
                        break
                    time.sleep(1)
                    
        except Exception as e:
            self.log_message(f"❌ Критическая ошибка: {e}", DarkTheme.ERROR_COLOR)
            self.bot.actions._write_to_log("ERROR", f"AFK Bro Bot crashed: {e}")
        
        # Автоматически останавливаем если поток завершился
        if self.is_running:
            self.stop_bot()
    
    def on_closing(self):
        """Обработчик закрытия окна"""
        if self.is_running:
            self.stop_bot()
        self.root.destroy()
    
    def run(self):
        """Запускает GUI"""
        self.root.mainloop()
