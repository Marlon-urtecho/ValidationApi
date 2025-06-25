from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (AnalizarFlujoDeCajaAPIView, AnalizarSensibilidadAPIView,
                    CalcularIndiceEndeudamiento, CalcularLTVAPIView,
                    ConyugeViewSet, DomicilioViewSet,
                    EvaluarCapacidadPagoAPIView, GastosMensualesViewSet,
                    LaboralViewSet, LogoutView, PersonaDetalleCompletoView,
                    PersonaViewSet, PruebasDeEstresAPIView,
                    ReferenciaPersonalViewSet, RegisterView, SolicitudViewSet,
                    TablaAmortizacionCalculada, UserViewSet)

router = DefaultRouter()
router.register(r'personas', PersonaViewSet)
router.register(r'solicitudes', SolicitudViewSet)
router.register(r'laborales', LaboralViewSet)
router.register(r'domicilios', DomicilioViewSet)
router.register(r'conyuges', ConyugeViewSet)
router.register(r'gastos', GastosMensualesViewSet)
router.register(r'referencias', ReferenciaPersonalViewSet)
router.register(r'usuarios', UserViewSet, basename='usuarios')


urlpatterns = [
    path('', include(router.urls)),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('registro/', RegisterView.as_view(), name='registro'),
    path('personas/<int:persona_id>/detalle-completo/', PersonaDetalleCompletoView.as_view()),
    path('amortizacion/calculada/persona/<int:persona_id>/', TablaAmortizacionCalculada.as_view(), name='amortizacion_calculada'),
    path('evaluar-capacidad-pago/persona/<int:persona_id>/', EvaluarCapacidadPagoAPIView.as_view(), name='evaluar_capacidad_pago'),
    path('analizar-flujo-caja/persona/<int:persona_id>/', AnalizarFlujoDeCajaAPIView.as_view(), name='analizar_flujo_caja'),
    path('cacular-indice-endeudamineto/persona/<int:persona_id>/', CalcularIndiceEndeudamiento.as_view(), name='calcular_indice_endeudamiento'),
    path('api/analizar-sensibilidad/', AnalizarSensibilidadAPIView.as_view(), name='analizar-sensibilidad'),
    path('api/pruebas-estres/', PruebasDeEstresAPIView.as_view(), name='pruebas-estres'),
    path('api/ltv/<int:id_persona>/', CalcularLTVAPIView.as_view(), name='calcular-ltv'),
    
]
