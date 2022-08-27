from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

#import auctions

from .models import User, auctionListingModel, commentsModel, bidsModel
from .forms import auctionListingForm, commentsForm, bidsForm

# Index shows all the active listings
def index(request):
    # Query listing list informarion
    item_list = auctionListingModel.objects.all
    
    return render(request, "auctions/index.html", {
        'item_list': item_list,
    })


# User login
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


# User logout
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# User register
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


# User can create a new listing
@login_required(login_url='/login')
def create_listing(request):
    if request.method == "GET":
        form = auctionListingForm
        return render(request, "auctions/create_listing.html", {
            'form': form
        })
    if request.method == "POST":
        form = auctionListingForm(request.POST)
        if form.is_valid:
            form.instance.user_id = request.user.id
            form.save()
            return HttpResponseRedirect(reverse("index"))


# User can check listing's information
@login_required(login_url='/login')
def listing_info(request, pk):
    if request.method == "GET":
        form_comments = commentsForm
        form_bids = bidsForm

        # Query listing informarion, if listing doesn't exist redirect to index
        listing = auctionListingModel.objects.filter(pk = pk).first()
        if listing == None:
            return HttpResponseRedirect(reverse('index'))

        # Query current bid price, if there are not queries yet, display the initial price    
        current_bid = bidsModel.objects.filter(auction = pk).first()
        if current_bid == None:
            current_bid = auctionListingModel.objects.get(pk = pk).price
        else:
            current_bid = bidsModel.objects.get(auction = pk).bid
        comments = commentsModel.objects.filter(auction_id = pk)

        # Check if auction is open or close
        if auctionListingModel.objects.get(pk = pk).auction_open == True: 
            return render(request, "auctions/listing_info.html", {
                'listing': listing,
                'form_comments': form_comments,
                'form_bids': form_bids,
                'comments': comments,
                'current_bid': current_bid
            })

        elif request.user.id == bidsModel.objects.filter(auction = pk).first().user_id:
            print('WORKING##############')
            bid_user = bidsModel.objects.filter(auction = pk).first().user_id
            return render(request, "auctions/listing_info.html", {
                'bid_user': bid_user,
                'listing': listing,
                'form_comments': form_comments,
                'form_bids': form_bids,
                'comments': comments,
                'current_bid': current_bid
            })

        else:
            return render(request, "auctions/listing_info.html", {
                'listing': listing,
                'form_comments': form_comments,
                'form_bids': form_bids,
                'comments': comments,
                'current_bid': current_bid
            })


# Add a comment to a listing
@login_required(login_url='/login')
def comments(request, pk):
    if request.method == "POST":
        form_comments = commentsForm(request.POST)
        if form_comments.is_valid:
            form_comments.instance.auction_id = pk
            form_comments.instance.user_id = request.user.id
            form_comments.save()
            return HttpResponseRedirect(reverse("listing_info", args=(pk,)))


# Delete a listing
@login_required(login_url='/login')
def delete_listing(request, pk):
    if request.method == "POST":
        auctionListingModel.objects.get(pk = pk).delete()
        return HttpResponseRedirect(reverse('index'))

# Close an auction
@login_required(login_url='/login')
def close_listing(request, pk):
    if request.method == "POST":
        winner = bidsModel.objects.filter(auction = pk).first().user
        auction = auctionListingModel.objects.get(pk = pk)
        auction.auction_open = False
        auction.winner =winner
        auction.save()

        return HttpResponseRedirect(reverse('index'))

# Bid for a listing
@login_required(login_url='/login')
def bid_listing(request, pk):
    form_bids = bidsForm(request.POST)
    if form_bids.is_valid():

        # If the item has no bids yet
        if not bidsModel.objects.filter(auction = pk).first():         
            if form_bids.cleaned_data['bid'] > auctionListingModel.objects.get(pk = pk).price:
                form_bids.instance.user_id = request.user.id
                form_bids.instance.auction_id = pk
                form_bids.save()

                auction_new_price = auctionListingModel.objects.get(pk = pk)
                auction_new_price.price = form_bids.cleaned_data['bid']
                auction_new_price.save()

                return HttpResponseRedirect(reverse("listing_info", args=(pk,)))
            else:
                return HttpResponse('<h1>Sorry, your bid must be larger than the starting bid</h1>')

        # If the item already has bids        
        if bidsModel.objects.filter(auction = pk).first():
            if form_bids.cleaned_data['bid'] > bidsModel.objects.get(auction = pk).bid:
                bid_new_price = bidsModel.objects.get(auction = pk)
                bid_new_price.bid = form_bids.cleaned_data['bid']
                bid_new_price.user_id = request.user.id
                bid_new_price.save()

                auction_new_price = auctionListingModel.objects.get(pk = pk)
                auction_new_price.price = form_bids.cleaned_data['bid']
                auction_new_price.save()

                return HttpResponseRedirect(reverse("listing_info", args=(pk,)))
            else:
                return HttpResponse('<h1>Sorry, your bid must be larger than the starting bid</h1>')



# Add an item to watchlist
@login_required(login_url='/login')
def watchlist(request):
    if request.method == "GET":
        item_list = auctionListingModel.objects.filter(watchlist = request.user.id)
        return render(request, "auctions/watchlist.html", {
            'item_list': item_list
        })
    if request.method == "POST":
        pk = request.POST.get('item_pk')
        item = auctionListingModel.objects.get(pk = pk)
        item.watchlist.add(request.user.id)
        item_list = auctionListingModel.objects.filter(watchlist = request.user.id)
        return render(request, "auctions/watchlist.html", {
            'item_list': item_list
        })


# Delete item from watchlist
@login_required(login_url='/login')
def delete_watchlist(request, pk):
    if request.method == "POST":
        watchlist = auctionListingModel.objects.get(pk = pk)
        watchlist.watchlist.remove(request.user.id)
        watchlist.save()
        return HttpResponseRedirect(reverse('watchlist'))


# List with all the categories available
@login_required(login_url='/login')
def category_list(request):
    category_list = auctionListingModel.objects.values('category').distinct()
    print(category_list)
    return render(request, "auctions/category_list.html", {
        'category_list': category_list
    })


# Display specific category
@login_required(login_url='/login')
def category(request, category):
    item_list = auctionListingModel.objects.filter(category = category)
    return render(request, "auctions/index.html", {
        'item_list': item_list
    })