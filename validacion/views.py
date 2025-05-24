from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Amortizacion, Persona
from rest_framework import status
from .models import (
    Persona, Solicitud, Laboral, Domicilio, Conyuge,
    GastosMensuales, ReferenciaPersonal
)
from .serializers import (
    PersonaSerializer, SolicitudSerializer, LaboralSerializer,
    DomicilioSerializer, ConyugeSerializer, GastosMensualesSerializer,
    ReferenciaPersonalSerializer
)

from .serializers import AmortizacionSerializer

class TablaAmortizacionCalculada(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, persona_id):
        try:
            persona = Persona.objects.get(pk=persona_id)
        except Persona.DoesNotExist:
            return Response({"detail": "Persona no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        # Obtener solicitud activa o la que quieras calcular (ajusta según tu lógica)
        solicitud = Solicitud.objects.filter(IdPersona=persona).first()
        if not solicitud:
            return Response({"detail": "No se encontró solicitud para esta persona"}, status=status.HTTP_404_NOT_FOUND)

        P = float(solicitud.MontoSolicitado)
        n = solicitud.PlazoFinanciero  # meses

        # Obtenemos tasa anual desde query params o asumimos 12%
        tasa_anual = float(request.query_params.get("tasa_anual", 12))
        r = tasa_anual / 100 / 12  # tasa mensual decimal

        # Calcular cuota fija mensual
        if r > 0:
            cuota = P * (r * (1 + r) ** n) / ((1 + r) ** n - 1)
        else:  # tasa 0%
            cuota = P / n

        cuota = round(cuota, 2)

        tabla = []
        saldo = P

        for mes in range(1, n + 1):
            interes = round(saldo * r, 2)
            capital = round(cuota - interes, 2)
            saldo = round(saldo - capital, 2)
            if saldo < 0:
                saldo = 0.0

            tabla.append({
                "Mes": mes,
                "Cuota": cuota,
                "Capital": capital,
                "Interes": interes,
                "CapitalVivo": saldo,
            })

        return Response({
            "Persona": f"{persona.Nombres} {persona.Apellidos}",
            "MontoSolicitado": P,
            "PlazoMeses": n,
            "TasaAnual": tasa_anual,
            "TablaAmortizacion": tabla,
        })

class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer

class SolicitudViewSet(viewsets.ModelViewSet):
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer

class LaboralViewSet(viewsets.ModelViewSet):
    queryset = Laboral.objects.all()
    serializer_class = LaboralSerializer

class DomicilioViewSet(viewsets.ModelViewSet):
    queryset = Domicilio.objects.all()
    serializer_class = DomicilioSerializer

class ConyugeViewSet(viewsets.ModelViewSet):
    queryset = Conyuge.objects.all()
    serializer_class = ConyugeSerializer

class GastosMensualesViewSet(viewsets.ModelViewSet):
    queryset = GastosMensuales.objects.all()
    serializer_class = GastosMensualesSerializer

class ReferenciaPersonalViewSet(viewsets.ModelViewSet):
    queryset = ReferenciaPersonal.objects.all()
    serializer_class = ReferenciaPersonalSerializer
