from django.shortcuts import render,redirect
from django import forms
from django.views.generic import View
from tasks.models import Todo
from django.contrib import messages
# Create your views here.

class TodoForm(forms.Form):
    task_name = forms.CharField()
  #  user = forms.CharField()

# class TaskForm(forms.ModelForm):
#     class Meta:
#         model=Task
#         field ='Task_name'    



class TodoCreateView(View):
    def get(self,request,*args,**kwargs):
        form = TodoForm()
        return render(request,"todo-add.html",{'form':form})
    def post(self,request,*args,**kwargs):
        form = TodoForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            Todo.objects.create(**form.cleaned_data,user=request.user)
            messages.success(request,"Todo has been created successfully")
            return redirect('todo-list')
        messages.error(request,"Failed to create todo")
        return render(request,"todo-add.html",{"form":form})

class TodoListView(View):
    def get(self,request,*args,**kwargs):
        qs = Todo.objects.filter(status=False,user=request.user).order_by("-date")
        return render(request,"todo-list.html",{"todos":qs}) 

class TodoDetailView(View):
    def get(self,request,*args,**kwargs):
        id = kwargs.get("pk")
        qs = Todo.objects.get(id=id)
        return  render(request,"todo-detail.html",{"todo":qs})

class TodoDeleteView(View):
    def get(self,request,*args,**kwargs):
        id = kwargs.get("pk")
        Todo.objects.get(id=id).delete()
        messages.success(request,"Todo has been deleted successfully")
        return redirect('todo-list')
class TaskEditView(View):
    def get(self,request,*args,**kwargs):
        id = kwargs.get("pk")
        Todo.objects.filter(id=id).update(status=True)
        messages.success(request,"Todo has been updated successfully")
        return redirect("todo-list")
    
class TodosCompletedView(View):
    def get(self,request,*args,**kwargs):
        qs = Todo.objects.filter(status=True)    
        return render(request,"todo-completed.html",{"todos":qs})    

# class IndexView(View):
#     template_name = 'index.html'
#     def get(self,request,*args,**kwargs):
#         return render(request,self.template_name)

# class TaskCreateView(View):
#     model = Task
#     form_class =TaskForm
#     template_name = "task-add.html"

#     def get(self,request,*args,**kwargs):
#         form = self.form_class
#         return render(request,self.template_name,{"form":form})

#     def post(self,request,*args,**kwargs):
#         from=self.form_class(request.POST)
#         if form.is_valid():
#             form.instance.user=request.user
#             form.save()
#             messages.success(request,"todo-add successfully")
#         messages.error(request,"failed to create todo")
#         return render(request,self.template_name,{'form':form})
    
# class TaskListView(View):
#     model = Task
#     template_name = "task-list.html"
#     def get(self,request,*args,**kwargs):
#         qs = Task.objects.flter(user=request.user)
#         return render(request,self.template.name,{'tasks':qs})
    
            

