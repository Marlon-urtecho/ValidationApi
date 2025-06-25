from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import (Amortizacion, Conyuge, Domicilio, GastosMensuales,
                     Laboral, Persona, ReferenciaPersonal, Solicitud)

@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('Nombres', 'Apellidos', 'NumeroIdentificacion', 'Nacionalidad', 'Sexo', 'EstadoCivil')
    search_fields = ('Nombres', 'Apellidos', 'NumeroIdentificacion')
    list_filter = ('Nacionalidad', 'EstadoCivil', 'Sexo')
    ordering = ('Apellidos', 'Nombres')
    fieldsets = (
        (_("Datos personales"), {
            'fields': ('user', 'Nombres', 'Apellidos', 'TipoIdentificacion', 'NumeroIdentificacion', 'Nacionalidad', 'FechaNacimiento', 'Sexo', 'EstadoCivil')
        }),
    )


@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('NumeroSolicitud', 'TipoMoneda', 'MontoSolicitado', 'PlazoFinanciero', 'Estado', 'IdPersona')
    search_fields = ('NumeroSolicitud',)
    list_filter = ('TipoMoneda', 'Estado')
    ordering = ('-IdSolicitud',)
    raw_id_fields = ('IdPersona',)


@admin.register(Laboral)
class LaboralAdmin(admin.ModelAdmin):
    list_display = ('IdPersona', 'TipoEmpleo', 'LugarTrabajo', 'IngresosMensuales', 'MontoGarantia', 'MontoDeudas')
    list_filter = ('TipoEmpleo',)
    search_fields = ('LugarTrabajo',)
    raw_id_fields = ('IdPersona',)


@admin.register(Domicilio)
class DomicilioAdmin(admin.ModelAdmin):
    list_display = ('IdPersona', 'Direccion', 'EstadoDomicilio', 'MontoMensualidad', 'Departamento', 'Municipio', 'Barrio')
    list_filter = ('EstadoDomicilio', 'Departamento')
    search_fields = ('Direccion', 'Barrio')
    raw_id_fields = ('IdPersona',)


@admin.register(Conyuge)
class ConyugeAdmin(admin.ModelAdmin):
    list_display = ('IdPersona', 'NombreApellidos', 'NumeroCedula', 'NumeroPersonasACargo')
    search_fields = ('NombreApellidos', 'NumeroCedula')
    raw_id_fields = ('IdPersona',)


@admin.register(GastosMensuales)
class GastosMensualesAdmin(admin.ModelAdmin):
    list_display = (
        'IdPersona', 'Alimentacion', 'VestimentaCalzado', 'Transporte',
        'Colegiatura', 'OtrosGastos', 'GastosSalud',
        'Telecomunicaciones', 'ServiciosAguaLuz', 'ServiciosCableInternet'
    )
    raw_id_fields = ('IdPersona',)


@admin.register(ReferenciaPersonal)
class ReferenciaPersonalAdmin(admin.ModelAdmin):
    list_display = ('IdPersona', 'NombreApellido', 'NumeroContacto')
    search_fields = ('NombreApellido', 'NumeroContacto')
    raw_id_fields = ('IdPersona',)


@admin.register(Amortizacion)
class AmortizacionAdmin(admin.ModelAdmin):
    list_display = ('IdPersona', 'Mes', 'Cuota', 'Capital', 'Interes', 'CapitalVivo')
    list_filter = ('Mes',)
    raw_id_fields = ('IdPersona',)
