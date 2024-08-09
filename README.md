# Quack

Rede social desenvolvida em Django como projeto final na EBAC.

## **Requisitos**

```
Python 3.10.7 >
Poetry
```

- [Python 3.10.7](https://www.python.org/downloads/release/python-3107/)
- [Poetry](https://python-poetry.org/docs/#installation)

1. **Clone o Repositório**

   ```bash
   git clone https://github.com/JayfckZ/quack.git
   cd quack

2. **Instalar Dependências**

   Utilize o Poetry para instalar todas as dependências do projeto. No diretório do projeto, execute:

   ```
   poetry install
   ```

3. **Configurar o Ambiente**

   Ative o ambiente virtual criado pelo Poetry:

   ```
   poetry shell
   ```

4. **Configurar o Banco de Dados**

   Antes de rodar o servidor, você precisa configurar o banco de dados. Execute as migrações com o comando:

   ```
   python manage.py migrate
   ```

5. **Criar um Superusuário**

   Para criar um superusuário para acessar o painel de administração do Django, execute:

   ```
   python manage.py createsuperuser
   ```
   
6. **Rodar o Servidor**

    Agora você pode rodar o servidor de desenvolvimento do Django com:

    ```
    python manage.py runserver
    ```

    A aplicação estará disponível em http://127.0.0.1:8000/.