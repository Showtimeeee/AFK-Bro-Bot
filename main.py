from config import Config
from src.actions import Actions
from src.bot import Bot
from src.gui import AFKBotGUI

def main():
    config = Config()
    actions = Actions(config)
    bot = Bot(actions, config)
    
    # Запускаем GUI
    gui = AFKBotGUI(bot)
    gui.run()

if __name__ == "__main__":
    main()
