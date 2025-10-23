import time
from datetime import datetime

class Bot:
    def __init__(self, actions, config):
        self.actions = actions
        self.config = config
        self.is_running = False
        self.action_count = 0
        self.start_time = None
    
    def stop(self):
        """Останавливает бота"""
        self.is_running = False
        
        if self.start_time is not None:
            end_time = datetime.now()
            duration = end_time - self.start_time
            
            # Логируем остановку
            self.actions._write_to_log("SYSTEM", 
                f"AFK BRO BOT STOPPED. Duration: {duration}, Actions: {self.action_count}")
