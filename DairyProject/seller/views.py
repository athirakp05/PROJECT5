from django.shortcuts import get_object_or_404, redirect, render
from .forms import DeliveryBoyApprovalForm, DeliveryBoyRegistrationForm
from farm.models import CustomUser, Login_Details
from .models import  ApprovalRequest, DeliveryBoyEdit
from django.core.mail import send_mail
from django.contrib import messages
from .models import DeliveryBoy
from django.contrib.auth.decorators import login_required

def delivery_register(request):
    if request.method == 'POST':
        form = DeliveryBoyRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            delivery_boy = form.save(commit=False)
            
            # Ensure that the user is a CustomUser instance
            if isinstance(request.user, CustomUser):
                delivery_boy.user = request.user
                delivery_boy.is_active = False  # Set is_active to False until admin approval
                delivery_boy.save()

                # Create an ApprovalRequest
                approval_request = ApprovalRequest.objects.create(delivery_boy=delivery_boy)

                messages.success(request, 'Your registration is pending approval from the admin.')
                return redirect('delivery_register')
            else:
                messages.error(request, 'Invalid user type.')
    else:
        form = DeliveryBoyRegistrationForm()

    return render(request, 'delivery_register.html', {'form': form})

@login_required
def deliveryboy_approval(request):
    approval_requests = ApprovalRequest.objects.filter(is_approved=False)

    if request.method == 'POST':
        form = DeliveryBoyApprovalForm(request.POST)
        if form.is_valid():
            approval_request_id = form.cleaned_data['approval_request_id']
            is_approved = form.cleaned_data['is_approved']

            approval_request = get_object_or_404(ApprovalRequest, id=approval_request_id)
            delivery_boy = approval_request.delivery_boy

            if is_approved:
                delivery_boy.is_active = True
                delivery_boy.save()

            approval_request.is_approved = is_approved
            approval_request.save()

            messages.success(request, 'Approval status updated successfully.')
            return redirect('deliveryboy_approval')
    else:
        form = DeliveryBoyApprovalForm()

    return render(request, 'admin/deliveryboy_approval.html', {'approval_requests': approval_requests, 'form': form})
def delivery_dashboard(request):
    if 'email' in request.session:
        # Check if the user is a delivery boy and is approved
        if request.user.is_authenticated and request.user.is_deliveryboy and request.user.deliveryboy.is_active:
            response = render(request, 'dash/delivery_dashboard.html')
            response['Cache-Control'] = 'no-store, must-revalidate'
            return response
        else:
            messages.warning(request, 'You need admin approval to access the dashboard.')
            return redirect('home')
    else:
        return redirect('home')

def delivery_boys(request):
    delivery_boys = DeliveryBoy.objects.all()
    return render(request, 'admin/delivery_boys.html', {'delivery_boys': delivery_boys})