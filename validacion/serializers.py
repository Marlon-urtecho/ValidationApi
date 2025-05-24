from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Persona, Solicitud, Laboral, Domicilio, Conyuge,
    GastosMensuales, ReferenciaPersonal, Amortizacion
)

# Serializador para el usuario
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# Serializador para Persona
class PersonaSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)

    class Meta:
        model = Persona
        fields = '__all__'

# Serializador para Solicitud
class SolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitud
        fields = '__all__'

# Serializador para Laboral
class LaboralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laboral
        fields = '__all__'

# Serializador para Domicilio
class DomicilioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domicilio
        fields = '__all__'

# Serializador para Conyuge
class ConyugeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conyuge
        fields = '__all__'

# Serializador para GastosMensuales
class GastosMensualesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GastosMensuales
        fields = '__all__'

# Serializador para ReferenciaPersonal
class ReferenciaPersonalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferenciaPersonal
        fields = '__all__'

# Serializador para Amortizacion
class AmortizacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amortizacion
        fields = '__all__'

class AmortizacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amortizacion
        fields = '__all__'
        read_only_fields = fields