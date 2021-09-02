from rest_framework import serializers

from main.models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:  # чтобы вытягивать данные или поляя
        model = Category  # из какой моделки надо  вытягивать данные или поляя
        fields = '__all__'  # какие поля надо вытягивать


class PostSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only=True)  # переопределяем поле
                                            # в каком формате передать дату : день, месяц, год час, минуты, секунды

    class Meta:
        model = Post
        fields = ('id', 'title', 'category', 'created_at', 'text')

    def to_representation(self, instance):  # создаем дополнительное поле ,преопределяем метод  <--
        representation = super().to_representation(instance)  # super для того чтобы от родителя переопределить метод,
                                                    # intance -объект поста
        representation['author'] = instance.author.email
        representation['images'] = PostImageSerializer(instance.images.all(),
                                                       many=True, context=self.context).data   # здесь хранятся отформатированные данные
                            # many=True может быть много катинков
        representation['comments'] = PostImageSerializer(instance.comments.all(),
                                                         many=True, context=self.context).data
        representation['ratings'] = PostImageSerializer(instance.ratings.all(),
                                                        many=True, context=self.context).data
        representation['likes'] = PostImageSerializer(instance.likes.all(),
                                                      many=True, context=self.context).data
        return representation

    def create(self, validated_data):
        request = self.context.get('request')
        user_id = request.user.id
        validated_data['author_id'] = user_id
        post = Post.objects.create(**validated_data)
        return post


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'

    def _get_image_url(self, obj, ):
        if obj.image:  # image из модельки PostImage
            url = obj.image.url
            request = self.context.get('request')
            if request is not None:
                url = request.build_absolute_uri(url)
            else:
                url = ''
            return url

        def to_representation(self, instance):
            representation = super().to_representation(
                instance)  # super для того чтобы от родителя наследо+вать метод
            representation['images'] = self._get_image_url(instance)
            return representation


class RatingSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Rating
        fields = ('id', 'author', 'post', 'grade')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        action = self.context.get('action')

        if action == 'list':
            representation['post'] = instance.post.title

        elif action == 'retrieve':
            representation['post'] = PostSerializer(instance.post).data

        return representation

    def create(self, validated_data):
        request = self.context.get('request')

        if Rating.objects.filter(post=validated_data.get('post'), author=validated_data.get('author')):
            raise serializers.ValidationError('Данный пользователь уже рейтнул этот пост.')

        rating = Rating.objects.create(
            **validated_data
        )

        return rating


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')
    created_date = serializers.DateTimeField(format='%d.%m.%Y %H:%M:%S', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'post', 'comment', 'author', 'created_date')

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        action = self.context.get('action')
        print(action)
        if action == 'list':
            representation['post'] = instance.post.title
            representation['comment'] = instance.comment[:30] + '...' if len(
                instance.comment) >= 30 else instance.comment

        elif action == 'retrieve':
            representation['post'] = PostSerializer(instance.post).data

        return representation


class LikeSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Like
        fields = ('id', 'post', 'author', 'status')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        action = self.context.get('action')
        print(action)
        if action == 'list':
            representation['post'] = instance.post.title

        elif action == 'retrieve':
            representation['post'] = PostSerializer(instance.post).data

        return representation

    def create(self, validated_data):
        request = self.context.get('request')

        if Like.objects.filter(post=validated_data.get('post'), author=validated_data.get('author')):
            raise serializers.ValidationError('Данный пользователь уже лайкнул этот пост.')

        like = Like.objects.create(
            **validated_data
        )

        return like


class FavoritesSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Favorites
        fields = ('id', 'name', 'post', 'author')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        action = self.context.get('action')

        if action == 'list':
            representation['post'] = instance.post.title

        elif action == 'retrieve':
            representation['post'] = PostSerializer(instance.post).data

        return representation

    def create(self, validated_data):
        request = self.context.get('request')

        if Favorites.objects.filter(post=validated_data.get('post'), author=validated_data.get('author')):
            raise serializers.ValidationError('Этот пост был добавлен в избранное.')

        favorites = Favorites.objects.create(
            **validated_data
        )

        return favorites
