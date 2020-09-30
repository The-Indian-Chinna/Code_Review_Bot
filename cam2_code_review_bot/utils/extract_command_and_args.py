def extract_command_and_args(command_and_args):

    if " " not in command_and_args:
        return command_and_args, []

    # Pull the command from the beginning
    command = command_and_args[: (command_and_args.find(" "))]
    args_str = command_and_args[(command_and_args.find(" ") + 1) :]

    # The array of arguments and the command
    args = []

    # If there are quotes, accept the spaces as characters
    found_quote = False
    arg = ""

    for i in range(0, len(args_str)):
        if args_str[i] == '"':
            found_quote = not found_quote
        # Append argument if a space not in a quote is found
        elif args_str[i] == " " and not found_quote:
            args.append(arg)
            arg = ""
        else:
            arg += args_str[i]

    # Raise an error for an unclosed quote
    if found_quote:
        raise ValueError("Quote was not closed in argument")

    # Append the last argument
    args.append(arg)

    return command, args
