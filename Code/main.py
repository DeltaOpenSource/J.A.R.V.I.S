import listen
import commands

if __name__ == "__main__":
    for command in listen.listening():
        if command:
            print(command)
            commands.handler_commands(command)
        else:
            print("Не удалось распознать речь.")