import os
from collections import defaultdict
import subprocess
from termcolor import cprint
import difflib

from susytester.logger import PrettyLogger
from susytester.download import download_tests

logger = PrettyLogger()

def get_invoke(program_path):
    program_name, ext = os.path.splitext(program_path)
    if ext == '.py':
        return 'python3 ' + program_path
    elif ext == '.c':
        return 'gcc -std=c99 -o {0}.exe {1}; {0}.exe'.format(program_name, program_path)

def get_tests_dict(program_path, download_options=None):
    folder = os.path.join(os.path.dirname(program_path), 'tests')
    tests = defaultdict(dict)

    if not os.path.exists(folder):
        if not download_options:
            raise ValueError("Não foram fornecidos testes. Use a flag --download se quiser baixá-los")
        logger.info("Baixando testes", attrs=['bold'])
        download_tests(folder, download_options['class_name'], download_options['activity_number'])
        

    for file_name in os.listdir(folder):
        name, ext = os.path.splitext(file_name)
        with open(os.path.join(folder, file_name), 'r') as file:
            tests[name][ext] = file.read()

    program_name, program_ext = os.path.splitext(program_path)
    program_name = os.path.basename(program_name)

    return tests

def test_single(program_path, test_name, input, expected_output):
    program_invoke = get_invoke(program_path)
    try:
        completed_process = subprocess.run(
            program_invoke.split(' '),
            input=input.encode('utf-8'),
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        program_output = completed_process.stdout.decode('utf-8').split('\n')
        expected_output = expected_output.split('\n')
        if program_output != expected_output:
            logger.error("O programa produziu uma saída diferente da esperada")
            logger.log('\n'.join(difflib.ndiff(program_output, expected_output)))
            return False
    except subprocess.TimeoutExpired as e:
        logger.error('O programa deu timeout')
        return False
    except subprocess.CalledProcessError as e:
        logger.error('Processo terminou com código não-nulo (%s)' % e.returncode)
        logger.log(e.stderr.decode('utf-8'))
        return False

    return True

def summary(success, failed, program_path):
    logger.info('---------- RESUMO DOS TESTES ----------', attrs=['bold'])
    if len(failed) <= 0:
        logger.success('PASSOU!', attrs=['bold'])
    else:
        logger.error('FALHOU!', attrs=['bold'])
        logger.info('Legenda: (-) linha exclusiva da saída do seu programa (line error)')
        logger.info('         (+) linha exclusiva da saída esperada (line error)')
        logger.info('         ( ) linha comum a ambas as saídas (ok)')
        logger.info('         (?) linha não presente em ambas (intraline error)')

    logger.log('File: '.ljust(15) + program_path)
    logger.log('OS: '.ljust(15) + os.name)

    logger.success("Sucesso (%d): " % len(success), end='')
    logger.log(success)
    logger.error("Falha (%d): " % len(failed), end='')
    logger.log(failed)

def test(program_path, **kwargs):
    tests = get_tests_dict(program_path, **kwargs)

    succeeded_tests = []
    failed_tests = []
    for test_name, values in sorted(tests.items(), key=lambda item: item[0]):
        logger.warn('EXECUTANDO', test_name, attrs=['bold'])
        if test_single(program_path, test_name, values['.in'], values['.out']):
            succeeded_tests.append(test_name)
            logger.success('TESTE PASSOU')
        else:
            failed_tests.append(test_name)
            logger.error('TESTE NÃO PASSOU')
    summary(succeeded_tests, failed_tests, program_path)