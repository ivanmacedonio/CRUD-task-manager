
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model): #creamos la tabla 
    title= models.CharField(max_length=20)
    description= models.TextField(blank=True) #si no envian nada por defecto queda vacio 
    created= models.DateTimeField(auto_now_add=True) #si no le envian nada carga la fecha de creacion automatico ACTUAL
    datedcompleted= models.DateTimeField(null= True) #permite guardar valores vacios
    important= models.BooleanField(default=False)
    user= models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__ (self):

        return self.title + '- by' + self.user.username


'''Por defecto django guarda los datos de user en una tabla 
generada automaticamente, por eso si importamos user (tabla con datos propios)
podemos decir que el usuario que realizo una tarea va a ser el que comparta
campo clave con la tabla de usuarios, donde relacionamos los datos entre si

El cascade hace referencia a que si se elimina el campo con el que se relaciona
directamente la tarea, se elimina la tarea. Si se elimina el user 2, todas 
las tareas con campo clave 2 se eliminaran


'''