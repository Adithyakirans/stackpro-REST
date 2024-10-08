from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import UserSerializer,QuestionSerializer,AnswerSerializer
from .models import Questions,Answers
from rest_framework import authentication,permissions
from rest_framework.decorators import action
from rest_framework import serializers



# create user creation view using viewsets

class Userview(viewsets.ViewSet):
    def create(self,request,*args,**kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        

# Creating view for questions
class QuestionView(viewsets.ModelViewSet):
    serializer_class =QuestionSerializer
    queryset = Questions.objects.all()

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    # since we didnt pass user id we need to override create method
    def create(self, request, *args, **kwargs):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
    #     # function to list out question excluding current user's(overriding list funtion)
    # def list(self, request, *args, **kwargs):
    #     queryset = Questions.objects.all().exclude(user=request.user)
    #     serializer = QuestionSerializer(queryset,many=True)
    #     return Response(data=serializer.data)
    
    # OR override built in get_queryset function
    def get_queryset(self):
        return Questions.objects.all().exclude(user=self.request.user)
    
    @action(methods=['POST'],detail=True)
    def add_answer(self,request,*args,**kwargs):
        # get object we want to add answer to
        object = self.get_object()
        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user,question=object)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
# create view for answers
        
class AnswerView(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    queryset = Answers.objects.all()

    # we can override both create and listing method because we've already added it inside questions

    def create(self,request,*args,**kwargs):
        raise serializers.ValidationError('method not found')
    
    def list(self,request,*args,**kwargs):
        raise serializers.ValidationError('method not found')
    
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    # override destroy method so only author can delete their answer
    def destroy(self, request, *args, **kwargs):
        # get data of current user
        object = self.get_object()
        if request.user == object.user:
            object.delete()
            return Response(data='deleted')
        else:
            raise serializers.ValidationError('permission denied')
        
    # creating custom method for adding upvotes
    @action(methods=['POST'],detail=True)
    def add_upvote(self,request,*args,**kwargs):
        # get object we want to add upvote to
        answer = self.get_object()
        user = request.user
        # get which user upvoted for which answer
        answer.upvote.add(user)
        return Response(data='upvote added')



        



