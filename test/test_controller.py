import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.dataset import Base, Estacion
from controllers.main_controller import MainController


# --- Configuración de base de datos de pruebas PostgreSQL ---
DATABASE_URL = "postgresql://admin:123@localhost/datos_test"

# Crea engine y sesión para pruebas
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)

# --- Fixture para la sesión de prueba ---
@pytest.fixture(scope="function")
def session_prueba():
    Base.metadata.drop_all(bind=engine)     # Limpiar la base
    Base.metadata.create_all(bind=engine)   # Crear tablas desde cero
    session = TestingSessionLocal()
    yield session
    session.rollback()
    session.close()

# --- Fixture para datos simulados del API ---
@pytest.fixture
def datos_mockeados():
    return [
        {
            "a_o": "2023",
            "trimestre": "1",
            "proveedor": "Claro",
            "abonados_en_servicio": "1000",
            "abonados_pospago": "600",
            "abonados_prepago": "400",
            "l_neas_activas": "950",
            "l_neas_retiradas": "50"
        }
    ]

# --- Prueba unitaria de importar_estaciones ---
def test_importar_estaciones_postgresql(mocker, session_prueba, datos_mockeados):
    # Mock del APIClient para no llamar al API real
    mocker.patch("controllers.main_controller.APIClient.obtener_datos", return_value=datos_mockeados)

    # Forzamos al controlador a usar la sesión de prueba
    mocker.patch("controllers.main_controller.Session", return_value=session_prueba)

    controller = MainController()
    controller.importar_estaciones()

    # Verificamos que los datos fueron insertados correctamente
    estaciones = session_prueba.query(Estacion).all()
    assert len(estaciones) == 1
    assert estaciones[0].nombre == "Claro"
    assert estaciones[0].año == 2023
    assert estaciones[0].abonados_servicio == 1000
# --- Test: eliminar_estacion_id ---
def test_eliminar_estacion_id(mocker, session_prueba):
    # Insertar manualmente una estación para luego eliminarla
    estacion = Estacion(
        año=2023,
        trimestre="1",
        nombre="Movistar",
        abonados_servicio=800,
        abonados_pospago=500,
        abonados_prepago=300,
        lineas_activas=750,
        lineas_retiradas=50
    )
    session_prueba.add(estacion)
    session_prueba.commit()

    estacion_id = estacion.id
    mocker.patch("controllers.main_controller.Session", return_value=session_prueba)

    controller = MainController()
    resultado = controller.eliminar_estacion_id(estacion_id)

    assert resultado is True
    assert session_prueba.query(Estacion).filter_by(id=estacion_id).first() is None

# --- Test: listar_estaciones_por_ano ---
def test_listar_estaciones_por_ano(capsys, mocker, session_prueba):
    # Agregar varias estaciones con distintos años
    estaciones = [
        Estacion(año=2022, trimestre="1", nombre="Tigo", abonados_servicio=500, abonados_pospago=300, abonados_prepago=200, lineas_activas=450, lineas_retiradas=50),
        Estacion(año=2023, trimestre="2", nombre="Claro", abonados_servicio=1000, abonados_pospago=600, abonados_prepago=400, lineas_activas=950, lineas_retiradas=50),
    ]
    session_prueba.add_all(estaciones)
    session_prueba.commit()

    mocker.patch("controllers.main_controller.Session", return_value=session_prueba)
    controller = MainController()

    controller.listar_estaciones_por_ano(2023)
    salida = capsys.readouterr().out

    assert "Claro" in salida
    assert "2023" in salida
    assert "Tigo" not in salida
