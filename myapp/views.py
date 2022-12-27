from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from myapp.forms import TodoListForm 
from myapp.models import Status, TodoList

# Create your views here.
def create_item(request):
    todo = TodoList.objects.all() # Query com todos objetos da lista
    status_list = Status.objects.all()
    if request.method == "POST": # para POST
        form = TodoListForm(request.POST)  
        if form.is_valid():
            form.save() # salva informação
            return redirect('/')
        
    form = TodoListForm() # Formulário
    context = {"form" : form, 'todo': todo, 'status_list': status_list}
    return render(request, 'index.html', context)


def delete_item(request):
    todo_id  = request.GET.get('todo_id') # Id da Lista
    todo = TodoList.objects.get(id=todo_id) # Pega Objeto
    todo.delete() # Deleta
    data = {'status':'delete'}
    return JsonResponse(data)


def update_item(request):  
    data_id  = request.GET.get('data_id') # Id da Lista
    title = request.GET.get('title') # Id do status
    print(data_id, title)

    todo = get_object_or_404(TodoList,id=data_id) # Get Objeto lista
    todo.title = title # status recebe novo valor "Id do status"
    todo.save() # salva  

    data = {'status':'update-item', 'title':title}
    return JsonResponse(data) # retorna


def update_status(request):  
    data_id  = request.GET.get('data_id') # Id da Lista
    status_id = request.GET.get('status_id') # Id do status 
    
    status = Status.objects.get(id=status_id) # Get objeto status 

    todo = get_object_or_404(TodoList,id=data_id) # Get Objeto lista
    todo.status = status # status recebe novo valor "Id do status"
    todo.save() # salva  
    
    data = {'status':status_id}
    return JsonResponse(data)