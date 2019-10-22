from groundstation.backend_api.utils import add_command, create_context

@create_context
def populate_commands_table():

    commands = {
        'ping':0,
        'get-hk':0,
        'turn-on':1,
        'turn-off':1,
        'set-fs':1
    }

    for name, num_args in commands.items():
        c = add_command(command_name=name, num_arguments=num_args)
        print(f'{c.command_name} added successfully to db!')

if __name__=='__main__':
    populate_commands_table()
