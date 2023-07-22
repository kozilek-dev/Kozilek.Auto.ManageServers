# Gerenciador de servidores Minecraft

[![CI](https://github.com/kozilek-dev/Kozilek.Auto.ManageServers/actions/workflows/ci-pipeline.yml/badge.svg)](https://github.com/kozilek-dev/Kozilek.Auto.ManageServers/actions/workflows/ci-pipeline.yml)
[![CD](https://github.com/kozilek-dev/Kozilek.Auto.ManageServers/actions/workflows/cd-pipeline.yml/badge.svg)](https://github.com/kozilek-dev/Kozilek.Auto.ManageServers/actions/workflows/cd-pipeline.yml)

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