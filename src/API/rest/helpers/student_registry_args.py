
def add_args_keys(parser):
    arg_keys = ['matricula', 'email', 'nome', 'foto']
    for k in arg_keys:
        parser.add_argument(k)