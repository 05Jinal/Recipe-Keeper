from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from vege.models import *
from django.contrib.auth import authenticate,login,logout

# Create your views here.

def receipes(request):
    if request.method=="POST":
        data= request.POST

        receipe_name= data.get('receipe_name')
        receipe_description= data.get('receipe_description')
        receipe_image= request.FILES.get('receipe_image')

        # print(receipe_name)
        # print(receipe_description)
        # print(receipe_image)

#   To save data in the model name

        Receipe.objects.create(
        receipe_name =receipe_name,
        receipe_description= receipe_description,
        receipe_image=receipe_image,

        )
        return redirect('/receipes/')
    
    queryset= Receipe.objects.all()

    if request.GET.get('search'):
    #    print(request.GET.get('search'))
   
       queryset = queryset.filter(receipe_name__icontains=request.GET.get('search'))



    context = {'receipes': queryset}
        
    return render(request, 'receipes/receipes.html',context)

#   To delete with ths help of unique id 

def delete_receipe(request,id):
    queryset= Receipe.objects.get(id=id)
    queryset.delete()
    return redirect('/receipes/')

def update_receipe(request, id):
    queryset = Receipe.objects.get(id=id)

    if request.method == "POST":
        data = request.POST

      
        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_description')
        receipe_image = request.FILES.get('receipe_image')
    
        # Update the fields in the queryset
        queryset.receipe_name = receipe_name
        queryset.receipe_description = receipe_description

        if receipe_image:
            queryset.receipe_image = receipe_image
            
        # Save the updated queryset
        queryset.save()

        return redirect('/receipes/')  # Redirect after successful update

    context = {'receipe': queryset}

    return render(request, 'receipes/update.html', context)



def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the user exists
        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid Username')
            return redirect('/login/')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, 'Invalid password or username.')
            return redirect('/login/') 
        else:
            login(request, user)  # Log the user in
            return redirect('/receipes/')  # Redirect to recipes page

    return render(request, 'receipes/login.html')  # Render the login page for GET requests


def logout_page(request):
     
     logout(request)
     return redirect('/login')   # Redirect to recipes page


def register_page(request):
    

    if request.method=="POST" :
        first_name= request.POST.get('first_name')
        last_name= request.POST.get('last_name')
        username= request.POST.get('username')
        password= request.POST.get('password')

        user= User.objects.filter(username = username)

        if user.exists():
            messages.info(request,'Username already taken')
            return redirect ('/register/')


        user= User.objects.create(
            first_name= first_name,
            last_name= last_name,
            username= username
        )
        
        user.set_password(password)
        user.save()

        messages.success(request, 'Account Created Successfully')  # Correct use of messages
        return redirect('/register/')

            
        

    return render(request,'receipes/register.html')