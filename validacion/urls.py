from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    EvaluarCapacidadPagoAPIView, PersonaViewSet, SolicitudViewSet, LaboralViewSet, DomicilioViewSet,
    ConyugeViewSet, GastosMensualesViewSet, ReferenciaPersonalViewSet
)
from .views import TablaAmortizacionCalculada

router = DefaultRouter()
router.register(r'personas', PersonaViewSet)
router.register(r'solicitudes', SolicitudViewSet)
router.register(r'laborales', LaboralViewSet)
router.register(r'domicilios', DomicilioViewSet)
router.register(r'conyuges', ConyugeViewSet)
router.register(r'gastos', GastosMensualesViewSet)
router.register(r'referencias', ReferenciaPersonalViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('amortizacion/calculada/persona/<int:persona_id>/', TablaAmortizacionCalculada.as_view(), name='amortizacion_calculada'),
    path('evaluar-capacidad-pago/persona/<int:persona_id>/', EvaluarCapacidadPagoAPIView.as_view(), name='evaluar_capacidad_pago'),
]
