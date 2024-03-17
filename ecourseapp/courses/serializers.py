from rest_framework import serializers
from .models import Category, Course


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class CourseSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(source='image')

    def get_image(self, obj):
        request = self.context['request']
        if request:
            return request.build_absolute_uri('/static/%s' % obj.image.name)
        return obj.image.name

    class Meta:
        model = Course
        fields = ['id', 'name', 'image', 'created_date', 'category_id']
