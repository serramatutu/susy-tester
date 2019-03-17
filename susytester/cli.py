import os
from argparse import ArgumentParser, Action
from susytester.logger import PrettyLogger
from susytester.test import test

logger = PrettyLogger()

class ParseDownloadOptions(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        download_options = {
            "class_name": values[0],
            "activity_number": int(values[1])
        }
        setattr(namespace, self.dest, download_options)

def main():
    parser = ArgumentParser(description='Testa uma solução para um problema.')

    parser.add_argument(
        dest='program_name',
        type=str,
        help='Nome do programa testado'
    )

    parser.add_argument(
        '--download',
        '--d',
        dest='download_options',
        type=str,
        action=ParseDownloadOptions,
        nargs=2,
        help='Opções de download de testes. [turma lab]'
    )

    args = parser.parse_args()

    directory = os.path.dirname(os.path.realpath(args.program_name))

    program_path = os.path.join(directory, args.program_name)
    # try:
    test(program_path, download_options=args.download_options)
    # except Exception as e:
    #     print(e)
    #     logger.log(e.args[0])