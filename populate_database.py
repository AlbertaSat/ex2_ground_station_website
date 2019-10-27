from groundstation.backend_api.utils import add_telecommand, create_context

@create_context
def populate_commands_table():

    commands = {
        'ping': (0,False),
        'get-hk':(0,False),
        'turn-on':(1,True),
        'turn-off':(1,True),
        'set-fs':(1,True),
    }

    for name, (num_args, danger) in commands.items():
        c = add_telecommand(command_name=name, num_arguments=num_args, is_dangerous=danger)
        print(f'{c.command_name} added successfully to db!')

if __name__=='__main__':
    populate_commands_table()