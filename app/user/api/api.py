from crypt import methods
from turtle import mode
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from app.user.models import User
from app.user.api.serializers import UserSerializer, UserListSerializer, UpdateUserSerializer, PasswordSerializer


# -- DOCUMENTACION DEL CODIGO EN SWAGGER --


class OrganizarMatriz(APIView):
    """
    Endpoint #1 - Desarrollo
    """
    data = [3,5,5,6,8,3,4,4,7,7,1,1,2]


    # SE ORDENA LA DATA
    def data_ordenada(self):
        matriz_sin_clasificar = []
        matriz_sin_clasificar = self.data
        matriz_sin_clasificar_ordenadas = sorted(matriz_sin_clasificar)
        return matriz_sin_clasificar_ordenadas

    # SE ARMA UNA LISTA DE NUMEROS SIN LOS REPETIDOS
    def data_sin_numeros_repetidos(self):
        resultantList = []
        for element in self.data_ordenada():
            if element not in resultantList:
                resultantList.append(element)
        return resultantList

    # SE CONCATENA LA LISTA ORDENADA CON LOS REPETIDOS
    def get(self, request):
        try:
            numbers = self.data_sin_numeros_repetidos()
            dup = [x for i, x in enumerate(self.data) if i != self.data.index(x)]

            clasificado = numbers + dup

            return Response({
                "sin clasificar": self.data,
                "clasificado": clasificado
                }, status=status.HTTP_200_OK)
                
        except Exception as e:
            return Response({'errors' : str(e)}, status = status.HTTP_400_BAD_REQUEST)



class UserViewSet(viewsets.GenericViewSet):
    """
    Endpoint #2 - Desarrollo

    * Todas las funciones fueron probadas en Postman
    """

    model = User
    serializer_class = UserSerializer
    list_serializer_class = UserListSerializer
    queryset = None


    def get_object(self, pk):
        return get_object_or_404(self.serializer_class.Meta.model, pk=pk)


    #CONSULTA
    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects\
                            .filter(is_active=True)\
                            .values('id', 'username', 'name', 'last_name')
        return self.queryset


    # CAMBIO DE CLAVE DEL USUARIO
    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        try:
            user = self.get_object(pk)
            password_serializer = PasswordSerializer(data = request.data)
            if password_serializer.is_valid():
                user.set_password(password_serializer.validated_data['password'])
                user.save()
                return Response({
                    'message' : 'Contraseña actualizada correctamente!'
                })
            return Response({
                'message' : 'Hay errores en la informacion enviada',
                'errors' : password_serializer.errors
            }, status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
                return Response({'errors' : str(e)}, status = status.HTTP_400_BAD_REQUEST)


    # LISTADO DE USUARIOS
    def list(self, request):
        try:
            users = User.objects.all().values('id','username','email','name')
            users_serializer = self.list_serializer_class(users, many = True)
            return Response(users_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'errors' : str(e)}, status = status.HTTP_400_BAD_REQUEST)


    # REGISTRO DE USUARIO
    def create(self, request):
        try:
            user_serializer = self.serializer_class(data = request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response({'message' : 'Usuario creado correctamente!'}, status=status.HTTP_201_CREATED)
            return Response({
                'message' : 'Hay errores en el registro',
                'errors' : user_serializer.errors
            },status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'errors' : str(e)}, status = status.HTTP_400_BAD_REQUEST)


    # VISTA DETALLADA DEL USUARIO
    def retrieve(self, request, pk=None):
        try:
            user = self.get_object(pk)
            user_serializer = self.serializer_class(user)
            return Response(user_serializer.data)
        except Exception as e:
            return Response({'errors' : str(e)}, status = status.HTTP_400_BAD_REQUEST)


    # ACTUALIZACION DEL USUARIO REGISTRADO
    def update(self, request, pk=None):
        try:
            user = self.get_object(pk)
            user_serializer = UpdateUserSerializer(user, data=request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response({
                    'message' : 'Usuario actualizado correctamente!'
                }, status= status.HTTP_200_OK)
            return Response({
                'message' : 'Hay errores en la actualizacion',
                'errors' : user_serializer.errors
            },status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'errors' : str(e)}, status = status.HTTP_400_BAD_REQUEST)


    # EL USUARIO NO SE ELIMINA, SOLO CAMBIA EL ESTADO DE ACTIVO A INACTIVO
    def destroy(self, request, pk=None):
        try:
            user_destroy = self.model.objects.filter(id = pk).update(is_active=False)
            if user_destroy == 1:
                return Response({
                    'message' : 'Usuario Eliminado correctamente!'
                })
            return Response({
                'message' : 'No existe el usuario que desea eliminar!'
            }, status = status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'errors' : str(e)}, status = status.HTTP_400_BAD_REQUEST)