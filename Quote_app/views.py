from django import http
from django.shortcuts import render,redirect,HttpResponse
import bcrypt
from django.contrib import messages
from .models import User,Quote

# Create your views here.
def index(request):
    return render(request, 'register_login.html')

def register(request):
    errors = User.objects.register_validation(request.POST)
    if errors:
        for value in errors.values():
            messages.error(request, value, extra_tags="register")

    else:
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()

        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = pw_hash
        )
        request.session['user_id'] = user.id
        return redirect('/quotes')

    return redirect('/')

def login(request):
    errors = User.objects.login_validation(request.POST)
    if errors: 
        for value in errors.values():
            messages.error(request, value, extra_tags='login')

    else:
        user = User.objects.filter(email = request.POST['email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                return redirect('/quotes')
            else:
                messages.error(request, "Email or Password not match!", extra_tags='login')

        if not user:
            messages.error(request,"This email address not register yet!!! Please go to register!", extra_tags='login')

    return redirect('/')

def login_success(request):
    context ={
        'user' : User.objects.get(id = request.session['user_id'])
    }
    return render(request, 'success.html', context)


def logout(request):
    request.session.flush()
    return redirect('/')

def quotes_dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')

    else: 
        user = User.objects.get(id=request.session['user_id'])
        favor_quotes = Quote.objects.filter(users_who_like = user)
        quotes = Quote.objects.all().exclude(id__in = [quote.id for quote in favor_quotes])

        context = {
            'user': user,
            'quotes' : quotes,
            'favor_quotes': favor_quotes
        }
        return render(request, 'quotes.html', context)


def create_quote(request):
    errors = Quote.objects.quote_validation(request.POST)
    if errors:
        for value in errors.values():
            messages.error(request, value)

    else:
        user = User.objects.get(id = request.session['user_id'])
        quote = Quote.objects.create(
            quoted_by = request.POST['quoted_by'],
            message = request.POST['message'],
            posted_by = user
        )
        request.session['quote_id'] = quote.id
        return redirect('/quotes')
    
    return redirect('/quotes')
        


def favorite_quote(request, quote_id):
    user = User.objects.get(id = request.session['user_id'])
    quote = Quote.objects.get(id = quote_id)
    user.liked_quotes.add(quote)
    return redirect('/quotes')

def unfavorite_quote(request, quote_id):
    user = User.objects.get(id = request.session['user_id'])
    quote = Quote.objects.get(id = quote_id)
    user.liked_quotes.remove(quote)
    return redirect('/quotes')

def delete(request, quote_id):
    delete_quote = Quote.objects.get(id = quote_id)
    delete_quote.delete()
    return redirect('/quotes')


def edit(request, quote_id):   
    quote = Quote.objects.get(id=quote_id)
    context = {
        'quote': quote
    }
    return render(request, 'edit_page.html', context)

def update(request, quote_id):
    errors = Quote.objects.quote_validation(request.POST)
    if errors:
        for value in errors.values():
            messages.error(request, value)
            
    else:
        update_quote = Quote.objects.get(id=quote_id)
        update_quote.quoted_by = request.POST['quoted_by']
        update_quote.message = request.POST['message']
        update_quote.save()

        return redirect('/quotes')

    return redirect(f'/quotes/{quote_id}/edit')

def user_details(request, user_id):
    user = User.objects.get(id= user_id)
    user_quotes = user.quotes_posted.all()
    count = user_quotes.count()
    context= {
        'user': user,
        'user_quotes': user_quotes,
        'count': count
    }
    return render(request, 'user_page.html', context)
    

    

