import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import uuid

bot = telebot.TeleBot('5193117811:AAH0hWHVx0kH08sub52IFj2SAdJi1eugY-k')


# -----------------------------------------------------------------------

class TTTGame:

    def __init__(self, chat_id1, chat_id2, guid, player1, player2):
        self.guid = guid
        self.isGameOver = False
        self.isFirstPlayerStep = True
        self.status = [[None, None, None], [None, None, None], [None, None, None]]

        bot.send_message(chat_id1,
                         f"Второй игрок подключился к игре\nИгра начинается\nВы играете с @{player2}\nВаш символ: ❎\n")
        bot.send_message(chat_id2,
                         f"Второй игрок подключился к игре\nИгра начинается\nВы играете с @{player1}\nВаш символ: 🅾️\n")

        user_message1 = bot.send_message(chat_id1, "-")
        user_message2 = bot.send_message(chat_id2, "-")
        self.user_info = {
            'player1': {'chat_id': chat_id1, "team": 1, "message_id": user_message1.message_id},
            'player2': {'chat_id': chat_id2, "team": 0, "message_id": user_message2.message_id}
        }
        self.update()

    def step(self, btn_num, chat_id, call_id):
        if (self.isFirstPlayerStep and chat_id == self.user_info['player2']['chat_id']) \
                or (not self.isFirstPlayerStep and chat_id == self.user_info['player1']['chat_id']):
            bot.answer_callback_query(call_id, "Сейчас не ваш ход")
            return
        else:
            bot.answer_callback_query(call_id)

        btn_num = int(btn_num) - 1
        i = btn_num // 3
        j = btn_num % 3

        if self.isFirstPlayerStep and chat_id == self.user_info['player1']['chat_id']:
            self.status[i][j] = 1

        if self.isFirstPlayerStep is False and chat_id == self.user_info['player2']['chat_id']:
            self.status[i][j] = 0

        self.isFirstPlayerStep = not self.isFirstPlayerStep

        self.update()
        self.isWinner()


    def isWinner(self):

        if (self.status[1][0] == self.status[1][1] == self.status[1][2] or
                self.status[0][1] == self.status[1][1] == self.status[2][1] or
                self.status[0][0] == self.status[1][1] == self.status[2][2] or
                self.status[0][2] == self.status[1][1] == self.status[2][0]) and (self.status[1][1] is not None):

            winning_team = self.status[1][1]
            winning_case = True

        elif (self.status[0][0] == self.status[0][1] == self.status[0][2]
              or self.status[0][2] == self.status[1][2] == self.status[2][2]) and (self.status[0][2] is not None):
            winning_team = self.status[0][2]
            winning_case = True

        elif (self.status[2][0] == self.status[2][1] == self.status[2][2]
              or self.status[0][0] == self.status[1][0] == self.status[2][0]) and (self.status[2][0] is not None):
            winning_team = self.status[2][0]
            winning_case = True

        else:
            winning_case = False
            winning_team = None

        if winning_team == 1 and winning_case:
            bot.send_message(self.user_info['player1']['chat_id'], "Поздравляю, вы выиграли!")
            bot.send_message(self.user_info['player2']['chat_id'], "Очень жаль, но вы проиграли.")
            self.isGameOver = True

        elif winning_team == 0 and winning_case:
            bot.send_message(self.user_info['player2']['chat_id'], "Поздравляю, вы выиграли!")
            bot.send_message(self.user_info['player1']['chat_id'], "Очень жаль, но вы проиграли.")
            self.isGameOver = True

        elif not (None in sum(self.status, [])):
            bot.send_message(self.user_info['player2']['chat_id'], "Ничья! Игра окончена.")
            bot.send_message(self.user_info['player1']['chat_id'], "Ничья! Игра окончена.")
            self.isGameOver = True

    def update(self):
        def symbol(i, j):
            if self.status[i][j] is None:
                char = "⏺"
            elif self.status[i][j] == 1:
                char = "❎"
            else:
                char = "🅾"
            return char

        markup = InlineKeyboardMarkup()
        markup.row_width = 3
        markup.add(InlineKeyboardButton(symbol(0, 0), callback_data=f"TTT:{self.guid}:1"),
                   InlineKeyboardButton(symbol(0, 1), callback_data=f"TTT:{self.guid}:2"),
                   InlineKeyboardButton(symbol(0, 2), callback_data=f"TTT:{self.guid}:3"),
                   InlineKeyboardButton(symbol(1, 0), callback_data=f"TTT:{self.guid}:4"),
                   InlineKeyboardButton(symbol(1, 1), callback_data=f"TTT:{self.guid}:5"),
                   InlineKeyboardButton(symbol(1, 2), callback_data=f"TTT:{self.guid}:6"),
                   InlineKeyboardButton(symbol(2, 0), callback_data=f"TTT:{self.guid}:7"),
                   InlineKeyboardButton(symbol(2, 1), callback_data=f"TTT:{self.guid}:8"),
                   InlineKeyboardButton(symbol(2, 2), callback_data=f"TTT:{self.guid}:9"))

        bot.edit_message_text("-------------------------------------------------------\nСейчас ваш ход" if self.isFirstPlayerStep
                              else "-------------------------------------------------------\nСейчас ход другого игрока",
                              chat_id=self.user_info['player1']['chat_id'],
                              message_id=self.user_info['player1']['message_id'], reply_markup=markup)
        bot.edit_message_text("-------------------------------------------------------\nСейчас ваш ход" if not self.isFirstPlayerStep
                              else "-------------------------------------------------------\nСейчас ход другого игрока",
                              chat_id=self.user_info['player2']['chat_id'],
                              message_id=self.user_info['player2']['message_id'], reply_markup=markup)




# -----------------------------------------------------------------------

class TTTLobby:
    waiting_player = None
    waiting_player_name = None
    activeTTTGames = {}

    def step(self, btn_id, chat_id, call_id):
        game_guid = btn_id.split(':')[1]
        print(game_guid)
        print(self.activeTTTGames)
        try:
            self.activeTTTGames[game_guid].step(int(btn_id.split(':')[2]), chat_id, call_id)
            if self.activeTTTGames[game_guid].isGameOver:
                self.activeTTTGames.pop(game_guid)
        except KeyError:
            bot.answer_callback_query(call_id, "Эта игра уже окончена")

    def play(self, chat_id, player):
        if self.waiting_player is None:
            self.waiting_player = chat_id
            self.waiting_player_name = player
            bot.send_message(chat_id, 'Ищем второго игрока...')
        elif self.waiting_player == chat_id:
            bot.send_message(chat_id, 'Вы уже ищите игру')
        else:
            guid = str(uuid.uuid4())
            self.activeTTTGames[guid] = TTTGame(self.waiting_player, chat_id, guid, self.waiting_player_name, player)
            self.waiting_player = None
            self.waiting_player_name = None
