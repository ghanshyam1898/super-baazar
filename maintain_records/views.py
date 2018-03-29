from django.contrib.auth import login, authenticate, logout
from django.views.generic import View
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render

from .forms import *
from .models import *
import time


class LoginFormView(View):

    form_class = LoginForm
    template_name = 'mantain_records/signin.html'

    def get(self, request):
        time.sleep(0.5)
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        time.sleep(0.5)
        form = self.form_class(request.POST or None)

        if form.is_valid() or True:
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(username=username, password=password)

        else:
            return HttpResponse("Invalid form.")

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/')

        else:
            return HttpResponse("<h1>Incorrect username or password.</h1>")


def show_stock(request):
    if request.method == "GET":
        processed_item_details = {}
        raw_item_details = ItemDetails.objects.all()

        for item in raw_item_details:
            processed_item_details[item.item_name] = item.current_stock

        return render(request, "mantain_records/show_current_stock.html",
                      {'data': processed_item_details})



def sales(request):
    try:
        full_name = request.user.get_full_name()
    except:
        full_name = ''

    if request.method == "GET":
        if not request.user.is_authenticated():
            return redirect('/signin')

        item_names = []
        item_details = ItemDetails.objects.all()

        for item in item_details:
            item_names.append(item.item_name)

        dealer_details = []
        dealer_details_object = DealersDetails.objects.all()

        temp = ''

        for item in dealer_details_object:
            temp += item.dealer_name
            temp += ' : '
            temp += str(item.dealer_phone_number)

            dealer_details.append(temp)
            temp = ''

        return render(request, "mantain_records/sales_html_template.html",
                      {'full_name': full_name, 'item_names': item_names,
                       'dealer_details' : dealer_details, 'message': ''})

    elif request.method == "POST":
        if request.user.is_authenticated():
            pass
        else:
            return redirect('/signin')

        sales_details = {}
        total_invoice_amount = 0
        message = 'The Sales invoice has been processed successfully.'

        for i in range(1,8):
            current_item_name = "item_" + str(i) + "_name"
            current_item_quantity = "item_" + str(i) + "_quantity"

            if request.POST[current_item_quantity] != '':
                sales_details[request.POST[current_item_name]] = request.POST[current_item_quantity]

        for item_name in sales_details:
            current_item = get_object_or_404(ItemDetails, item_name=item_name)
            current_item.current_stock -= int(sales_details[item_name])
            current_item.save()

            total_invoice_amount += int(sales_details[item_name]) * current_item.default_selling_price

        selected_dealer = request.POST['dealer_details']

        if selected_dealer != '':
            all_dealers = DealersDetails.objects.all()
            dealer = all_dealers.filter(dealer_phone_number=int(selected_dealer.split(" : ")[1]))
            dealer = dealer[0]

            dealer.total_transaction += total_invoice_amount
            message = 'The Sales invoice of ' + dealer.dealer_name + ' has been processed successfully.'

            dealer.save()

        item_names = []
        item_details = ItemDetails.objects.all()

        for item in item_details:
            item_names.append(item.item_name)

        dealer_details = []
        dealer_details_object = DealersDetails.objects.all()

        temp = ''

        for item in dealer_details_object:
            temp += item.dealer_name
            temp += ' : '
            temp += str(item.dealer_phone_number)

            dealer_details.append(temp)
            temp = ''

        return render(request, "mantain_records/sales_html_template.html",
                      {'full_name': full_name, 'item_names': item_names,
                       'dealer_details' : dealer_details, 'message': message})


def purchase(request):

    try:
        full_name = request.user.get_full_name()
    except:
        full_name = ''

    if request.method == "GET":
        if not request.user.is_authenticated():
            return redirect('/signin')

        item_names = []
        item_details = ItemDetails.objects.all()

        for item in item_details:
            item_names.append(item.item_name)

        return render(request, "mantain_records/purchase_html_page.html",
                      {'full_name': full_name, 'item_names': item_names, 'message': ''})

    elif request.method == "POST":
        if request.user.is_authenticated():
            pass
        else:
            return redirect('/signin')

        sales_details = {}
        for i in range(1,8):
            current_item_name = "item_" + str(i) + "_name"
            current_item_quantity = "item_" + str(i) + "_quantity"

            if request.POST[current_item_quantity] != '':
                sales_details[request.POST[current_item_name]] = request.POST[current_item_quantity]

        for item_name in sales_details:
            current_item = get_object_or_404(ItemDetails, item_name=item_name)
            current_item.current_stock += int(sales_details[item_name])
            current_item.save()

        item_names = []
        item_details = ItemDetails.objects.all()

        for item in item_details:
            item_names.append(item.item_name)

        return render(request, "mantain_records/purchase_html_page.html",
                      {'full_name': full_name, 'item_names': item_names,
                       'message': 'The purchase invoice has been processed successfully.'})


def register_new_dealer(request):
    try:
        full_name = request.user.get_full_name()
    except:
        full_name = ''

    if request.method == "GET":
        if not request.user.is_authenticated():
            return redirect('/signin')

        return render(request, "mantain_records/register_new_dealer_html_template.html", {'full_name' : full_name})

    elif request.method == "POST":
        if not request.user.is_authenticated():
            return redirect('/signin')

        form = DealersDetailsForm(request.POST or None)

        if form.is_valid():
            new_dealer = form.save(commit=False)
            new_dealer.dealer_name = form.cleaned_data['dealer_name']
            new_dealer.dealer_phone_number = form.cleaned_data['dealer_phone_number']
            new_dealer.dealer_email = form.cleaned_data['dealer_email']
            new_dealer.dealer_address = form.cleaned_data['dealer_address']

            new_dealer.save()

            message = str(new_dealer.dealer_name) + " has been registered successfully."
            return render(request, "mantain_records/register_new_dealer_html_template.html",
                          {'message': message, 'full_name': full_name})

        else:
            return HttpResponse("<h1>Form Invalid</h1>")


def register_new_item(request):
    try:
        full_name = request.user.get_full_name()
    except:
        full_name = ''

    if request.method == "GET":
        if not request.user.is_authenticated():
            return redirect('/signin')

        return render(request, "mantain_records/new_item_registration_html_template.html",
                      {'message':'', 'full_name': full_name})

    elif request.method == "POST":
        if not request.user.is_authenticated():
            return redirect('/signin')

        form = ItemDetailsForm(request.POST or None)

        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.item_name = form.cleaned_data['item_name']
            new_item.default_cost_price = form.cleaned_data['default_cost_price']
            new_item.default_selling_price = form.cleaned_data['default_selling_price']

            all_saved_items = ItemDetails.objects.all()
            item_already_registered = False
            for item in all_saved_items:
                if item.item_name == new_item.item_name:
                    item_already_registered = True

            if item_already_registered is True:
                message = "Given item is already registered as " + str(new_item.item_name) +". No changes made."
                return render(request, "mantain_records/new_item_registration_html_template.html",
                              {'message': message, 'full_name': full_name})

            else:
                new_item.save()

            message = str(new_item.item_name) + " has been registered successfully."
            return render(request, "mantain_records/new_item_registration_html_template.html",
                          {'message': message, 'full_name': full_name})

        else:
            return HttpResponse("<h1>Form Invalid</h1>")


def declare_the_winner(request):
    dealers_object = DealersDetails.objects.all()
    dealers = []
    temp = []

    for item in dealers_object:
        temp.append(item.dealer_number)
        temp.append(item.total_transaction)
        dealers.append(temp)
        temp = []

    def get_transactional_amount(item):
        return item[1]

    dealers = sorted(dealers, key=get_transactional_amount)

    first_prize_winner_object = get_object_or_404(DealersDetails, dealer_number=dealers[-1][0])
    second_prize_winner_object = get_object_or_404(DealersDetails, dealer_number=dealers[-2][0])
    third_prize_winner_object = get_object_or_404(DealersDetails, dealer_number=dealers[-3][0])

    first_prize_winner_name = first_prize_winner_object.dealer_name
    second_prize_winner_name = second_prize_winner_object.dealer_name
    third_prize_winner_name = third_prize_winner_object.dealer_name

    first_prize_winner_phone_number = first_prize_winner_object.dealer_phone_number
    second_prize_winner_phone_number = second_prize_winner_object.dealer_phone_number
    third_prize_winner_phone_number = third_prize_winner_object.dealer_phone_number

    return render(request, "mantain_records/declare_winners_html_template.html",
              {'first_prize_winner_name': first_prize_winner_name,
               'first_prize_winner_phone_number' : first_prize_winner_phone_number,

               'second_prize_winner_name' : second_prize_winner_name,
               'second_prize_winner_phone_number' : second_prize_winner_phone_number,

               'third_prize_winner_name' : third_prize_winner_name,
               'third_prize_winner_phone_number' : third_prize_winner_phone_number

               })


def logout_user(request):
    time.sleep(0.5)
    logout(request)
    return redirect('/')
