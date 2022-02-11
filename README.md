# Dependências

Este exemplo utiliza um pacote python chamado geoserver-rest.
Para instalá-lo é necessário ter um gdal instalado na máquina.
Num ambiente ubuntu linux (20.04) foram instalados os seguintes pacotes:

```bash
sudo apt install libgdal-dev gdal-data gda-bin
```

A versão instalada no exemplo foi a 3.0.4

## Virtualenv
É necessário criar e ativar um virtualenv para instalação dos pacotes
```bash
cd diretorio_do_projeto/
python -m venv .venv
source .venv/bin/activate
```

Após a instalação das dependências do sistema, é necessário 'pinar' 
a versão a ser instalada no pip. 'Pinar' significar definir  a versão especpifica
do pacote.  
Em vez de usar `pip install gdal`, deve-se usar `pip install gdal==3.0.4`

Somente depois desta instalação deve-se instalar o geoserver-rest e o restante
dos pacotes contidos no requirements.txt.
```bash
pip install -r requirements.txt
```

## Como testar (SEM DOCKER)

1. Geoserver
    1.1 Alternativa 1: Baixar o Geoserver e rodar localmente na porta 8080. 
    1.2 Utilizar um geoserver existente ao qual tenha acesso (**Cuidado ao Utilizar esta opção!**)
2. Criar o virtualenv e instalar os pacotes necessários conforme descrito acima.
3. Criar um arquivo .env e configurar variáveis de ambiente contidas no arquivo **example_env**
4. Configurar e rodar o Flask:
```bash
export FLASK_APP=uploader.py
export FLASK_ENV=development
flask run
```



