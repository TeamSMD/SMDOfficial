from db import artExpo_works, artExpo_users, artExpo_transaction_log, smd_admins


if __name__ == '__main__':
    artExpo_transaction_log.make_table()
    artExpo_users.make_table()
    artExpo_works.make_table()
    smd_admins.make_table()
