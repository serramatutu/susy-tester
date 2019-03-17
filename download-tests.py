import os
import requests
from argparse import ArgumentParser

def get_susy_url(class_name, activity_number, test_number):
    return 'https://susy.ic.unicamp.br:9999/{}/{:02d}/dados/arq{:02d}.in' \
            .format(class_name, activity_number, test_number)

def download_to_file(url, file):
    file_contents = get_remote_file_contents(url)
    if file_contents:
        with open(file, 'w') as stream:
            stream.write(file_contents)
        return True
    return False

def get_remote_file_contents(url):
    r = requests.get(url, verify=False)
    if r.text.find("Sistema SuSy") >= 0: # susy n tem 404 :(
        return None
    return r.text

def download_tests(dest_folder, class_name, activity_number):
    os.makedirs(dest_folder, exist_ok=True)

    test_number = 1
    while True:
        url = get_susy_url(class_name, activity_number, test_number)
        test_file_name = os.path.join(dest_folder, 'arq{:02d}'.format(test_number))
        if not download_to_file(url, test_file_name+'.in'):
            break
        download_to_file(url, test_file_name+'.out')

        test_number += 1


if __name__ == '__main__':
    parser = ArgumentParser('Extrai arquivos de teste do SuSy')
    parser.add_argument(
        dest='dest_folder',
        type=str,
        help='A pasta de destino para os arquivos de teste'
    )
    parser.add_argument(
        dest='class_name',
        type=str,
        help='Nome da sala'
    )
    parser.add_argument(
        dest='activity_number',
        type=int,
        help='O número da atividade/lab'
    )

    args = parser.parse_args()

    download_tests(args.dest_folder, args.class_name, args.activity_number)
