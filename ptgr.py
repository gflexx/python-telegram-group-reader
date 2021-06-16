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

    #  connect
    client = TelegramClient(phone_num, api_id, api_hash)
    client.connect()

    # if user is not authorized yet
    # send code and enter auth code
    if not client.is_user_authorized():
        client.send_code_request(phone_num)
        client.sign_in(phone_num, input('Enter Auth Code Sent: '))

    if client.is_user_authorized():
        me = client.get_me()
        print('Connected as {} !'.format(me.username))

    # get chats
    chats = []
    print('Fetching chats...')
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

    # filter chats from groups
    # chats from groups megagroup is True
    groups = []
    print('Geting groups...')
    for c in chats:
        try:
            if c.megagroup == True:
                groups.append(c)
        except:
            continue
    x = 0
    if not groups:
        print('No groups found!')
        return
    for g in groups:
        print(str(x) + ' -- ' + g.title)
        x += 1
    print('Choose group or press X to Exit...')
    target_groups = []
    while True:
        try:
            user_input = input('Enter number: ')
            
        except EOFError:
            print('Something went wrong...  :(')
            break


if __name__ == '__main__':
    main()
