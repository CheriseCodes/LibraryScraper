from rest_framework import serializers

from books.models import Book

from django.contrib.auth.models import User



class BookSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Book
        fields = ['url', 'id','owner',
                  'title', 'contributors', 'query','branches']
    def create(self, validated_data):
        """
        Create and return a new `Book` instance, given the validated data.
        """
        return Book.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.contributors = validated_data.get('contributors', instance.contributors)
        instance.branches = validated_data.get('branches', instance.branches)
        instance.save()
        return instance

class UserSerializer(serializers.HyperlinkedModelSerializer):
    books = serializers.HyperlinkedRelatedField(many=True, view_name='book-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url','id', 'username', 'books']