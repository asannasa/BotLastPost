from dotenv import set_key, find_dotenv

env_file = find_dotenv()
if env_file == '':
    env_file = open(".env", "x")
    env_file.close()
    # print('File created')

# print(f'File name: {find_dotenv()}')
try:
    set_key(find_dotenv(), "TOKEN", input('Enter TOKEN: '))
    set_key(find_dotenv(), "TIME", input('Enter message interval: '))
    set_key(find_dotenv(), "ADMIN", input(
        'Enter the admin id of the bot (separated by commas if there are multiple admins): '))
except KeyboardInterrupt as err:
    print("\nExit of settings.py")
    raise SystemExit(1)
finally:
    exit(0)
