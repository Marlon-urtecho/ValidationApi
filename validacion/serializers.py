from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.models import Group

from .models import (Amortizacion, Conyuge, Domicilio, GastosMensuales,
                     Laboral, Persona, ReferenciaPersonal, Solicitud)


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Group.objects.all(),
        required=False 
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups']
    
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

# Serializador para Solicitud
class SolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitud
        fields = '__all__'

# Serializador para Persona
class PersonaSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    solicitudes = SolicitudSerializer(many=True, read_only=True)

    class Meta:
        model = Persona
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

class DatosSimuladosSerializer(serializers.Serializer):
    ingreso_proyectado = serializers.DecimalField(max_digits=18, decimal_places=2)
    pago_cuota_simulado = serializers.DecimalField(max_digits=18, decimal_places=2)
    tasa_interes = serializers.DecimalField(max_digits=5, decimal_places=2)
    variacion_escenario = serializers.DecimalField(max_digits=5, decimal_places=2)

class PersonaDetalleCompletoSerializer(serializers.ModelSerializer):
    solicitudes = SolicitudSerializer(many=True, read_only=True)
    laborales = LaboralSerializer(many=True, read_only=True)
    domicilios = DomicilioSerializer(many=True, read_only=True)
    conyuges = ConyugeSerializer(many=True, read_only=True)
    gastos = GastosMensualesSerializer(many=True, read_only=True)
    referencias = ReferenciaPersonalSerializer(many=True, read_only=True)

    class Meta:
        model = Persona
        fields = [
            'id', 'Nombres', 'Apellidos', 'TipoIdentificacion', 'NumeroIdentificacion',
            'Nacionalidad', 'FechaNacimiento', 'EstadoCivil', 'Sexo',
            'solicitudes', 'laborales', 'domicilios', 'conyuges', 'gastos', 'referencias'
        ]
