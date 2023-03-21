from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import User, NewListing, UserWatchlist, UserComments, Bid
import datetime


def index(request):
    request.session['message'] = {
                'message': ''
            } 
    try:
        listings = NewListing.objects.all()
        return render(request, "auctions/index.html", {
        'listings': listings
    })
    except:
        listings = []
        return render(request, "auctions/index.html", {
        'listings': listings
    })


def login_view(request):
    
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create_listing(request):
    request.session['message'] = {
                'message': ''
            } 
    if request.method == 'POST':
        now = datetime.datetime.now()
        year = now.year
        month = now.strftime("%b")
        day = now.day
        hour = now.hour
        minute = now.minute
        exact_time = "{}:{}".format(hour, minute)
        time = f'{month} {day}, {year} {exact_time}.'
        title = request.POST['title']
        description = request.POST['descr']
        bid = request.POST['bid']
        image_url = request.POST['image']
        category = request.POST['category']
        if category == '':
            category = 'No Category Listed'
        else:
            category = request.POST['category']
        titles = NewListing.objects.all()
        title_list = [title.title for title in titles]    
        listings = NewListing(title=title, text=description, bid=bid, time=time, image_url=image_url, category=category, status="open")
        listings.user = request.user
        if listings.title in title_list:
            pass
        else:    
            listings.save()
        return HttpResponseRedirect(reverse('index'))
   
    return render(request, 'auctions/create.html')


def listings(request, list_title):
    item = NewListing.objects.filter(title=list_title).first()
    bid = Bid.objects.filter(title=list_title)
    bid_list = [price.price for price in bid]
    message = request.session.get('message', '')
    user = request.user
    comments = UserComments.objects.all()
    status = item.status
    try:
        all_bids = Bid.objects.filter(title=list_title)
        all_bids_titles = [price.price for price in all_bids]
        most_bid = max(all_bids_titles)
        name = Bid.objects.filter(price=most_bid, title=list_title).first()
        username = name.user
        title_name = name.title
    except:
        username = 'None'
        title_name = ''
    
    if request.method == 'POST':
        if 'watchlist' in request.POST:
            new_item = NewListing.objects.filter(title=list_title).first()
            request.session['new_item'] = {
                'id': new_item.id,
                'title': new_item.title,
                'text': new_item.text,
                'bid': new_item.bid,
                'time': new_item.time,
                'image_url': new_item.image_url,
                'category': new_item.category
            }
            return HttpResponseRedirect(reverse('add', args=(request.user, )))

        elif 'comment' in request.POST:
            return HttpResponseRedirect(reverse('comment', args=(item.title, )))
        
        elif 'place_bid' in request.POST:
            request.session['bid'] = {
                'price': request.POST['bid'], 
                'title': list_title
            }
            return HttpResponseRedirect(reverse('bid'))
        elif 'close_bid' in request.POST:
            request.session['item'] = {
                'name': list_title
            } 
            name = Bid.objects.filter(title=list_title).first()
            try:
                username = name.user
                title_name = name.title
            except:
                username = ''
                title_name = ''
            return HttpResponseRedirect(reverse('close'))

    return render(request, 'auctions/listings.html', {
        'item': item, 
        'comments': comments, 
        'num_bids': len(bid_list), 
        'message': message['message'], 
        'title': list_title, 
        'user': user, 
        'status_code': status, 
        'name': username,
        'winner_name_title': title_name
    })


@login_required
def watchlist(request):
    request.session['message'] = {
                'message': ''
            } 
    watchlist = UserWatchlist.objects.filter(user=request.user)
    
    return render(request, 'auctions/watchlist.html', {
        'items': watchlist
    })
       

def categories(request):
    request.session['message'] = {
                'message': ''
            } 
    categories_list = []
    categories = NewListing.objects.all()
    for category in categories:
        if category.category not in categories_list:
            categories_list.append(category.category)
    return render(request, 'auctions/categories.html', {
        'categories_list': categories_list
    })


def listed_category(request, category):
    request.session['message'] = {
                'message': ''
            } 
    items = NewListing.objects.filter(category=category)
    return render(request, 'auctions/listed_cat.html', {
        'category': category, 
        'items': items
    })    


def delete(request, name):
    listing = UserWatchlist.objects.filter(title=name).first()
    listing.delete()
    request.session['new_item'] = None
    return HttpResponseRedirect(reverse('watchlist'))


def comment(request, item_name):
    request.session['message'] = {
                'message': ''
            } 
    if request.method == 'POST':
        comment = request.POST['user_comment']
        user = request.user
        now = datetime.datetime.now()
        year = now.year
        month = now.strftime("%b")
        day = now.day
        hour = now.hour
        minute = now.minute
        exact_time = "{}:{}".format(hour, minute)
        time = f'{month} {day}, {year} {exact_time}.'
        user_comment = UserComments(user=user, title=item_name, comment=comment, time=time)
        user_comment.save()
        return HttpResponseRedirect(reverse('listings', args=(item_name, )))
    return render(request, 'auctions/comment.html', {
        'item_name': item_name
    })



def add(request, user):
    request.session['message'] = {
                'message': ''
            } 
    new_item_data = request.session.get('new_item', None)
    if new_item_data is not None:

        new_item = NewListing.objects.get(id=new_item_data['id'])
        titles = UserWatchlist.objects.all()
        title_list = [title.title for title in titles]
        user_query = UserWatchlist.objects.filter(user=request.user) 
        user_titles = [title.title for title in user_query]
        if new_item.title not in user_titles:
            user_item = UserWatchlist(title=new_item.title, text=new_item.text, bid=new_item.bid, time=new_item.time, image_url=new_item.image_url, category=new_item.category)
            user_item.user = request.user
            user_item.save()
        return HttpResponseRedirect(reverse('watchlist'))
     
    return HttpResponseRedirect(reverse('watchlist'))


def bid(request):
    bid_price = request.session.get('bid', '')
    bid = Bid.objects.filter(title=bid_price['title'])
    bid_prices = [price.price for price in bid]

    if len(bid_prices) == 0:
        if bid_price['price'] != '':
            new_bid = Bid(user=request.user, title=bid_price['title'], price=bid_price['price'])
            new_bid.save()
            request.session['message'] = {
                'message': 'Bid Successfully Sumbitted!.'
            } 
            return HttpResponseRedirect(reverse('listings', args=(bid_price['title'], )))  
        else:
            request.session['message'] = {
                'message': 'Bid Price too Small! Please try again.'
            } 
    else:
        if bid_price['price'] != '' and float(bid_price['price']) > max(bid_prices):
                new_bid = Bid(user=request.user, title=bid_price['title'], price=bid_price['price'])
                new_bid.save()
                request.session['message'] = {
                'message': 'Bid Successfully Submitted!'
            } 
                return HttpResponseRedirect(reverse('listings', args=(bid_price['title'], ))) 
        else:
            request.session['message'] = {
                'message': 'Bid Price too Small! Please try again.'
            } 
            return HttpResponseRedirect(reverse('listings', args=(bid_price['title'], )))
    return HttpResponseRedirect(reverse('listings', args=(bid_price['title'], )))


def close(request):
    data = request.session.get('item', '')
    item = NewListing.objects.filter(title=data['name']).first()
    item.status = 'closed'
    item.save()
    bids = Bid.objects.filter(title=data['name'])
    bid_prices_list = [price.price for price in bids]
    try:
        max_bid = max(bid_prices_list)
        max_query = Bid.objects.get(title=data['name'], price=max_bid)
        max_query.status = 'won'
        max_query.save()
        winner = str(max_query.user)
        item = str(max_query.title)
    except: 
        pass
    return HttpResponseRedirect(reverse('listings', args=(data['name'], )))


