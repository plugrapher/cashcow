from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.core.mail import EmailMessage ,EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from .models import Post,Wallet,Transaction
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate, logout, login
from django.db.models import Q # new
from .forms import  ProfileForm, UserForm,PostForm
from django.template.loader import render_to_string
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from decimal import Decimal
from django.core.paginator import Paginator

@login_required
def viewcard(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    purchased_posts = Transaction.objects.filter(user=request.user, transaction_type='withdrawal')

    context = {
        'post': post,
        'purchased_posts': purchased_posts,
    }
    return render(request, "users/viewcard.html", context)


def home(request):
    post = Post.objects.all()
    context = {
        'post': post,
    }
    return render(request, 'users/home.html', context)


def about(request):
    return render(request, 'users/about.html')



@csrf_protect
@login_required(login_url="home")
def createPost(request):
	form = PostForm()

	if request.method == 'POST':
		form = PostForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
		return redirect('job-list')
	context = {'form':form}
	return render(request, 'users/post_form.html', context)



    
##############   QR CODE   #############
import qrcode
from io import BytesIO

@login_required
def category(request):
    # Generate Bitcoin address (this is just a placeholder)
    bitcoin_address = "3EJ7ETzxeU4r7zviNUT6LxwkgLLiMQEvJq"

    # Generate QR code for the Bitcoin address
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(bitcoin_address)
    qr.make(fit=True)

    # Create a BytesIO object to store the QR code image
    qr_code_image = BytesIO()
    qr.make_image().save(qr_code_image, format='PNG')
    qr_code_image.seek(0)

    context = {
        'bitcoin_address': bitcoin_address,
        'qr_code_image': qr_code_image,
    }
    return render(request, 'users/category.html', context)

def navbar(request):
    post = Post.objects.filter(user=request.user).first()  # Adjust as needed
    context = {
        'post': post,
    }
    return render(request, 'users/navbar.html', context)




import requests
from .models import Wallet

@login_required
def profile(request):
    # Get user's wallet balance
    user_wallet = Wallet.objects.get(user=request.user)
    posts = Post.objects.all()

    # Fetch current BTC to USD exchange rate from the API
    btc_to_usd = None
    wallet_balance_btc = None

    try:
        api_url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd'
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            btc_to_usd = data.get('bitcoin', {}).get('usd')

            # Convert wallet balance to BTC if exchange rate is available
            if btc_to_usd:
                wallet_balance_btc = user_wallet.balance / btc_to_usd
    except Exception as e:
        # Handle API request errors gracefully
        print(f"Error fetching BTC to USD exchange rate: {e}")

    context = {
        'balance': user_wallet.balance,
        'btc_to_usd': btc_to_usd,
        'wallet_balance_btc': wallet_balance_btc,
        'post': post,

    }
    return render(request, 'users/profile.html', context)




@login_required
def logout(request):

    messages.success(request, "Logged Out Successfully!!")

    return redirect('/')

########################################################################
########### register here #####################################

def registration(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST) or None
        if form.is_valid():
            username = request.POST.get('username')
            #########################mail####################################
            htmly = get_template('users/email.html')
            d = { 'username': username }
            subject, from_email, to = 'hello', 'from@example.com', 'to@emaple.com'
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            try:
                msg.send()
            except:
                print("error in sending mail")
            ##################################################################
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/registration.html', {'form': form})

###################################################################################
################login forms###################################################
from rest_framework.authtoken.models import Token

@csrf_protect
def Login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        token_key = request.POST.get('token')
        
        if not token_key:
            messages.error(request, "Token is required.")
        elif form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                try:
                    token = Token.objects.get(key=token_key, user=user)
                    login(request, user)
                    messages.info(request, f"You are now logged in as {username}.")
                    return redirect('/')
                except Token.DoesNotExist:
                    messages.error(request, "Invalid token.")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, f"cashout {username}")
    
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})




@login_required(login_url="home")
def updateProfile(request):
    user =request.user
    profile = request.user
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Assuming 'profile' is the URL name for viewing the profile
    return render(request, 'users/profile_update.html', {'form': form})



def sendEmail(request):
	if request.method == 'POST':
		template = render_to_string('users/email_template.html', {
			'name':request.POST['name'],
			'email':request.POST['email'],
			'message':request.POST['message'],
			})
		email = EmailMessage(
			request.POST['subject'],
			template,
			settings.EMAIL_HOST_USER,
			['plugrapher@gmail.com']
			)
		email.fail_silently=False
		email.send()
	return render(request, 'users/email_sent.html')

@login_required
def post(request):
	post = Post.objects.get()

	if request.method == 'POST':

		return redirect('job-list')


	context = {'post':post}
	return render(request, 'users/post.html',context)


@login_required(login_url="home")
def updatePost(request):
	post = Post.objects.get()
	form = PostForm(instance=post)

	if request.method == 'POST':
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			form.save()
		return redirect('job-detail')
	context = {'form':form}
	return render(request, 'users/post_form.html', context)

@login_required(login_url="home")
def deletePost(request, post_id):
    post = Post.objects.get(pk=post_id)  # Retrieve the post object

    if request.method == 'POST':
        post.delete()
        return redirect('job-list')
    context = {'post':post}
    return render(request, 'users/delete.html', context)



from decimal import Decimal


@login_required
def testimonial(request):
    context = {}
    if request.method == 'POST':
        bitcoin_amount = request.POST.get('bitcoin_amount')
        try:
            amount = Decimal(bitcoin_amount)
        except Decimal.InvalidOperation:
            messages.error(request, 'Invalid amount. Please enter a valid number.')
            return redirect('testimonial')  # Adjust this redirect to your correct URL
        
        try:
            # Get or create wallet instance for the user
            wallet, created = Wallet.objects.get_or_create(user=request.user)
        except Wallet.DoesNotExist:
            messages.error(request, 'Wallet does not exist for this user.')
            return redirect('testimonial')  # Adjust this redirect to your correct URL

        # Create a pending or processing transaction
        Transaction.objects.create(user=request.user, amount=amount, transaction_type='deposit', status='pending')
        
        messages.success(request, 'Deposit request submitted. Please wait for confirmation.')
        return redirect('balance')  # Adjust this redirect to your correct URL

    return render(request, 'users/testimonial.html', context)

@login_required
def balance(request):
    # Bitcoin address for QR code generation
    bitcoin_address = "3EJ7ETzxeU4r7zviNUT6LxwkgLLiMQEvJq"
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(bitcoin_address)
    qr.make(fit=True)
    
    # Create a BytesIO object to store the QR code image
    qr_code_image = BytesIO()
    qr.make_image().save(qr_code_image, format='PNG')
    qr_code_image.seek(0)
    
    # Initialize the context with QR code details
    context = {
        'bitcoin_address': bitcoin_address,
        'qr_code_image': qr_code_image,
    }

    try:
        # Get the user's wallet
        wallet = Wallet.objects.get(user=request.user)
        # Get transactions related to the user
        transactions = Transaction.objects.filter(user=request.user).order_by('-timestamp')
        
        # Update the context with wallet and transaction details
        context.update({
            'balance': wallet.balance,
            'transactions': transactions,
        })

        # Add 'post' to context if it's necessary (Ensure 'post' is defined)
        post_id = request.GET.get('post_id')  # Example way to get a post_id, adjust accordingly
        if post_id:
            post = Post.objects.get(id=post_id)
            context['post'] = post

        return render(request, 'users/balance.html', context)
    except Wallet.DoesNotExist:
        # Handle the case where the wallet doesn't exist for the user
        messages.error(request, 'Wallet does not exist!')
        return redirect('testimonial')
    except Exception as e:
        messages.error(request, f'An error occurred: {e}')
        return render(request, 'users/balance.html', context)





@login_required
def job_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    purchased_posts = Transaction.objects.filter(user=request.user, transaction_type='withdrawal')
    post_id = request.GET.get('post_id')  # Example way to get a post_id, adjust accordingly
    if post_id:
        post = Post.objects.get(id=post_id)
    context = {
        'purchased_posts': purchased_posts,
        'post': post,
    }

    return render(request, "users/job-detail.html", context)




@login_required
def contact(request, post_id):
    post = Post.objects.get(id=post_id)
    purchased_posts = Transaction.objects.filter(user=request.user, transaction_type='withdrawal')

    context = {
        'purchased_posts': purchased_posts,
        'post': post,
    }


    return render(request, 'users/contact.html', context)




@login_required
def job_list(request):
    queryset = Post.objects.all()  # Get all posts
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(cardnumber__icontains=query) |
            Q(location__icontains=query) |
            Q(bank__icontains=query) |
            Q(price__icontains=query)
        )
    paginator = Paginator(queryset, 10)  # Show 10 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    user_wallet = Wallet.objects.get(user=request.user)
    purchased_posts = Transaction.objects.filter(user=request.user, transaction_type='withdrawal')
    context = {
        'page_obj': page_obj,
        'post': post,
        'queryset': queryset,
        'purchased_posts': purchased_posts,
    }
    return render(request, "users/job-list.html", context)
    

@login_required
def buy_card(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    amount_decimal = Decimal(str(post.price))  # Convert to Decimal object
    try:
        wallet = Wallet.objects.get(user=request.user)
        wallet_balance = Decimal(str(wallet.balance))  # Convert to Decimal object
    except Wallet.DoesNotExist:
        messages.error(request, 'You need to have a wallet to buy a card.')
        return redirect('balance')

    if wallet_balance >= amount_decimal:
        wallet.balance -= amount_decimal
        wallet.save()
        Transaction.objects.create(
            user=request.user,
            post=post,  # Reference the post in the transaction
            amount=amount_decimal,
            transaction_type='withdrawal'
        )
        messages.success(request, f'You successfully bought the {post.cardnumber}.')
        return redirect('job-detail', post_id=post.id)
    else:
        messages.error(request, 'Insufficient balance to buy this card.')
        return redirect('balance')


