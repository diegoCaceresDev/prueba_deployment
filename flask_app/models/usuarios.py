import os

from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.utils.expresiones_regulares import EMAIL_REGEX


class Usuario:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    def __str__(self) -> str:
        return f"{self.email} ({self.id})"

    @classmethod
    def validar(cls, formulario):
        """
        Valida si los datos recibidos por el usuario son correctos
        """
        errores = []
        if not EMAIL_REGEX.match(formulario['email']):
            errores.append(
                "El correo indicado es inválido"
            )

        if cls.get_by_email(formulario['email']):
            errores.append(
                "el correo ya existe"
            )

        if len(formulario['first_name']) < 2:
            errores.append(
                "El nombre debe tener al menos 2 caracteres"
            )

        if len(formulario['last_name']) < 2:
            errores.append(
                "El apellido debe tener al menos 2 caracteres"
            )

        return errores

    @classmethod
    def get_all(cls):
        """
        Obtiene todos los datos de los usuarios
        """
        resultados_instancias = []
        query = "SELECT * FROM users"
        resultados = connectToMySQL(os.getenv('BASE_DATOS')).query_db(query)
        for resultado in resultados:
            instancia = cls(resultado)
            resultados_instancias.append(instancia)

        return resultados_instancias


    @classmethod
    def save(cls, data ):
        """
        Guarda un nuevo usuario en la base de datos
        """
        print(data)
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )


    @classmethod
    def get(cls, id ):
        """
        Obtener todos los datos de un usuario a traves de su 'ID'
        """
        query = "SELECT * FROM users WHERE id = %(id)s;"
        data = { 'id': id }
        resultados = connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
        if resultados:
            return cls(resultados[0])
        
        return None
    
    @classmethod
    def get_by_email(cls, email ):
        """
        Obtener todos los datos de un usuario a traves de su 'Email'
        """
        query = "SELECT * FROM users WHERE email = %(email)s;"
        data = { 'email': email }
        resultados = connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
        if resultados:
            return cls(resultados[0])
        
        return None
    
    
    @classmethod
    def eliminar(cls, id ):
        """
        Elimina todos los datos de un usuario a traves de su 'ID'
        """
        query = "DELETE FROM users WHERE id = %(id)s;"
        data = { 'id': id }
        connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
        return True

    def delete(self):
        """
        Elimina todos los datos de un usuario a traves de su 'ID'
        """
        query = "DELETE FROM users WHERE id = %(id)s;"
        data = { 'id': self.id }
        connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
        return True

    def update(self):
        query = "UPDATE users SET password = %(password)s, updated_at = NOW() WHERE id = %(id)s"
        data = {
            'id': self.id,
            'password': self.password
        }
        connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
        return True
