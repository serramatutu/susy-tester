# susy-tester
Corretor automático de exercícios do SuSy (sem gastar suas submissões!)

## instalação
```
git clone https://github.com/serramatutu/susy-tester
cd susy-tester 
python3 setup.py install
python3 -m pip install -e .
```

## uso
Abra um terminal na pasta do seu projeto e execute o abaixo.

```
python3 -m susytester [--download turma trabalho] FILENAME
```

### flags:
```--download```: especifica opções de download automático de testes caso eles ainda não estejam na sua máquina. 

### exemplos
```python3 -m susytester --download mc102w 01 lab01.py```

---

## TODO:
- consertar suporte com GCC
- adicionar suporte a mais linguagens
- blacklist de testes (para pular)
- variáveis de ambiente (?)