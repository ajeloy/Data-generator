# Data-generator
Simple Script que genera una cantidad establecida por el usuario de registros con campos aleatorios.

# Descripción
El script generator.py busca insertar automáticamente datos aleatorios en una determinada base de datos Mysql.

# Ejecución
usage: generator.py [-h] user password database table rows

Arguments

positional arguments:
  user        Username
  password    Password
  database    Database name
  table       Table name
  rows        Number of rows to insert

options:
  -h, --help  show this help message and exit

# Ejemplo
python generator.py username pass database table 200
