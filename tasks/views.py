from django.shortcuts import render, redirect, get_object_or_404
from .forms import TaskForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.

def home (request):

    return render(request, 'home.html')

def signup (request):

    if request.method == 'GET':

        return render (request, 'signup.html', {
            'form': UserCreationForm
        })

    else:
        if request.POST['password1'] == request.POST['password2']:
            try: 
                #register user
                user= User.objects.create_user(username=request.POST['username'], 
                                     password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
             
            except IntegrityError:
                return render (request, 'signup.html', {

                    'form': UserCreationForm,
                    'error': 'username already exist'
                })               
        return render (request, 'signup.html', {

                    'form': UserCreationForm,
                    'error': 'password NOT match'
                })
   
   
            
        

#si las contraseñas no coinciden cae directo al httpresponse, si coinciden 
#usamos la clase user de django para crear usuarios y decimos que los datos de 
#esa clase imortada son provenientes de el post y el save lo valida para 
#cargarse en la bbdd

#la funcion del try es que podamos devolver otro httpresponse en caso de 
#un error con el nombre del error, ademas de evitar que caiga el programa 

# en caso de caer en el except, en vez de que caiga el programa vuelve  
#a ejecutar el formulario de signup pero acompañado de una variable error
#la cual debemos llamar dentro del html para que aparezca, recordemos
#que el error solo le llega por parametro en caso de que se incumpla alguna
#condicion dentro del login, como password not match o que el user ya existia
#
@login_required   
def tasks(request):

    tasks= Task.objects.filter(user=request.user, datedcompleted__isnull= True)

    return render(request, 'tasks.html', {

        'tasks': tasks
    })
@login_required   
def task_detail(request, task_id):
    if request.method == 'GET':
        #task= Task.objects.get(pk=task_id)
        task= get_object_or_404(Task, pk=task_id, user=request.user)
        form= TaskForm(instance=task) #rellenamos el formulario con los valores de task y lo guardamos en una variable
        #y se lo pasamos al html
        return render (request, 'task_detail.html', {'task': task , 'form': form})
    else:
          try:
                task= get_object_or_404(Task, pk=task_id, user=request.user)
                form=TaskForm(request.POST, instance=task)
                form.save()
                return redirect('tasks')
          except ValueError:
                return render (request, 'task_detail.html', {'task': task , 'form': form, 'error': 'Error update'})


'''le enviamos una id a el detalle mediante la url y en la variable
task se guardan los datos de la tarea que le coincida la primary key 
con la id enviada, y nos retorna el html que recibe la tarea tomada por el get
dejo comentada esa opcion, pues puede caer la pagina indicando un numero
inexistente, asique usamos la importada get or 404, donde le enviamos 
el model donde debe buscar la id, y la variable con la que se compara la pk'''

def signout (request):

    logout(request)

    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {

        'form': AuthenticationForm
    })
    else:
        user= authenticate(request, username=request.POST['username'],
                     password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {

        'form': AuthenticationForm,
        'error': 'Username or password incorrect'
    })  
        else:
            login(request, user)
            return redirect('tasks')





'''
si los datos llegan por post, vamos a verificar con authenticate si el user 
existe en la base de datos. si la variable queda vacia significa que no existe
ningun ususario con esos datos, por ende nos retorna a la pagina de logueo
seguido de un error que dicee user or pass incorrect. En caso de que si 
exista y la variable no este vacia, guadamos su sesion con login y lo enviamos
a la pagina 
'''
@login_required   
def create_task(request):

    if request.method == 'GET':

        return render (request, 'create_task.html', {

        'form': TaskForm
    })

    else:
        try:

            form= TaskForm(request.POST)
            #Taskform genera formularios con los datos que le enviemos 
            new_task = form.save(commit=False)
            new_task.user= request.user
            new_task.save()
            return redirect('tasks')
        
        except ValueError:

            return render (request, 'create_task.html', {

                'form': TaskForm,
                'error': 'Por favor indique datos validos'
            })
        
'''

creamos una variable formulario la cual almacena las 3 variables tal como indicamos 
en el forms.

la variable formulario va a gaurdar los datos PERO NO LOS ENVIA A LA BBDD (
eso es el commit) , unicamente los guarda en la variable tarea


el usuario de la tarea va a ser el mismo que le corresponda a la sesion 
que envio la tarea, es decir, el usuario que estaba logueado cuando se creo

se envia la tarea a la bbdd 

se redirecciona a la pagina de tareas una vez terminamos el procedimiento
'''
@login_required   
def complete_task(request, task_id):

    task= get_object_or_404(Task, pk=task_id, user= request.user)

    if request.method == 'POST':
        task.datedcompleted = timezone.now()
        task.save()
        return redirect ('tasks')
    
@login_required   
def delete_task(request, task_id):

    task= get_object_or_404(Task, pk=task_id, user= request.user)

    if request.method == 'POST':
        task.delete()
        return redirect ('tasks')






'''
creamos una view la cual guarda en una variable las tareas que correspondan
al modelo Task, usando de filtro el id de la tarea y el usuario logueado

si vamos a indicar que una tarea fue compeltada es info nueva, pues la tarea 
ya tenia una propiedad que indicaba incompleta y la info nueva va a modificar
esta propiedad. en fecha de finalizacion le indicamos una funcion importad que 
devuelve el horario actual, guarda la variable cambiada y redirecciona a tasks
 '''

@login_required   
def tasks_completed(request):

    tasks= Task.objects.filter(user=request.user, datedcompleted__isnull= False)

    return render(request, 'tasks.html', {

        'tasks': tasks
    })
