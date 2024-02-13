from django.shortcuts import redirect, render
from farm.models import CustomUser, Login_Details
from .models import DeliveryBoy, DeliveryBoyEdit
from django.core.mail import send_mail
from django.contrib import messages
from .models import DeliveryBoy

def delivery_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        driving_license = request.FILES.get('driving_license')

        # Basic validation
        if password != confirm_password:
            messages.error(request, 'Password and Confirm Password do not match.')
            return redirect('delivery_register')

        # Create a CustomUser instance
        user = CustomUser.objects.create(
            email=email,
            role='DeliveryBoy',  # Assuming 'DeliveryBoy' is a valid role in your system
            mobile=mobile,
        )
        user.set_password(password)
        user.save()

        # Create a DeliveryBoy instance (not approved yet)
        delivery_boy = DeliveryBoy.objects.create(
            user=user,
            name=name,
            email=email,
            mobile=mobile,
            driving_license=driving_license,
            is_approved=False,
        )

        # Create a Login_Details instance
        login_details = Login_Details.objects.create(
            email=email,
            password=password,  # Note: In a real-world scenario, you should hash the password
            role='DeliveryBoy',  # Assuming 'DeliveryBoy' is a valid role in your system
        )

        # Create a DeliveryBoyEdit instance
        delivery_boy_edit = DeliveryBoyEdit.objects.create(
            user=user,
            delivery_boy=delivery_boy,
            driving_license=driving_license,
        )

        # Send registration details to admin via email for approval
        send_approval_email(delivery_boy)

        messages.success(request, 'Registration successful. Wait for admin approval.')

        return redirect('home')  # Redirect to your home page

    return render(request, 'delivery_register.html')

def send_approval_email(delivery_boy):
    subject = 'New Delivery Boy Registration - Approval Required'
    message = f"Name: {delivery_boy.name}\nEmail: {delivery_boy.email}\nMobile: {delivery_boy.mobile}"

    # Replace 'admin@example.com' with your admin's email
    recipient_email = 'athirakp808@gmail.com'
    send_mail(subject, message, 'from@example.com', [recipient_email])


def delivery_dashboard(request):
    if 'email' in request.session:
        response = render(request, 'dash/delivery_dashboard.html')
        response['Cache-Control'] = 'no-store, must-revalidate'
        return response
    else:
        return redirect('home')
