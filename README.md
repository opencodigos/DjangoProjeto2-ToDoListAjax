# Django: TO DO LIST

Nesse tutorial vamos desenvolver um to do list com Django. E conhecer o poder do AJAX para deixar as coisas mais dinâmicas.

Repositório inicial: https://github.com/djangomy/config-default-simple

Depois de feito as configurações iniciais e executado o projeto. 

Vamos para criação do nosso modelo e estrutura do projeto.

- **Modelando Projeto**
    
    Vamos criar duas tabelas. A primeira é **TodoList** e uma outra **Status,** que serve ****para criar o droplist das informações dos status exemplo: **“⛔️ a Fazer, ⚠️ Fazendo e ✅ Finalizado”.** Poderíamos deixar essas informações fixas em um simples array. Mas achei melhor criar uma tabela onde usuário pode customizar essas informações.
    
    Na tabela **TodoList** vamos criar um campo tipo ***ForeignKey*** relacionando com tabela status. Note que `to_field='id', default='1'` ao adicionar essas duas tags, que significa que para *field id* da tabela **Status** colocar como *default* o item de Id=1. Sempre que criarmos um formulário partir dessa tabela TodoList o campo ‘status” já terá um **valor default.**
    
    ***myapp/templates/models.py***
    
    ```python
    from django.db import models
    
    class Status(models.Model):
        name = models.CharField(max_length=20)
        
        def __str__(self):
            return self.name
        
    
    class TodoList(models.Model):
        title = models.CharField(max_length=100)
        status = models.ForeignKey(Status, on_delete=models.CASCADE, 
                                   related_name='status', to_field='id', default='1') 
       
        def __str__(self):
            return self.title
    ```
    
    No template HTML vamos ter um formulário simples de um campo somente para adicionar um item na lista. Então, teremos que configurar o forms e adicionar classes bootstrap para esse campo “***title***”. 
    
    Note que `exclude = ('status',)` quando adiciono essa tag significa que estou excluindo esse campo status do formulário. Como foi dito acima esse campo inicialmente já recebe um valor default.
    
    ***myapp/forms.py***
    
    ```python
    from django import forms 
    from .models import TodoList
    
    class TodoListForm(forms.ModelForm):  
         
        class Meta:
            model = TodoList
            fields = ('title',)
            exclude = ('status',)
        
        def __init__(self, *args, **kwargs): # Adiciona 
            super().__init__(*args, **kwargs)  
            for field_name, field in self.fields.items():   
                  field.widget.attrs['class'] = 'form-control'
    ```
    
    Na views do projeto vamos adicionar essas duas funções. ***create_item*** onde vamos fazer um post para criar um item na lista. E função ***delete_item*** para deletar um item da lista.
    
    **myapp/views.py**
    
    ```python
    def create_item(request):
        todo = TodoList.objects.all() # Query com todos objetos da lista
        if request.method == "POST": # para POST
    				form = TodoListForm(request.POST)  
            if form.is_valid():
                form.save() # salva informação
                return redirect('/')
            
        form = TodoListForm() # Formulário
        context = {"form" : form, 'todo': todo}
        return render(request, 'index.html', context)
    
    def delete_item(request, id):
        todo = TodoList.objects.get(id=id) # pega o objeto
        todo.delete() # deleta
        return redirect('index')
    ```
    
    Criar as rotas para acessar nossas views.
    
    **myapp/urls.py**
    
    ```python
    from django.urls import path 
    from myapp import views
    
    urlpatterns = [
        path('', views.create_item, name='create_item'),  
        path('delete/<int:id>/', views.delete_item, name="delete"),
    ]
    ```
    
    No nosso template *index.html* vamos adicionar nosso {{form}} e rodar a aplicação para testar. 
    
    **No momento não estamos utilizando Ajax para deixar as coisas mais dinâmicas. Apenas estamos fazendo as configurações iniciais e testando “estrutura” do projeto.**
    
    Estou utilizando ícones dessa biblioteca **Font Awesome**.
    
    Segue documentação para instalar via CDN ou PIP. Você escolhe.
    
    [https://fontawesome.com/v5/docs/web/use-with/wordpress/install-manually](https://fontawesome.com/v5/docs/web/use-with/wordpress/install-manually)
    
    ***myapp/base/templates/base.html***
    
    ```html
    # prefiro utilizar versão free CDN.
    <head>
    	 ....
    	<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.15.4/css/all.css" integrity="sha384-DyZ88mC6Up2uqS4h/KRgHuoeGwBcD4Ng9SiP4dIRy0EXTlnuz47vAwmeGwVChigm" crossorigin="anonymous"/>
     
    </head>
    ```
    
    ***myapp/templates/index.html***
    
    ```html
    {% extends 'base.html' %}
    
    {% block title %}Pagina 1{% endblock %}
    
    {% block content %}
    	<h2>Pagina 1</h2> 
    
    	<div class="p-5">
    
    		<form class="d-flex gap-4 col-md-6" method="POST"> 
    	      {% csrf_token %}  
                <button type="submit" class="btn btn-success"><i class="fa fa-plus"></i></button> 
                {{form}}  
    		</form>    
    
    		<table class="table"> 
    
                <thead>
                    <tr>
                        <th scope="col">Titulo</th> 
                        <th scope="col">Status</th>
                        <th scope="col">Deletar</th> 
                    </tr>
                </thead>
    
                {% for el in todo %} # são as linhas que vão repetir
                <tbody>
                    <tr class="table align-middle">
                        <th scope="row">{{el.title}}</th>  
                        <th scope="row">{{el.status}}</th> 
                        <th scope="row">
                            <a class="btn" href="{% url 'delete' el.id %}"><i class="fa fa-trash link-danger"></i></a>
                        </th> 
                    </tr>
                </tbody>  
                {% endfor %}
    
            </table>    
    
    	</div> 
    {% endblock %}
    ```
    
- **Configurar AJAX**
    
    Primeiro para usar o AJAX precisamos importar jquery no nosso projeto. 
    
    Pode pegar o CDN daqui [https://releases.jquery.com/](https://releases.jquery.com/)
    
    ```html
     <body>
    	...
    	<script src="https://code.jquery.com/jquery-3.6.1.min.js" integrity="sha256-o88AwQnZB+VDvE9tvIXrMQaPlFFSUTR+nldQm1LuPXQ=" crossorigin="anonymous"></script>
      
    	{% block scripts %} {% endblock %}
    </body>
    </html>
    ```
    
- **Atualizar Titulo da Lista**
    
    ## Atualizar titulo da lista com AJAX.
    
    Primeiro pensei nessa estrutura. O usuário clica no titulo e aparece o formulário para editar. Então vou ter duas tags:
    
    1 - Adicionei uma “***div*”** para “***title***”. E criei um atributo para ***data-title*** que recebe o identificador do item da lista. E com esse ***data-title*** conseguimos chamar via Ajax e pegar o id.
    
    2 - <form> se inicia Oculto. Esse formulário só vai aparecer quando clicar em cima do titulo. Esse form não tem nenhuma novidade. é um campo **input** e **botão submit.** 
    
    **Lembrando Método GET** 
    
    ```html
    <th scope="row" style="width:35rem;">
    
    	<div class="title" id="title{{el.id}}" data-title="{{el.id}}">{{el.title}}</div>
    	
    	<form class="d-none d-flex" id="form-title{{el.id}}" method="GET" style="width:35rem;">
    		<input class="form-control" type="text" id="inputText{{el.id}}" value="{{el.title}}">
    		<button type="submit" class="btn" id="edit{{el.id}}"><i class="fa fa-edit link-warning"></i></button>
    	</form>
    
    </th>
    ```
    
    Debaixo de *{% endblock %}* vamos chamar tag script assim: *{% block scripts %}*.
    
    Nessas duas linhas de destaque em amarelo é feita aquela jogada. Quando usuário clicar em cima do titulo aparece o campo para editar e remove o contexto anterior. 
    
    Logo mais abaixo quando `success: function (data)` recebemos uma resposta do servidor de que a informação foi salva. Então volta para configuração inicial. 
    
    Nota que precisamos adicionar no HTML essa resposta, para que usuário veja essa alteração acontecendo em tempo real. Assim que recebe a informação do servidor já atualiza no template HTML o resultado da alteração.
    
    ```jsx
    {% endblock %}
    
    {% block scripts %}
    <script type="text/javascript"> 
    		// Atualiza Titulo da Lista
    		$("div.title").click(function () {
    	
    			var data_id = $(this).attr("data-title");
    	
    			$("form#form-title" + data_id).removeClass('d-none')
    			$("div#title" + data_id).addClass('d-none')
    	
    			$('button#edit' + data_id).on("click", function (e) {
    				e.preventDefault();
    			  
    				title = $('input#inputText'+ data_id).val();
    	 
    				$.ajax({
    					type: 'GET',
    					url: '{% url "update-item" %}',
    					data: {'data_id': data_id,'title': title,},
    					datatype: "json",
    					success: function (data) {
    						if (data.status == "update-item") {
    							$("form#form-title" + data_id).addClass('d-none');
    							$("div#title" + data_id).removeClass('d-none'); 
    							$("#title" + data_id).html(data.title); 
    						}  
    					}
    				}); 
    
    			});
    		});
    </script> 
    {% endblock %}
    ```
    
    Na nossa views vamos criar uma função. Chamei de Update Item. 
    
    ```python
    def update_item(request):  
        data_id  = request.GET.get('data_id') # Id da Lista
        title = request.GET.get('title') # Id do status
        print(data_id, title)
    
        todo = get_object_or_404(TodoList,id=data_id) # Get Objeto lista
        todo.title = title # status recebe novo valor "Id do status"
        todo.save() # salva  
    
        data = {'status':'update-item', 'title':title}
        return JsonResponse(data) # retorna
    ```
    
- **Atualizar Status**
    
    ## Atualizar o Status do Item da Lista
    
    Vamos criar um select para atualizar o status do item.
    
    Esse ***status_list*** é um ***context*** que vamos configurar na views para listar todos os status que existe a partir do modelo **Status**. Na função **create_item** adicionamos esse **context.**
    
    `status_list = Status.objects.all()` .
    
    ```html
    <th scope="row">
    
    	<div class="SelDiv">
    		<select class="form-select" name="status" id="{{el.id}}">
    			{% for st in status_list %}
    				<option value="{{st.id}}" {% if el.status.id == st.id %}selected{% endif %}>
    				{{st.name}}
    				</option>
    			{% endfor %}
    		</select>
    	</div>
    
    </th>
    
    ```
    
    Nossa configuração AJAX fica assim…
    
    ```jsx
    	// Muda Status do Item da Lista
    	$("div.SelDiv select").on('change', function () {
    
    		var data_id = this.id;
    		var status_id = $(this).find('option').filter(':selected').val();
    
    		console.log("data_id: ", data_id, "status_id: ", status_id)
    		
    		$.ajax({
    			type: 'GET',
    			url: '{% url "update-status" %}',
    			data: {
    				'data_id': data_id,
    				'status_id': status_id,
    			},
    			datatype: "json",
    
    			success: function (data) {
    				console.log(data)
    			}
    
    		});
    	});
    ```
    
    Função vai receber esses dados e salvar na tabela.
    
    ```python
    def update_status(request):  
        data_id  = request.GET.get('data_id') # Id da Lista
        status_id = request.GET.get('status_id') # Id do status 
        
    		status = Status.objects.get(id=status_id) # Get objeto status 
        
    		todo = get_object_or_404(TodoList,id=data_id) # Get Objeto lista
        todo.status = status # status recebe novo valor "Id do status"
        todo.save() # salva  
        
    		data = {'status':status_id}
        return JsonResponse(data)
    ```
    
- **Deletar um Item da Lista**
    
    ## Deletar Item da Lista
    
    Para deletar um item da lista primeiro precisamos adicionar um botão template.
    
    Nota que adicionamos essa tag `data-delete="{{el.id}}"` Assim conseguimos fazer um “GET” via Ajax e pegar o identificador do item da lista. 
    
    Poderíamos aproveitar o identificador da tag tr#id. Optei por criar essa tag data-delete.
    
    ```html
    <th scope="row">
    	<a class="btn" id="btn-delete" data-delete="{{el.id}}"><i class="fa fa-trash link-danger"></i></a>
    </th>
    ```
    
    Para deletar é mesmo conceito dos outros. Nos passamos o identificador e na views é feito o filtro para deletamos o item da tabela. 
    
    Mas agora adicionamos uma regra no retorno. Por que quando deletamos um item o usuário não recebe essa atualização no frontend. Só é mostrado para usuário depois q atualiza a pagina. 
    
    Então fica assim, envio o identificador para views e delete acontece. Depois na função **“success”** vamos ter um retorno onde definimos uma condição. Se status for igual a **“delete”** pego o identificador da coluna e **remove()**.
    
    ```jsx
    	// Deleta um Item da Lista
    	$("a#btn-delete").on("click", function (e) {
    		e.preventDefault();
    
    		var todo_id = $(this).attr("data-delete");
    		console.log(todo_id);
    
    		$.ajax({
    			type: 'GET',
    			url: '{% url "delete" %}',
    			data: { 'todo_id': todo_id },
    			datatype: "json",
    			success: function (data) {
    
    				if (data.status == "delete") {
    					$("tbody tr#" + todo_id).fadeOut("slow", function () {
    						$("tbody tr#" + todo_id).remove();
    					});
    				} else {
    					// faz alguma coisa
    				}
    
    			}
    		});
    	})
    ```
    
    Essa é função para deletar um item da tabela.
    
    ```python
    def delete_item(request):
        todo_id  = request.GET.get('todo_id') # Id da Lista
        todo = TodoList.objects.get(id=todo_id) # Pega Objeto
        todo.delete() # Deleta
        data = {'status':'delete'}
        return JsonResponse(data)
    ```