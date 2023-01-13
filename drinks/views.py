from django.http import JsonResponse
from .models import Drink
from .serializers import DrinkSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


# by default functions are handled as GET requests, thus decorator not needed in those cases, otherwise we need the 
# decorator as shown below
@api_view(['GET', 'POST'])
def drink_list(request):
  if request.method == 'GET':
    # get all drinks
    drinks = Drink.objects.all()

    # serialize them
    serializer = DrinkSerializer(drinks, many = True)

    # return json
    return JsonResponse({'drinks': serializer.data})
  
  elif request.method == 'POST':
    # deserialize data
    serializer = DrinkSerializer(data = request.data)

    # check data is valid
    if serializer.is_valid():
      serializer.save()
      return JsonResponse({
        'data': serializer.data,
        'status': status.HTTP_201_CREATED
      })

    # pass to database
  
  else:
    return JsonResponse({
      'error': f'the function you are trying to utilise does not accept {request.method} requests',
      'accepted requests': ['GET', 'POST']
    })


# returns
# {"drinks": [
#     {
#       "id": 1, 
#       "name": "Coca-Cola", 
#       "description": "Simply the best"
#     }, 
#     {
#       "id": 2, 
#       "name": "Mountain Dew", 
#       "description": "Not actually anything to do with mountains"
#     }
#   ]
# }

# PUT == UPDATE
@api_view(['GET', 'PUT', 'DELETE'])
def drink_detail(request, id):

  try:
    drink = Drink.objects.get(pk = id)
  except Drink.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)

  if request.method == 'GET':
    serializer = DrinkSerializer(drink)
    return Response(serializer.data)
  
  elif request.method == 'PUT':
    serializer = DrinkSerializer(drink, data = request.data)

    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

  elif request.method == 'DELETE':
    drink.delete()
    return Response(status = status.HTTP_204_NO_CONTENT)