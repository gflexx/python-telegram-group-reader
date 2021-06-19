from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.sync import TelegramClient
import json

with open('config.json') as config_file:
	config = json.load(config_file)

api_id = config['api_id']
api_hash = config['api_hash']
phone_num = config['phone_num']

def main():
    print('Starting app... \nConnecting...')

    # connect client
    client = TelegramClient(phone_num, api_id, api_hash)
    client.connect()

    # if not authenticated send auth Code
    # enter auth code to sign in
    if not client.is_user_authorized():
        client.send_code_request(phone_num)
        client.sign_in(phone_num, input('Enter Auth Code: '))

    if client.is_user_authorized():
        me = client.get_me()
        print('Connected as {}'.format(me.username))

    # get chats
    chats = []
    print('Getting chats...')
    get_chats = GetDialogsRequest(
        offset_date = None,
        offset_id = 0,
        offset_peer = InputPeerEmpty(),
        limit = 108,
        hash = 0,
    )
    response = client(get_chats)
    chats.extend(response.chats)
    print('Chats obtained ({})'.format(len(chats)))

    # get groups
    groups = []
    print('Getting groups...')
    for c in chats:
        try:
            if c.megagroup == True:
                groups.append(c)
        except:
            continue
    if not groups:
        print('No groups found!')
        return
    x = 0
    for g in groups:
        print(str(x) + ' -- ' + g.title)
        x += 1

    # listen for input continuosly
    while True:
        try:
            print('Choose group or press X to exit...')
            user_input = input('Enter number: ')

            # change input to int if not string
            try:
                u_input = int(user_input)
            except ValueError:
                u_input = user_input

            # if input is str check if x to exit
            if isinstance(u_input, str):
                if u_input.upper() == 'X':
                    print('Exiting, bye...')
                    exit()
                else:
                    print('Please enter a number!\n')

            # if input is int check if within group index
            elif isinstance(u_input, int):
                i = 0
                valid = []
                for i in range(x):
                    valid.append(i)
                    i += 1
                if u_input in valid:
                    target = groups[u_input]
                    print('Getting group ( {} )\n'.format(target.title))
                else:
                    print('Please enter a valid number within the list!\n')

        except EOFError:
            print('Something went wrong... :(')
            break


if __name__ == '__main__':
    main()
