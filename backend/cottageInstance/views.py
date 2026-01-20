from rest_framework.decorators import api_view, authentication_classes, permission_classes, action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from stripeApp.views import make_stripe_checkout_session
from rest_framework.response import Response
from rest_framework import status

#Models
from .models import CottageInstanceModel
from accounts.models import CustomUser

from .serializers import CottageSerializer, inviteMembers, cottageSubscriptionSerializer

from django.conf import settings
from django.core.mail import send_mail



from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db.models import Q

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def createCottageSubscription(request):
    serializer = cottageSubscriptionSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save(owner=request.user)
        payment_link = make_stripe_checkout_session(serializer.data['stripe_subscription'], request.user.email)
        return Response({
            'results' : {'payment_link': payment_link}
        }, status=status.HTTP_200_OK)
    
    return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def me(request):
    try:
        if request.user.access_to_cottage:
            cottage = request.user.access_to_cottage
        else:
            return Response({'error': 'Cottage not found for user'}, status=status.HTTP_404_NOT_FOUND)

        print(cottage, request.user)
    except CottageInstanceModel.DoesNotExist:
        return Response({'error': 'Cottage not found for user'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CottageSerializer(cottage)
        return Response({'status': 'success', 'results': serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = CottageSerializer(cottage, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save() 
            return Response({'status': 'success', 'results': serializer.data}, status=status.HTTP_200_OK)
        return Response({'status': 'error', 'errors': serializer.errors}, status=status.HTTP_200_OK)




@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def sendInvitation(request):
    try:
        cottage = CottageInstanceModel.objects.filter(
            owner=request.user,
            id=request.user.access_to_cottage.id
        ).first()

    except CottageInstanceModel.DoesNotExist:
        return Response({'error': 'Cottage not found for user'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        serializer = inviteMembers(data=request.data)
        if serializer.is_valid():
            accountsPerCottagePlan = {
                'Basic' : 1,
                'Standard' : 3,
                'Premium': 200
            }
            
            userCounts = cottage.CottageUsers.count() + 2# +2  one is the owner which also a user and the second is the new user
            if userCounts > accountsPerCottagePlan[cottage.stripe_subscription]:
                return Response({'status': 'failed', 'message': 'Cottage user limit reached. Please contact support to upgrade your plan.'}, status=status.HTTP_200_OK)

            account = CustomUser.objects.filter(email=serializer.data.get('email')).first()
            if account:
                cottage.CottageUsers.add(account)
                #Send notification to user email that they were invited to cottage
                subject = "You’ve Been Invited to Join a Cottage on CottagePilot!"
                loginUrl = f"{settings.FRONTEND_URL}login/"
                # Render the HTML content with context variables
                html_content = render_to_string('emails/cottage_invite.html', {
                    'user_name': account.username,
                    'cottage_name': cottage.name,
                    'login_url': loginUrl,
                })
                
                # Generate plain-text content by stripping HTML tags
                text_content = strip_tags(html_content)
                
                email = EmailMultiAlternatives(
                    subject=subject,
                    body=text_content,  # fallback to plain text
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[account.email]
                )
                email.attach_alternative(html_content, "text/html")
                email.send()

                return Response({'status': 'success', 'email': serializer.data.get('email')}, status=status.HTTP_200_OK)

            else:
                #Send notification to email to create a Cottapilot user
                subject = "You’ve Been Invited to Join a Cottage on CottagePilot!"
                signupurl = f"{settings.FRONTEND_URL}pricing/"
                # Render the HTML content with context variables
                html_content = render_to_string('emails/invite_to_signup.html', {
                    'cottage_name': cottage.name,
                    'signup_url': signupurl,
                })
                
                # Generate plain-text content by stripping HTML tags
                text_content = strip_tags(html_content)
                
                email = EmailMultiAlternatives(
                    subject=subject,
                    body=text_content,  # fallback to plain text
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[serializer.data.get('email')]
                )
                email.attach_alternative(html_content, "text/html")
                email.send()

                return Response({'status': 'success', 'email': serializer.data.get('email')}, status=status.HTTP_200_OK)
            
        return Response({'status': 'error', 'errors': serializer.errors}, status=status.HTTP_200_OK)
   
    else:    
        return Response({'status': 'error', 'errors': 'Wrong method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)




@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def listOfUserCottages(request):
    if request.method == 'GET':
        try:
            cottages = CottageInstanceModel.objects.filter((Q(CottageUsers=request.user) | Q(owner=request.user)) & Q(stripe_payment_status=True)
            ).distinct()


        except CottageInstanceModel.DoesNotExist:
            return Response({'error': 'Cottage not found for user'}, status=status.HTTP_404_NOT_FOUND)

        
        serializer = CottageSerializer(cottages, many=True)

        return Response({'status': 'success', 'results': serializer.data}, status=status.HTTP_200_OK)
   
    else:    
        return Response({'status': 'error', 'errors': 'Wrong method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def selectCottage(request):
    if request.method == 'POST':
        id = request.data['id']
        try:
            cottage = CottageInstanceModel.objects.get(id = id, stripe_payment_status=True)
            user = request.user
            user.access_to_cottage = cottage
            user.save()

            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        except CottageInstanceModel.DoesNotExist:
            return Response({'error': 'Cottage not found for user'}, status=status.HTTP_404_NOT_FOUND)
   
    else:    
        return Response({'status': 'error', 'errors': 'Wrong method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

