import db_controller
import payments


def default_users_types():
    users_types_list = ["user", 'admin', 'security']
    for x in users_types_list:
        db_controller.TypesOfUsers().insert(x)


def append_table_with_apt_code(dummy_code=None):
    if dummy_code is None:
        data = payments.Payments().get_all_apt_codes()
        for x in data:
            db_controller.Apartments().insert(x)
    else:
        db_controller.Apartments().insert(dummy_code)



"""append_table_with_apt_code("Test 1")
append_table_with_apt_code("Test 2")
append_table_with_apt_code("Test 3")"""
