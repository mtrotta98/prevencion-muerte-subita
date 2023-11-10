from src.core.sedes.sedes import Sede
from src.core.db import db
from src.core.usuarios import get_usuario
from src.core import entidades

from geopy.geocoders import Nominatim


def get_sedes(busqueda):
    """Esta funcion devuelve todas las sedes"""

    with db.session.no_autoflush:
        if busqueda:
            return Sede.query.filter_by(nombre=busqueda).all()
    return Sede.query.all()

def get_sedes_provincia(id):
    """Esta funcion devuelve todas las sedes asociadas a una provincia"""

    with db.session.no_autoflush:
        if id:
            return Sede.query.filter_by(id_provincia=id).all()
    return Sede.query.all()


def get_sede(id):
    """Devuelve una sede buscada por su id"""
    return Sede.query.filter_by(id=id).first()


def agregar_sede(data):
    """Esta funcion da de alta una sede"""

    entidad = entidades.get_entidad(data["id_entidad"])
    data["id_entidad"] = str(entidad.id)
    data["cantidad_DEA"] = 0
    sede = Sede(**data)
    db.session.add(sede)
    db.session.commit()
    return sede

def editar_sede(data):
    """Esta funcion edita los datos de una sede"""

    sede = get_sede(data['id_sede'])
    sede.latitud = data['latitud'],
    sede.longitud = data['longitud'],
    sede.nombre = data['nombre'],
    sede.flujo_personas = data['flujo_personas'],
    sede.superficie = data['superficie'],
    sede.personal_estable = data['personal_estable'],
    sede.pisos = data['pisos'],
    sede.estado = sede.estado,
    sede.cantidad_DEA = data['cantidad_DEA']
    db.session.commit()
    return sede


def sede_a_cardioasistida(id):
    """ Esta funcion cambia el estado de la sede a cardioasistida """
    sede = get_sede(id)
    sede.estado = "espacio cardioasistido"
    db.session.commit()
    return ""

def validar_datos_existentes(nombre):
    """Esta funcion valida que los datos de alta de sede no existan en la base de datos"""

    nombre_existente = Sede.query.filter_by(nombre=nombre).first()
    if nombre_existente is not None:
        return False, "La sede ya esta cargada en el sistema."
    else:
        return True, ""


def validar_nombre_existente(nombre):
    """Esta funcion valida que los datos de edicion de sede no existan en la base de datos"""

    sedes = get_sedes("")
    nombres = []
    for sede in sedes:
        if (sede.nombre == nombre):
            nombres.append(sede)
    if (len(nombres) > 2):
        return False, "La sede ya esta cargada en el sistema."
    else:
        return True, ""
    

def get_sedes_asociadas(id, busqueda):
    """Devuelve las sedes asociadas a una entidad"""

    id_entidad = id
    sedes = get_sedes(busqueda)
    sedes_asociadas = []
    for sede in sedes:
        id_sede = sede.id_entidad
        if id_sede == id_entidad:
            sedes_asociadas.append(sede)
   
    return sedes_asociadas

def get_sedes_por_provincia(id, id_provincia):
    """Devuelve las sedes asociadas a una entidad y provincia"""

    id_entidad = id
    sedes = get_sedes_provincia(id_provincia)
    sedes_provincia = []
    for sede in sedes:
        id_sede = sede.id_entidad
        if id_sede == id_entidad:
            sedes_provincia.append(sede)
    
    return sedes_provincia

def relacionar_representante_sede(id_representante, id_sede):
    """Esta funcion genera la relacione entre un administrador provincial y una sede"""
    sede = get_sede(id_sede)
    admin = get_usuario(id_representante)
    sede.usuarios.append(admin)
    db.session.commit()

def informacion_sede(usuario_solicitudes):
    """Esta funcion devuelve la informacion de las sedes para poder mostrar en las solicitudes de un usuario"""

    if usuario_solicitudes:
        sedes = []
        for solicitud in usuario_solicitudes:
            sedes.append(get_sede(solicitud.id_sede))
        return sedes
    return None

def get_direccion(sede):
    """Esta funcion devuelve la direccion de una sola sede"""

    if sede:
        direccion = []
        geolocator = Nominatim(user_agent="__main__")
        location = geolocator.reverse(f"{sede.latitud}, {sede.longitud}")
        direccion.append(location.raw['address'].get('road'))
        if location.raw['address'].get('house_number'):
                direccion.append(location.raw['address'].get('house_number'))
        else:
                direccion.append("No posee numero")
        return direccion
    return None

def get_direcciones(sedes):
    """Esta funcion devuelve la direccion de una coleccion de sedes"""

    if sedes:
        direcciones = []
        geolocator = Nominatim(user_agent="__main__")
        for sede in sedes:
            direccion = []
            location = geolocator.reverse(f"{sede.latitud}, {sede.longitud}")
            direccion.append(location.raw['address'].get('road'))
            if location.raw['address'].get('house_number'):
                direccion.append(location.raw['address'].get('house_number'))
            else:
                direccion.append("No posee numero")
            direcciones.append(direccion)
        return direcciones
    return None