import random
import redis
import threading
from datetime import datetime
from colorama import Fore, init

init()
colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX,
          Fore.LIGHTGREEN_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, Fore.LIGHTYELLOW_EX,
          Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW]

client_color = random.choice(colors)
separator_token = ": "

class ChatClass:
    def __init__(self, username, room_name):
        self.username = username
        self.room_name = room_name
        self.red = redis.Redis()
        self.sub = self.red.pubsub()
        self.is_chatting = True


    def handle_request(self) -> str:
            try:
                to_send = input()
                date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                to_send = f"{client_color}[{date_now}] {self.username}{separator_token}{to_send}{Fore.RESET}"
                return to_send
            except KeyboardInterrupt:
                self.stop_chat()
                return ""

    def handle_messages(self):
         for message in self.sub.listen():
            if message['type'] == 'message':
                print(f"{message['data'].decode()}")
                if not self.is_chatting:
                    break


    def start_pulling(self):
        self.sub.subscribe(self.room_name)
        threading.Thread(target=self.handle_messages).start()

        try:
            while self.is_chatting:
                message = self.handle_request()
                self.red.publish(self.room_name, message)
        except KeyboardInterrupt:
            self.stop_chat()

    def stop_chat(self):
        self.is_chatting = False


if __name__ == '__main__':
    username = input("Enter your username: ")
    room_name = input("Enter room name: ")
    chat_worker = ChatClass(username, room_name)
    chat_worker.start_pulling()
    
