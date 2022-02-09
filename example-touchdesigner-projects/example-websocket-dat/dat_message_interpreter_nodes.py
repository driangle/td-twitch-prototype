import random

def clamp(value,min_val=-1, max_val=1):
    return min(max(value, min_val), max_val)
        

op_table_user_state = op('table_user_state')
users = {}
DEBUG = True
# TODO parameterize ADMIN_USER
# TODO parameterize MAX_USER_COUNT
ADMIN_USER = 'selfloop'
MAX_USER_COUNT = 1000

def log_debug(message):
    global DEBUG
    if DEBUG:
        print('[dat_message_interpreter] ' + message)

class MessageInterpreter:

    def __init__(self):
        self._actions = []
        self._color_actions = []

    def add_action(self, condition, action):
        self._actions.append({'condition': condition, 'action': action})

    def add_color_action(self, action):
        return self._color_actions.append(action)

    def interpret(self, username, color, message):
        log_debug(f'Interpreting message [{message}] with color [{color}] for user [{username}]')
        try:
            for action in self._actions:
                if action['condition'](username, message):
                    action['action'](self, username, message)
                    break # one action per message
            for action in self._color_actions:
                action(username, color)
        except Exception as e:
            print(f'[dat_message_interpreter] Unexpected error while interpreting message. {str(type(e))}:{str(e)}')
            import traceback
            traceback.print_exception(type(e), e, e.__traceback__)

class UserState:

    def __init__(self, index, username):
        self._state = {
            'index': index,
            'username': username,
            'color': [1, 1, 1], # default color
            'initial_position': {
                'x': random.uniform(-1, 1),
                'y': random.uniform(-1, 1),
            },
            'velocity': {
                'x': random.uniform(-1, 1),
                'y': random.uniform(-1, 1),
            }
        }
    def index(self):
        return self._state['index']
    def to_row(self):
        return [
            self._state['username']
        ] + self._state['color'] + [
            self._state['initial_position']['x'],
            self._state['initial_position']['y'],
            self._state['velocity']['x'],
            self._state['velocity']['y']
        ]
    
    def set_color(self, color):
        self._state['color'] = color

    def get_color(self):
        return self._state.get('color')

    def stop(self):
        self._state = {
            **self._state,
            'velocity': {
                'x': 0,
                'y': 0
            }
        }
    def change_direction(self, direction, amount):
        try:
            getattr(self, direction)(amount)
        except AttributeError as e:
            print(f'[dat_message_interpreter] Unknown direction [{direction}]')

    def left(self, amount):
        self._state = {
            **self._state,
            'velocity': {
                **self._state['velocity'],
                'x': clamp(-(amount / 100))
            }
        }
    def right(self, amount):
        self._state = {
            **self._state,
            'velocity': {
                **self._state['velocity'],
                'x': clamp(amount / 100)
            }
        }
    def up(self, amount):
        self._state = {
            **self._state,
            'velocity': {
                **self._state['velocity'],
                'y': clamp(amount / 100)
            }
        }
    def down(self, amount):
        self._state = {
            **self._state,
            'velocity': {
                **self._state['velocity'],
                'y': clamp(-(amount / 100))
            }
        }

def update_table_op(user):
    global op_table_user_state
    if user.index() == op_table_user_state.numRows:
        op_table_user_state.appendRow(user.to_row())
    else:
        op_table_user_state.replaceRow(user.index(), user.to_row())

def handle_reset(self, username, message):
    global users
    global op_table_user_state
    print('[dat_message_interpreter] Resetting...')
    users = {}
    op_table_user_state.clear()

def handle_sim(self, username, message):
    print('[dat_message_interpreter] Simulating large group..')
    for index in range(0, 50):
        self.interpret(username + '-' + str(index), '#ffffff', 'join')

def handle_join(self, username, message, update_table=True):
    global users
    global op_table_user_state
    if username not in users:
        user = UserState(op_table_user_state.numRows, username)
        users[username] = user
        update_table_op(user)

def handle_stop(self, username, message):
    global users
    user = users[username]
    user.stop()
    update_table_op(user)

def handle_change_direction(self, username, message):
    global users
    global op_table_user_state
    try:
        parts = message.split(' ')
        direction = parts[0].lower()
        amount = float(parts[1])
        if username not in users:
            # join automatically when a direction command is sent
            users[username] = UserState(op_table_user_state.numRows, username)
        user = users[username]
        user.change_direction(direction, amount)
        update_table_op(user)
    except (IndexError, ValueError):
        pass
    
def handle_set_color(username, color):
    global users
    global op_table_user_state
    if color and username in users:
        user = users[username]
        current_color = user.get_color()
        new_color = parse_color(color)
        if current_color != new_color:
            user.set_color(parse_color(color))
            update_table_op(user)

interpreter = MessageInterpreter()
interpreter.add_action(
    condition=lambda username,message: username ==  me.parent().par.Adminuser and message == "reset",
    action=handle_reset
)
interpreter.add_action(
    condition=lambda username,message: username == me.parent().par.Adminuser and message == "sim",
    action=handle_sim
)
interpreter.add_action(
    condition=lambda _,message: message == "join",
    action=handle_join
)
interpreter.add_action(
    condition=lambda _,message: message == "stop",
    action=handle_stop
)
interpreter.add_action(
    condition=lambda _,message: len([
        direction for direction in [
            "left",
            "right",
            "up",
            "down",
        ] if message.startswith(direction)
    ]) > 0,
    action=handle_change_direction
)
interpreter.add_color_action(handle_set_color)

def parse_color(color_hex):
    hex = color_hex.lstrip('#')
    return [int(hex[i:i+2], 16) / 255.0 for i in (0, 2, 4)]

def onTableChange(dat):
    if dat.numRows == 0:
        return
    last_row = dat.rows()[dat.numRows - 1]
    username = last_row[0].val
    color = last_row[1].val
    message = last_row[2].val
    interpreter.interpret(username, color, message)
    return