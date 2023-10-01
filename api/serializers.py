from rest_framework import serializers, status

from .models import Token


class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Token
        fields = '__all__'
        extra_kwargs = {'full_url': {'validators': []}}

    def create(self, validated_data):

        full_url = validated_data['full_url']
        try:
            short_url = validated_data['short_url']
            token, created = Token.objects.get_or_create(
                full_url=full_url, short_url=short_url
            )
        except KeyError:
            token, created = Token.objects.get_or_create(
                full_url=full_url
            )
        if created:
            status_code = status.HTTP_201_CREATED
        else:
            status_code = status.HTTP_200_OK
        return token, status_code
