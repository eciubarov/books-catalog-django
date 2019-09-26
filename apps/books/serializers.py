from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Book, Review, Author, Category, Cover


class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Review
        fields = ('id', 'text', 'date', 'book', 'username')


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ('id', 'first_name', 'last_name')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name')


class CoverSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cover
        fields = ('id', 'file', 'thumbnail')


class BookListSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    # authors = AuthorSerializer(many=True)
    # categories = CategorySerializer(many=True)

    class Meta:
        model = Book
        fields = ('id', 'title', 'description', 'authors', 'categories', 'cover', 'link')


class BookCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ('id', 'title', 'description', 'authors', 'categories', 'cover')

    def create(self, validated_data):
        authors = validated_data.pop('authors')
        categories = validated_data.pop('categories')
        instance = Book.objects.create(**validated_data)

        for author in authors:
            instance.authors.add(author)

        for category in categories:
            instance.categories.add(category)

        return instance
