# Gerenciador de servidores Minecraft

### Instalar dependências

```commandline
pip install -r requirements.txt
```

### Como rodar a API
> Rode a partir da raíz do projeto

```commandline
uvicorn api.main:app --reload
```


### Como testar

```commandline
python -m unittest manager/tests/manager_test.py
```