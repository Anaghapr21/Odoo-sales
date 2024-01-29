from django.shortcuts import render

# Create your views here.
# from rest_framework import generics
# from .models import Customer,Contact
# from .serializers import CustomerSerializer,ContactSerializer



# class CustomerListCreateView(generics.ListCreateAPIView):
#     queryset=Customer.objects.all()
#     serializer_class=CustomerSerializer

# class CustomerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
#     queryset=Customer.objects.all()
#     serializer_class=CustomerSerializer



# class ContactListCreateView(generics.ListCreateAPIView):
#     queryset=Contact.objects.all()
#     serializer_class=ContactSerializer

# class ContactRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
#     queryset=Contact.objects.all()
#     serializer_class=ContactSerializer


from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Customer,Contact
from .serializers import CustomerSerializer,ContactSerializer


# @api_view(['POST'])
# def create_customer(request):
#     serializer=CustomerSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data,status=status.HTTP_201_CREATED)
#     return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
def create_customer(request):
    if request.method == 'POST':
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            # Save customer data
            customer = serializer.save()

            # Extract email and mobile
            email = request.data.get('email')
            mobile = request.data.get('mobile')

            # Save contact data
            contact_data = {'customer_id': customer.id, 'email': email, 'mobile': mobile}
            contact_serializer = ContactSerializer(data=contact_data)
            if contact_serializer.is_valid():
                contact_serializer.save()
                return Response({'message': 'Customer created successfully'}, status=201)
            else:
                customer.delete()  # Delete customer if contact creation fails
                return Response({'error': 'Failed to create contact'}, status=400)
        else:
            return Response(serializer.errors, status=400)
    else:
        return Response({'error': 'Method not allowed'}, status=405)

# @api_view(['GET'])
# def list_customers(request):
#     customers=Customer.objects.all()
#     serializer=CustomerSerializer(customers,many=True)
#     return Response(serializer.data)
@api_view(['GET'])
def list_customers(request):
    customers = Customer.objects.all()
    serialized_customers = []
    for customer in customers:
        customer_data = CustomerSerializer(customer).data
        try:
            contact = Contact.objects.get(customer_id=customer.id)
            contact_data = {
                'email': contact.email,
                'mobile': contact.mobile
            }
            customer_data['contact'] = contact_data
        except Contact.DoesNotExist:
            pass
        serialized_customers.append(customer_data)
    return Response(serialized_customers)


@api_view(['GET'])
def retrieve_customer(request,pk):
    try:
        customer=Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer=CustomerSerializer(customer)
    return Response(serializer.data)

@api_view(['PUT', 'PATCH'])
def update_customer(request, pk):
    try:
        customer = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = CustomerSerializer(customer, data=request.data, partial=True)
    if serializer.is_valid():
        # Handle photo separately
        if 'photo' in request.FILES:
            customer.photo = request.FILES['photo']
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# @api_view(['PUT'])  # Change to PUT method for updating data
# def update_customer(request, pk):  # Include pk parameter to identify which customer to update
#     try:
#         customer = Customer.objects.get(pk=pk)
#     except Customer.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     serializer = CustomerSerializer(customer, data=request.data)  # Pass instance for partial updates
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# from rest_framework.parsers import MultiPartParser

# @api_view(['PUT'])
# @parser_classes([MultiPartParser])
# def update_customer(request, pk):
#     try:
#         customer = Customer.objects.get(pk=pk)
#     except Customer.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     serializer = CustomerSerializer(customer, data=request.data, partial=True)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_contact(request):
    serializer= ContactSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def list_contacts(request):
    contacts=Contact.objects.all()
    serializer=ContactSerializer(contacts,many=True)
    return Response(serializer.data)


@api_view(['GET'])
def retrieve_contact(request,pk):
    try:
        contact=Contact.objects.get(pk=pk)
    except Contact.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer=ContactSerializer(contact)
    return Response(serializer.data)


@api_view(['GET'])
def customer_contact(request, customer_id):
    try:
        contacts = Contact.objects.filter(customer_id=customer_id)
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)
    except Contact.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    

@api_view(['PUT'])
def update_customer_contact(request, customer_id):
    try:
        # Get the existing contact details for the specified customer
        contacts = Contact.objects.filter(customer_id=customer_id)
        
        if not contacts.exists():
            return Response({'error': 'No contact details found for the specified customer'}, status=status.HTTP_404_NOT_FOUND)
        
        # Assuming a customer has only one associated contact, update the first one found
        contact = contacts.first()
        
        # Update the contact details with the data from the request
        serializer = ContactSerializer(contact, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Contact.DoesNotExist:
        return Response({'error': 'No contact details found for the specified customer'}, status=status.HTTP_404_NOT_FOUND)