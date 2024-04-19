from django.shortcuts import render,redirect
from .models import Registration, Billing 
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login

def login_user(request):
    if request.method == 'POST':
        telephone = request.POST.get('telephone')
        id_number = request.POST.get('id_number')
        
        # Authenticate the user
        user = authenticate(username=telephone, password=id_number)
        
        if user is not None:
            # User is authenticated, log them in
            auth_login(request, user)
            return redirect('application')  # Redirect to application page after login
        else:
            # Authentication failed
            messages.error(request, 'Invalid telephone number or ID number.')
            return redirect('login_user')  # Redirect back to login page with error message
    return render(request, 'login.html')

# Create your views here.
def register(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        telephone = request.POST.get('telephone')
        borehole_location = request.POST.get('borehole_location')
        id_number = request.POST.get('id_number')
        
        username = telephone
        while User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different telephone number.')
            return redirect('register')
        
        # Create the user account
        user = User.objects.create_user(username=username, password=id_number)
        
        # Create and save the registration object
        registration = Registration.objects.create(user=user, full_name=full_name, address=address, telephone=telephone, borehole_location=borehole_location, id_number=id_number)
        
        registration.user = user
        registration.save()
        
        return redirect('login_user')  # Redirect to success page or render a success message

    return render(request, 'register.html')

def application(request):
    return render(request, 'application.html')

@login_required
def compute_billing(request):
    if request.method == 'POST':
        # Retrieve selected values from the form
        drilling_type = request.POST.get('drilling_type')
        pump_type = request.POST.get('pump_type')
        depth_height_range = request.POST.get('depth_height')
        client_category = request.POST.get('client_category')  # Assuming you have a select input for client category

        # Define fees based on client category
        if client_category == 'Industrial':
            survey_fees = 20000
            authority_fees = 50000
        elif client_category == 'Commercial':
            survey_fees = 15000
            authority_fees = 30000
        elif client_category == 'Domestic':
            survey_fees = 7000
            authority_fees = 10000
        else:
            return HttpResponse("Invalid selection")

        # Calculate fees based on selected options
        if drilling_type == 'symmetricdrilling':
            drilling_cost = 130000
        elif drilling_type == 'coredrilling':
            drilling_cost = 225000
        elif drilling_type == 'geotech':
            drilling_cost = 335000
        else:
            return HttpResponse("Invalid selection for drilling type")

        if pump_type == 'submersible':
            pump_cost = 90000
        elif pump_type == 'solarpump':
            pump_cost = 65000
        elif pump_type == 'handpump':
            pump_cost = 30000
        else:
            return HttpResponse("Invalid selection for pump type")

        if depth_height_range == '1-100':
            depth_cost = 1000
        elif depth_height_range == '101-200':
            depth_cost = 1500
        elif depth_height_range == '201-300':
            depth_cost = 2000
        elif depth_height_range == '300+':
            depth_cost = 2500
        else:
            return HttpResponse("Invalid selection for depth and height range")
    
        
        total_fees = survey_fees + authority_fees
        
        # Predefined data for pipe type, diameter, length, and number of outlets
        pipe_type = 'type1'
        pipe_diameter = 2.5  # inches
        pipe_length = 100  # meters
        num_outlets = 5

        # Predefined prices per unit for different types of pipes
        pipe_prices = {
            'type1': 10,  # Price per unit for type1 pipe
            'type2': 15,  # Price per unit for type2 pipe
            # Add more types as needed
        }
        # Calculate total amount charged on plumbing
        plumbing_cost = pipe_prices.get(pipe_type, 0) * pipe_length * pipe_diameter * num_outlets


        # Predefined prices for each service and the number of clients
        drilling_prices = [130000, 225000, 335000]  # Prices for symmetric, core, and geo-technical drilling
        pump_prices = [90000, 65000, 30000]  # Prices for submersible, solar, and hand pumps
        num_drilling_clients = 100  # Example number of clients for drilling service
        num_pump_clients = 80  # Example number of clients for pump service

        # Calculate total revenue generated by each service
        total_drilling_revenue = sum(drilling_prices) * num_drilling_clients
        total_pump_revenue = sum(pump_prices) * num_pump_clients

        # Calculate total revenue generated by the company from all services
        total_revenue = total_drilling_revenue + total_pump_revenue


        # Generate appropriate reports (if applicable, generate reports here)

        # Return or render the results as needed
        
        total_amount = drilling_cost + pump_cost + depth_cost + total_fees + plumbing_cost
        
        tax_rate = 0.16  # Example tax rate (16%)
        tax_amount = total_amount * tax_rate
        
        total_amount_with_tax = total_amount + tax_amount
        
        user = request.user
        
        billing = Billing.objects.create(
            user=user,
            client_category=client_category,
            drilling_type=drilling_type,
            pump_type=pump_type,
            depth_height=depth_height_range,
            tax_amount=tax_amount,
            total_fees=total_fees,
            plumbing_cost=plumbing_cost,
            total_revenue=total_revenue,
            total_amount=total_amount_with_tax
        )
        billing.save()

        return redirect('generate_report') 
    
    return HttpResponse("This view only accepts POST requests")

# @login_required 
# def generate_report(request):
#     current_user = request.user 
#     user_billings = Billing.objects.filter(user=current_user)

#     # Pass the filtered data to the template
#     return render(request, 'report.html', {'billings': user_billings})

@login_required 
def generate_report(request):
    current_user = request.user 
    user_billings = Billing.objects.filter(user=current_user).values('client_category', 'drilling_type', 'total_amount', 'pump_type', 'depth_height', 'tax_amount', 'plumbing_cost', 'total_amount')

    return render(request, 'report.html', {'billings': user_billings})