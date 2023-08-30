import os

from flask_app.config.mysqlconnection import connectToMySQL

from flask_app.models.usuarios import Usuario

class Show:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.title = data['title']
        self.network = data['network']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.released_date = data['released_date']
        self.author = []


    @classmethod
    def validar(cls, formulario):
        """
        Valida si los datos recibidos por el usuario son correctos
        """
        errores = []

        if len(formulario['title']) < 3:
            errores.append(
                "El titulo debe tener al menos 3 caracteres"
            )

        if len(formulario['network']) < 3:
            errores.append(
                "El Network debe tener al menos 3 caracteres"
            )
            
        if len(formulario['description']) < 3:
            errores.append(
                "La descripcion debe tener al menos 3 caracteres"
            )

        return errores


    @classmethod
    def get_all(cls):
        """
        Obtiene todos los datos de los shows
        """
        resultados_instancias = []
        query = "SELECT * FROM shows"
        resultados = connectToMySQL(os.getenv('BASE_DATOS')).query_db(query)
        for resultado in resultados:
            instancia = cls(resultado)
            resultados_instancias.append(instancia)

        return resultados_instancias
    
    
    @classmethod
    def save(cls, data ):
        """
        Guarda un nuevo show en la base de datos
        """
        print(data)
        query = """INSERT INTO shows (`title`, `network`, `description`, `user_id`, `released_date`) 
        VALUES (%(title)s, %(network)s, %(description)s, %(user_id)s, %(released_date)s);"""
        return connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )


    @classmethod
    def get_by_id(cls, id ):
        """
        Obtener todos los datos de un show a traves de su 'ID'
        """
        query = "SELECT * FROM shows LEFT JOIN users ON shows.user_id = users.id  WHERE shows.id = %(id)s;"
        data = { 'id': id }
        resultados = connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
        
        show = cls(resultados[0])
        author = {
            'first_name': resultados[0]['first_name'],
            'last_name': resultados[0]['last_name']
        }
        
        show.author.append( author)
        
        print(vars(show))
        
        return show
    
    
    @classmethod
    def delete(cls, id ):
        """
        Elimina todos los datos de un show a traves de su 'ID'
        """
        query = "DELETE FROM shows WHERE id = %(id)s;"
        data = { 'id': id }
        connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
        return True
    
    
    @classmethod
    def update(cls, data ):
        """
        Actualiza todos los datos de un show a traves de su 'ID'
        """
        query = "UPDATE shows SET `title` = %(title)s, `network` = %(network)s, `description` = %(description)s, `released_date` = %(released_date)s WHERE (`id` = %(id)s);"

        connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
        return True
    
