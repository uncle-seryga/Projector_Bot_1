import db_controller


def default_users_types():
    users_types_list = ["user", 'admin', 'security']
    for x in users_types_list:
        db_controller.TypesOfUsers().insert(x)

