def execute(users_by_roles: dict) -> str:
    """
    assign users new groups (client roles) in dict
    and nullify old ones (system roles)
    :param users_by_roles: key - role(s), value - list of users
    Example:
    {
    'role1': ['user1', 'user2', ... ],
    'role2': ['user0'],
    ('role3', 'role4'): ['user9', 'user10']
    }
    :return: status
    """
    fields = {'groups': [], 'customGroups': None}
    for group, users in users_by_roles.items():
        if type(group) != str:
            fields['customGroups'] = [*group]
        else:
            fields['customGroups'] = [group]
        [print(user_id, fields) for user_id in users]

    return 'Roles transitioned'
