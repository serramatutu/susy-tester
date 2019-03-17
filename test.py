from argparse import ArgumentParser
import os
from collections import defaultdict
import subprocess
from termcolor import cprint
import difflib

class Logger:
    @staticmethod
    def _normalize_args(args):
        return ' '.join(map(str, args))

    def success(self, *args, **kwargs):
        cprint(Logger._normalize_args(args), color='green', **kwargs)

    def warn(self, *args, **kwargs):
        cprint(Logger._normalize_args(args), color='yellow', **kwargs)

    def info(self, *args, **kwargs):
        cprint(Logger._normalize_args(args), color='cyan', **kwargs)

    def error(self, *args, **kwargs):
        cprint(Logger._normalize_args(args), color='red', **kwargs)

    def log(self, *args, **kwargs):
        cprint(Logger._normalize_args(args), **kwargs)

logger = Logger()

def get_invoke(program_path):
    program_name, ext = os.path.splitext(program_path)
    if ext == '.py':
        return 'python3 ' + program_path
    elif ext == '.c':
        return 'gcc -std=c99 -o %s.exe; %s.exe' % (program_name, program_name)

def get_tests_dict(program_path):
    folder = os.path.dirname(program_path)
    tests = defaultdict(dict)
    for file_name in os.listdir(folder):
        name, ext = os.path.splitext(file_name)
        with open(os.path.join(folder, file_name), 'r') as file:
            tests[name][ext] = file.read()

    program_name, program_ext = os.path.splitext(program_path)
    program_name = os.path.basename(program_name)
    del tests[program_name][program_ext]
    del tests[program_name]

    return tests

def test_single(program_path, test_name, input, expected_output, encoding='utf-8'):
    program_invoke = get_invoke(program_path)
    try:
        completed_process = subprocess.run(
            program_invoke.split(' '),
            input=input.encode(encoding),
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        program_output = completed_process.stdout.decode(encoding)
        if program_output != expected_output:
            logger.error("The program has produced a different output than the expected")
            logger.log(''.join(difflib.ndiff(program_output, expected_output)))
            # logger.log(program_output)
            return False
    except subprocess.TimeoutExpired as e:
        logger.error('The program has timed out')
        return False
    except subprocess.CalledProcessError as e:
        logger.error('Process finished with non-zero code (%s)' % e.returncode)
        logger.log(e.stderr.decode(encoding))
        return False        

    return True

def summary(success, failed, program_path, encoding):
    logger.info('---------- TEST SUMMARY ----------', attrs=['bold'])
    if len(failed) <= 0:
        logger.success('PASSED!', attrs=['bold'])
    else:
        logger.error('FAILED!', attrs=['bold'])
        logger.info('Legend: (-) line unique to your program output (line error)')
        logger.info('        (+) line unique to the expected output (line error)')
        logger.info('        ( ) line common to both (ok)')
        logger.info('        (?) line not present in both (intraline error)')

    logger.log('Tested file: '.ljust(15) + program_path)
    logger.log('OS: '.ljust(15) + os.name)
    logger.log('Used encoding: '.ljust(15) + encoding)

    logger.success("Succeeded (%d): " % len(success), end='')
    logger.log(success)
    logger.error("Failed (%d): " % len(failed), end='')
    logger.log(failed)

def test(program_path, **kwargs):
    tests = get_tests_dict(program_path)

    succeeded_tests = []
    failed_tests = []
    for test_name, values in tests.items():
        logger.warn('RUNNING', test_name, attrs=['bold'])
        if test_single(program_path, test_name, values['.in'], values['.out'], **kwargs):
            succeeded_tests.append(test_name)
            logger.success('TEST SUCCEEDED')
        else:
            failed_tests.append(test_name)
            logger.error('TEST FAILED')
    summary(succeeded_tests, failed_tests, program_path, **kwargs)

    

        
        

if __name__ == "__main__":
    parser = ArgumentParser(description='Testa uma solução para um problema.')

    parser.add_argument(
        dest='path',
        type=str,
        help='The tested program path'
    )

    parser.add_argument(
        '-e',
        '--encoding',
        dest='encoding',
        default='utf-8',
        type=str,
        help='The encoding for the input and output files'
    )

    args = parser.parse_args()

    test(args.path, encoding=args.encoding)