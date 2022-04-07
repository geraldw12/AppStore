from django.shortcuts import render, redirect
from django.db import connection

# # Create your views here.
# def index(request):
#     """Shows the main page"""

#     ## Delete customer
#     if request.POST:
#         if request.POST['action'] == 'delete':
#             with connection.cursor() as cursor:
#                 cursor.execute("DELETE FROM customers WHERE customerid = %s", [request.POST['id']])

#     ## Use raw query to get all objects
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT * FROM customers ORDER BY customerid")
#         customers = cursor.fetchall()

#     result_dict = {'records': customers}

#     return render(request,'app/index.html',result_dict)


# Create your views here.
def view(request, id):
    """Shows the main page"""
    
    ## Use raw query to get a customer
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM customers WHERE customerid = %s", [id])
        customer = cursor.fetchone()
    result_dict = {'cust': customer}

    return render(request,'app/view.html',result_dict)

# Create your views here.
def add(request):
    """Shows the main page"""
    context = {}
    status = ''

    if request.POST:
        ## Check if customerid is already in the table
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM customers WHERE customerid = %s", [request.POST['customerid']])
            customer = cursor.fetchone()
            ## No customer with same id
            if customer == None:
                ##TODO: date validation
                cursor.execute("INSERT INTO customers VALUES (%s, %s, %s, %s, %s, %s, %s)"
                        , [request.POST['first_name'], request.POST['last_name'], request.POST['email'],
                           request.POST['dob'] , request.POST['since'], request.POST['customerid'], request.POST['country'] ])
                return redirect('index')    
            else:
                status = 'Customer with ID %s already exists' % (request.POST['customerid'])


    context['status'] = status
 
    return render(request, "app/add.html", context)

# Create your views here.
def edit(request, id):
    """Shows the main page"""

    # dictionary for initial data with
    # field names as keys
    context ={}

    # fetch the object related to passed id
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM customers WHERE customerid = %s", [id])
        obj = cursor.fetchone()

    status = ''
    # save the data from the form

    if request.POST:
        ##TODO: date validation
        with connection.cursor() as cursor:
            cursor.execute("UPDATE customers SET first_name = %s, last_name = %s, email = %s, dob = %s, since = %s, country = %s WHERE customerid = %s"
                    , [request.POST['first_name'], request.POST['last_name'], request.POST['email'],
                        request.POST['dob'] , request.POST['since'], request.POST['country'], id ])
            status = 'Customer edited successfully!'
            cursor.execute("SELECT * FROM customers WHERE customerid = %s", [id])
            obj = cursor.fetchone()


    context["obj"] = obj
    context["status"] = status
    return render(request, "app/edit.html", context)

def login(request): 
     
    if request.POST: 
        if request.POST['action'] == 'signin': 
            user = request.POST.get('username', False) 
            pw = request.POST.get('pw', False) 
            print(user,pw) 
            curr_user = authenticate(username = user, password = pw) 
            if curr_user is not None: 
                login(request,curr_user) 
            else: 
                return render(request, 'app/login.html', {'not found': True}) 
            return redirect('main_page')     
  
    return render(request, 'app/login.html')

def main_page(request):
    """Shows the main page"""
    return render(request,'app/main_page.html')

def register_job(request): 
    """Shows the register job page""" 
    context = {} 
    status = '' 
 
    if request.POST: 
        ## Check if petid is already in the table 
        with connection.cursor() as cursor: 
 
            cursor.execute("SELECT MAX(CAST(offerid AS DECIMAL)) FROM joboffer") 
            maxofferid = cursor.fetchone() 
 
            cursor.execute("INSERT INTO joboffer VALUES (%s, %s, %s, %s, %s, %s)", [str(maxofferid[0]+1), request.POST['price'], request.POST['location'], request.POST['date_from'], request.POST['date_to'], request.POST['petid']]) 
 
    context['status'] = status 
  
    return render(request, "app/register_job.html", context)

def pending(request):
    """Shows the pending page"""

    ## Use raw query to get all objects
    with connection.cursor() as cursor:

        cursor.execute("SELECT * FROM pending WHERE offerid IN (SELECT offerid FROM joboffer WHERE petid IN (SELECT petid FROM pet WHERE username = 'johnny123')) AND offerid NOT IN (SELECT offerid FROM transaction) ORDER BY offerid") 
        pendingoffers = cursor.fetchall()

    result_dict = {'pendingrecords': pendingoffers}

    return render(request,'app/pending.html',result_dict)

def view_offer(request,offerid):
    """Shows the offer info page"""
    
    ## Use raw query to get a customer
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM joboffer WHERE offerid = %s", [offerid])
        offer = cursor.fetchone()
    result_dict = {'pendingoffers': offer}

    return render(request,'app/view_offer.html',result_dict)

def view_user(request, username): 
    """Shows the user info page""" 
     
    ## Use raw query to get a customer 
    with connection.cursor() as cursor: 
        cursor.execute("SELECT p.username, p.email, p.phonenum, p.year_exp, (SELECT ROUND(AVG(rating),2) FROM to_rate WHERE offerid IN (SELECT offerid FROM transaction WHERE petsitter = %s)) AS avg_rating FROM portfolio p WHERE p.username = %s", [username, username])
        user = cursor.fetchone() 
    result_dict = {'pendingusers': user} 
 
    return render(request,'app/view_user.html',result_dict)

def offer_accepted(request,offerid,petsitter): 
    """Shows the interested page""" 
     
    ## Use raw query to get a customer 
    with connection.cursor() as cursor: 
        cursor.execute("INSERT INTO transaction VALUES (%s,%s)", [offerid, petsitter]) 
 
    return render(request,'app/offer_accepted.html')

def register_user(request):
    """Shows the main page"""
    context = {}
    status = ''

    if request.POST:
        ## Check if username is already in the table
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM portfolio WHERE username = %s", [request.POST['username']])
            user = cursor.fetchone()
            ## No user with same username
            if user == None:
                ##TODO: date validation
                cursor.execute("INSERT INTO portfolio VALUES (%s, %s, %s, %s, %s)"
                        , [request.POST['username'], request.POST['email'], request.POST['phonenum'],
                           request.POST['year_exp'] , request.POST['password'] ])
                return redirect('login')    
            else:
                status = 'User with username %s already exists' % (request.POST['username'])


    context['status'] = status
 
    return render(request, "app/register_user.html", context)

def register_pet(request):
    """Shows the register pet page"""
    context = {}
    status = ''

    if request.POST:
        ## Check if petid is already in the table
        with connection.cursor() as cursor:

            cursor.execute("SELECT MAX(CAST(petid AS DECIMAL)) FROM pet")
            maxpetid = cursor.fetchone()

            cursor.execute("INSERT INTO pet VALUES (%s, %s , %s, %s, %s)", [request.POST['petname'], str(maxpetid[0]+1), request.POST['type'], request.POST['breed'], 'johnny123' ])

    context['status'] = status
 
    return render(request, "app/register_pet.html", context)

def mypets(request):
    """Shows the mypets page"""

    ## Use raw query to get all objects
    with connection.cursor() as cursor:

        cursor.execute("SELECT * FROM pet WHERE username = 'johnny123'")
        animal = cursor.fetchall()

    result_dict = {'pets': animal}

    return render(request,'app/mypets.html',result_dict)

def sit_pet(request):
    """Shows the sit a pet page"""

    with connection.cursor() as cursor:
        cursor.execute("SELECT offerid, petid FROM joboffer WHERE petid NOT IN (SELECT petid FROM pet WHERE username = 'johnny123') AND offerid NOT IN (SELECT offerid FROM transaction)")
        alloffers = cursor.fetchall()

    result_dict = {'total': alloffers}

    return render(request,'app/sit_pet.html', result_dict)

def view_pet(request, petid):
    """Shows the main page"""
    
    ## Use raw query to get a customer
    with connection.cursor() as cursor:
        cursor.execute("SELECT p.petname, p.type, p.breed, j.date_from, j.date_to, j.location, j.price, p.petid FROM pet p, joboffer j WHERE p.petid = %s AND p.petid = j.petid", [petid])
        eachpet = cursor.fetchone()
    result_dict = {'allpet': eachpet}

    return render(request,'app/view_pet.html',result_dict)

def interested(request, offerid): 
    """Shows the interested page""" 
     
    ## Use raw query to get a customer 
    with connection.cursor() as cursor: 
        cursor.execute("INSERT INTO pending VALUES (%s, %s)", [offerid, 'johnny123']) 
 
    return render(request,'app/interested.html')

def history(request):  
    """Shows the history page""" 
 
    ## Use raw query to get all objects 
    with connection.cursor() as cursor: 
        cursor.execute("SELECT j.offerid, j.price, j.location, j.date_from, j.date_to, j.petid, t.petsitter FROM joboffer j, transaction t, pet p WHERE j.offerid NOT IN (SELECT offerid FROM to_rate) AND j.offerid = t.offerid AND p.petid = j.petid AND p.username = 'johnny123'") 
        transactions_nr = cursor.fetchall() 
 
    result_dict = {'history_nr': transactions_nr} 
    print(result_dict)
    ## Use raw query to get all objects 
    with connection.cursor() as cursor: 
        cursor.execute("SELECT j.offerid, j.price, j.location, j.date_from, j.date_to, j.petid, t.petsitter, tr.rating FROM joboffer j, transaction t, pet p, to_rate tr WHERE j.offerid = t.offerid AND j.offerid = tr.offerid AND p.petid = j.petid AND p.username = 'johnny123'") 
        transactions_r = cursor.fetchall() 
 
    result_dict.update({'history_r': transactions_r})
    print(result_dict)
 
    return render(request,'app/history.html',result_dict)

def give_rating(request,offerid): 
    """Shows the give rating page"""
    context = {}
    status = ''

    if request.POST:
        ## Check if petid is already in the table
        with connection.cursor() as cursor: 
            cursor.execute("INSERT INTO to_rate VALUES (%s,%s)", [offerid, request.POST['rating']]) 
 
    context['status'] = status
 
    return render(request, "app/give_rating.html", context)
