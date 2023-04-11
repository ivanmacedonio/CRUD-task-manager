from django.forms import ModelForm
from .models import Task

class TaskForm(ModelForm):

    class Meta:

        model = Task
        fields = ['title', 'description', 'important']





'''importamos la tabla en la que vamos a bazar el formulario para no 
tener que copiar las variables de la tabla una por una en el form 

indicamos una clase llamada meta la cual va a contener un modelo el cual 
va a guardar las variables de la tabla que le indiquemos e importemos, en
este caso task. le indicamos que campos va a tomar el formulario. A LA 
VIEW le enviamos el formulario como ya hicimos anteriormente y lo cargamos 
en el html para el front'''