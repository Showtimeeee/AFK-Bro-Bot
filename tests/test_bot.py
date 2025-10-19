import datetime

def test_stop_method(self):
    """Тест остановки бота"""
    self.bot.is_running = True
    self.bot.action_count = 5
    self.bot.start_time = datetime.now()  # ← ДОБАВЬ ЭТУ СТРОКУ
    
    self.bot.stop()
    
    self.assertFalse(self.bot.is_running)