from db import smd_admins

if __name__ == '__main__':
    username = input('Username: ')
    password = input('Password: ')
    disp_name = input('DisplayName: ')
    smd_admins.new_admin(username, password, disp_name)
    print('OK')
