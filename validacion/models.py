from django.db import models
from django.contrib.auth.models import User


class Persona(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    Nombres = models.CharField(max_length=255)
    Apellidos = models.CharField(max_length=255)
    TipoIdentificacion = models.CharField(max_length=50)
    NumeroIdentificacion = models.CharField(max_length=50, unique=True)
    Nacionalidad = models.CharField(max_length=100)
    FechaNacimiento = models.DateField()
    EstadoCivil = models.CharField(max_length=50)  # Soltero o Casado
    Sexo = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.Nombres} {self.Apellidos}"


class Solicitud(models.Model):
    IdSolicitud = models.AutoField(primary_key=True)
    NumeroSolicitud = models.CharField(max_length=100)
    TipoMoneda = models.CharField(max_length=10)
    MontoSolicitado = models.DecimalField(max_digits=10, decimal_places=2)
    PlazoFinanciero = models.IntegerField()
    PropositoPrestamo = models.CharField(max_length=255)
    TasaInteresAnual = models.DecimalField(max_digits=5, decimal_places=2)
    Estado = models.CharField(max_length=50)
    IdPersona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name="solicitudes")

    def __str__(self):
        return self.NumeroSolicitud

class Laboral(models.Model):
    IdLaboral = models.AutoField(primary_key=True)
    IdPersona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name="laborales")
    TipoEmpleo = models.CharField(max_length=50)  # Contratado o Comerciante
    LugarTrabajo = models.CharField(max_length=255)
    FechaContratacion = models.DateField()
    FechaAlCorriente = models.DateField()
    IngresosMensuales = models.DecimalField(max_digits=10, decimal_places=2)
    MontoGarantia = models.DecimalField(max_digits=10, decimal_places=2)
    MontoDeudas = models.DecimalField(max_digits=10, decimal_places=2)


class Domicilio(models.Model):
    IdDomicilio = models.AutoField(primary_key=True)
    IdPersona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name="domicilios")
    Direccion = models.CharField(max_length=255)
    EstadoDomicilio = models.CharField(max_length=50)  # Propio o Alquilado
    MontoMensualidad = models.DecimalField(max_digits=10, decimal_places=2)
    Departamento = models.CharField(max_length=100)
    Municipio = models.CharField(max_length=100)
    Barrio = models.CharField(max_length=100)


class Conyuge(models.Model):
    IdConyuge = models.AutoField(primary_key=True)
    IdPersona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name="conyuges")
    NombreApellidos = models.CharField(max_length=255)
    NumeroCedula = models.CharField(max_length=50, unique=True)
    NumeroPersonasACargo = models.IntegerField()


class GastosMensuales(models.Model):
    IdGastosMensuales = models.AutoField(primary_key=True)
    IdPersona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name="gastos_mensuales")
    Alimentacion = models.DecimalField(max_digits=10, decimal_places=2)
    VestimentaCalzado = models.DecimalField(max_digits=10, decimal_places=2)
    Transporte = models.DecimalField(max_digits=10, decimal_places=2)
    Colegiatura = models.DecimalField(max_digits=10, decimal_places=2)
    OtrosGastos = models.DecimalField(max_digits=10, decimal_places=2)
    GastosSalud = models.DecimalField(max_digits=10, decimal_places=2)
    Telecomunicaciones = models.DecimalField(max_digits=10, decimal_places=2)
    ServiciosAguaLuz = models.DecimalField(max_digits=10, decimal_places=2)
    ServiciosCableInternet = models.DecimalField(max_digits=10, decimal_places=2)


class ReferenciaPersonal(models.Model):
    IdReferencia = models.AutoField(primary_key=True)
    IdPersona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name="referencias")
    NombreApellido = models.CharField(max_length=255)
    NumeroContacto = models.CharField(max_length=50)


class Amortizacion(models.Model):
    IdAmortizacion = models.AutoField(primary_key=True)
    IdPersona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name="amortizaciones")
    Mes = models.IntegerField()
    Cuota = models.DecimalField(max_digits=10, decimal_places=2)
    Capital = models.DecimalField(max_digits=10, decimal_places=2)
    Interes = models.DecimalField(max_digits=10, decimal_places=2)
    CapitalVivo = models.DecimalField(max_digits=10, decimal_places=2)
