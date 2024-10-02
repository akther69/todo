from django.shortcuts import render,redirect

from django.views.generic import View

from theapp.forms import RegistrationForm,SignInForm,ToDoForm

from django.contrib.auth import authenticate,login,logout

from theapp.models import ToDo

from django.contrib import messages

from theapp.decorators import signin_required

from django.utils.decorators import method_decorator

# Create your views here.

class SignUpView(View):
    
    def get(self,request,*args, **kwargs):
        
        form_instance=RegistrationForm()
        
        return render(request,"signup.html",{"form":form_instance})
    
    def post(self,request,*args, **kwargs):
        
        form_instance=RegistrationForm(request.POST)
        
        if form_instance.is_valid():
            
            form_instance.save()
            
            messages.success(request,"Account Created Successfully")
            
            return redirect("sign-in")
        
        messages.error(request,"Invalid Input")
        
        return render(request,"signup.html",{"form":form_instance})
    
class SignInView(View):
    
    def get(self,request,*args, **kwargs):
        
        form_instance=SignInForm()
        
        return render(request,"signin.html",{"form":form_instance})
    
    def post(self,request,*args, **kwargs):
        
        form_instance=SignInForm(request.POST)
        
        if form_instance.is_valid():
            
            data=form_instance.cleaned_data
            
            user_obj=authenticate(request,**data)
            
            if user_obj:
                
                login(request,user_obj)
                
                return redirect("todo-incompleted")
        
        messages.error(request,"Incorrect Username or Password")
            
        return render(request,"signin.html",{"form":form_instance})
   
   
@method_decorator(signin_required,name="dispatch") 
class ToDoCreateView(View):
    
    def get(self,request,*args, **kwargs):
        
        form_instance=ToDoForm()
        
        return render(request,"todo_add.html",{"form":form_instance})
    
    def post(self,request,*args, **kwargs):
        
        form_instance=ToDoForm(request.POST)
        
        if form_instance.is_valid():
            
            form_instance.instance.owner=request.user
            
            form_instance.save()
            
            return redirect("todo-incompleted")
        
        return render(request,"todo_add.html",{"form":form_instance})

@method_decorator(signin_required,name="dispatch")
class ToDoListView(View):
    
    def get(self,request,*args, **kwargs):
        
        qs=ToDo.objects.all()
        
        return render(request,"todo_list.html",{"tasks":qs})
    
    
@method_decorator(signin_required,name="dispatch")
class ToDoUpdateView(View):
    
    def get(self,request,*args, **kwargs):
        
        id=kwargs.get("pk")
        
        todo_object=ToDo.objects.get(id=id)
        
        form_instance=ToDoForm(instance=todo_object)
        
        return render(request,"todo_edit.html",{"form":form_instance})
    
    def post(self,request,*args, **kwargs):
        
        id=kwargs.get("pk")
        
        todo_object=ToDo.objects.get(id=id)
        
        form_instance=ToDoForm(request.POST,instance=todo_object)
        
        if form_instance.is_valid():
            
            form_instance.save()
            
            return redirect("todo-incompleted")
        
        return render(request,"todo_edit.html",{"form":form_instance})
    

@method_decorator(signin_required,name="dispatch")    
class ToDoDeleteView(View):
    
    def get(self,request,*args, **kwargs):
        
        id=kwargs.get("pk")
        
        ToDo.objects.get(id=id).delete()
        
        return redirect("todo-incompleted")
    
@method_decorator(signin_required,name="dispatch") 
class ToDoCompletedView(View):
    
    def get(self,request,*args, **kwargs):
        
        qs=ToDo.objects.filter(status=True).all()
        
        return render(request,"todo_completed.html",{"tasks":qs})
    
@method_decorator(signin_required,name="dispatch")    
class ToDoIncompletedView(View):
    
    def get(self,request,*args, **kwargs):
        
        qs=ToDo.objects.filter(status=False).all()
        
        return render(request,"todo_incompleted.html",{"tasks":qs})
    
class TodoCompleteUpdateView(View):
    
    def get(self,request,*args, **kwargs):
        
        id=kwargs.get("pk")
        
        ToDo.objects.filter(id=id).update(status=True)
        
        return redirect("todo-incompleted")
    
class SignOutView(View):
    
    def get(self,request,*args, **kwargs):
        
        logout(request)
        
        messages.success(request,"Logout Successfull")
        
        return redirect("sign-in")

    

