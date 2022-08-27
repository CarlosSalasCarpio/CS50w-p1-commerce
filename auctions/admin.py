from django.contrib import admin
from .models import User, auctionListingModel, commentsModel, bidsModel, User

# Register your models here.
admin.site.register(auctionListingModel)
admin.site.register(commentsModel)
admin.site.register(bidsModel)
admin.site.register(User)