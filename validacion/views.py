from django.db import connection
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Amortizacion, Persona
from rest_framework import status
from .permissions import IsAdminGroup
from .models import (
    Persona, Solicitud, Laboral, Domicilio, Conyuge,
    GastosMensuales, ReferenciaPersonal, User
)
from .serializers import (
    PersonaDetalleCompletoSerializer, PersonaSerializer, RegisterSerializer, SolicitudSerializer, LaboralSerializer,
    DomicilioSerializer, ConyugeSerializer, GastosMensualesSerializer,
    ReferenciaPersonalSerializer, UserSerializer
)

from .serializers import AmortizacionSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()  # Esto invalida el refresh token
            return Response({"detail": "Logout exitoso"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
    permission_classes = [IsAuthenticated, IsAdminGroup]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = RefreshToken.for_user(user)
            data = {
                "user": UserSerializer(user).data,
                "refresh": str(token),
                "access": str(token.access_token),
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PersonaDetalleCompletoView(APIView):
    def get(self, request, persona_id):
        try:
            persona = Persona.objects.get(id=persona_id)
        except Persona.DoesNotExist:
            return Response({'detail': 'Persona no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PersonaDetalleCompletoSerializer(persona)
        return Response(serializer.data)   


class TablaAmortizacionCalculada(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, persona_id):
        try:
            persona = Persona.objects.get(pk=persona_id)
        except Persona.DoesNotExist:
            return Response({"detail": "Persona no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        solicitud = Solicitud.objects.filter(IdPersona=persona).first()
        if not solicitud:
            return Response({"detail": "No se encontró solicitud para esta persona"}, status=status.HTTP_404_NOT_FOUND)

        P = float(solicitud.MontoSolicitado)
        n = solicitud.PlazoFinanciero  # meses

        # Leer tasa desde la base de datos (modelo), convertir a float
        tasa_anual = float(solicitud.TasaInteresAnual)
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

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminGroup]


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

class EvaluarCapacidadPagoAPIView(APIView):
    def get(self, request, persona_id):
        query = "SELECT * FROM EvaluarCapacidadPagoReal(%s);"

        with connection.cursor() as cursor:
            cursor.execute(query, [persona_id])
            row = cursor.fetchone()

        if row:
            (
                persona_id,
                ingreso_total,
                gastos_totales,
                flujo_caja_libre,
                cuota_mensual,
                dscr,
                estado_credito
            ) = row

            return Response({
                "PersonaId": persona_id,
                "IngresosMensualesTotales": float(ingreso_total),
                "GastosMensualesTotales": float(gastos_totales),
                "FlujoCajaLibre": float(flujo_caja_libre),
                "CuotaMensual": float(cuota_mensual),
                "DSCR": float(dscr) if dscr is not None else None,
                "EstadoCredito": estado_credito
            })

        return Response(
            {"detail": "No se encontraron datos para la persona especificada."},
            status=status.HTTP_404_NOT_FOUND
        )
class AnalizarFlujoDeCajaAPIView(APIView):
    def get(self, request, persona_id):
        query = "SELECT * FROM AnalizarFlujoDeCaja(%s);"

        with connection.cursor() as cursor:
            cursor.execute(query, [persona_id])
            row = cursor.fetchone()

        if row:
            (
                persona_id,
                ingreso_mensual,
                gastos_mensuales,
                flujo_caja_libre
            ) = row

            return Response({
                "PersonaId": persona_id,
                "IngresoMensual": float(ingreso_mensual) if ingreso_mensual is not None else None,
                "GastosMensuales": float(gastos_mensuales) if gastos_mensuales is not None else None,
                "FlujoCajaLibre": float(flujo_caja_libre) if flujo_caja_libre is not None else None
            })

        return Response(
            {"detail": "No se encontraron datos para la persona especificada."},
            status=status.HTTP_404_NOT_FOUND
        )
class CalcularIndiceEndeudamiento(APIView):
    def get(self, request, persona_id):
        query = "SELECT * FROM CalcularIndiceEndeudamiento(%s);"

        with connection.cursor() as cursor:
            cursor.execute(query, [persona_id])
            row = cursor.fetchone()

        if row:
            (
                persona_id,
                ingresos_mensuales,
                gastos_mensuales,
                indice_endeudamiento,
                evaluacion_endeudamiento
            ) = row

            # Evaluación del índice de endeudamiento si no viene desde la función
            if indice_endeudamiento is not None:
                if indice_endeudamiento <= 0.20:
                    evaluacion_endeudamiento = "Muy bajo: Buena salud financiera"
                elif indice_endeudamiento <= 0.35:
                    evaluacion_endeudamiento = "Aceptable: Manejo prudente de la deuda"
                elif indice_endeudamiento <= 0.50:
                    evaluacion_endeudamiento = "Alto: Riesgo potencial de sobreendeudamiento"
                else:
                    evaluacion_endeudamiento = "Muy alto: Riesgo significativo de insolvencia"
            else:
                evaluacion_endeudamiento = "Datos insuficientes para evaluar"

            return Response({
                "PersonaId": persona_id,
                "IngresoMensual": float(ingresos_mensuales),
                "GastosMensuales": float(gastos_mensuales),
                "IndiceEndeudamiento": float(indice_endeudamiento) if indice_endeudamiento is not None else None,
                "EvaluacionEndeudamiento": evaluacion_endeudamiento
            })

        return Response({"detail": "No se encontraron datos para la persona especificada."},
                        status=status.HTTP_404_NOT_FOUND)
    
class CalcularLTVAPIView(APIView):
    def get(self, request, id_persona):
        query = """
            SELECT
                MontoPrestamo,
                MontoGarantia,
                LTV,
                Interpretacion
            FROM CalcularLTV(%s);
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [id_persona])
            row = cursor.fetchone()

        if row:
            data = {
                "MontoPrestamo": float(row[0]) if row[0] is not None else None,
                "MontoGarantia": float(row[1]) if row[1] is not None else None,
                "LTV": float(row[2]) if row[2] is not None else None,
                "Interpretacion": row[3],
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "No se encontraron datos para esta persona."},
                status=status.HTTP_404_NOT_FOUND,
            )
class AnalizarSensibilidadAPIView(APIView):
    def post(self, request):
        try:
            id_persona = request.data.get('id_persona')
            variacion_escenario = request.data.get('variacion_escenario')

            if id_persona is None or variacion_escenario is None:
                return Response(
                    {"error": "id_persona y variacion_escenario son requeridos"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM AnalizarSensibilidad(%s, %s)", [id_persona, variacion_escenario])
                columns = [col[0] for col in cursor.description]
                result = cursor.fetchone()

            if result:
                data = dict(zip(columns, result))
                return Response(data)
            else:
                return Response(
                    {"error": "No se encontraron datos para la persona indicada"},
                    status=status.HTTP_404_NOT_FOUND
                )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class PruebasDeEstresAPIView(APIView):
    def post(self, request):
        id_persona = request.data.get('id_persona')
        reduccion_ingresos = request.data.get('reduccion_ingresos')
        incremento_gastos = request.data.get('incremento_gastos')
        incremento_tasa_interes = request.data.get('incremento_tasa_interes')

        if None in (id_persona, reduccion_ingresos, incremento_gastos, incremento_tasa_interes):
            return Response(
                {"error": "Faltan parámetros obligatorios"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM PruebasDeEstres(%s, %s, %s, %s)
                """, [id_persona, reduccion_ingresos, incremento_gastos, incremento_tasa_interes])
                columns = [col[0] for col in cursor.description]
                row = cursor.fetchone()

            if not row:
                return Response(
                    {"error": "No se encontraron resultados para el IdPersona dado"},
                    status=status.HTTP_404_NOT_FOUND
                )

            resultado = dict(zip(columns, row))
            return Response(resultado)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

