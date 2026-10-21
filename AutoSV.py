import os

import streamlit as st
from openai import OpenAI


LM_STUDIO_URL = os.getenv("LM_STUDIO_URL", "http://127.0.0.1:1234/v1")
API_KEY = os.getenv("sk-lm-yR4NfT1J:0FfIe1Q2dTCaLZ99PIIJ")

st.set_page_config(
    page_title="AutoSV-Op",
    page_icon="A",
    layout="wide",
    initial_sidebar_state="expanded"
)

VEHICULOS = [
    {
        "marca": "Toyota",
        "modelo": "Corolla",
        "anio": 2018,
        "precio": 10500,
        "tipo": "Sedán",
        "combustible": "Gasolina",
        "transmision": "Automática",
        "stock": 2
    },
    {
        "marca": "Honda",
        "modelo": "Civic",
        "anio": 2017,
        "precio": 9800,
        "tipo": "Sedán",
        "combustible": "Gasolina",
        "transmision": "Automática",
        "stock": 1
    },
    {
        "marca": "Hyundai",
        "modelo": "Tucson",
        "anio": 2019,
        "precio": 14500,
        "tipo": "SUV",
        "combustible": "Gasolina",
        "transmision": "Automática",
        "stock": 2
    },
    {
        "marca": "Toyota",
        "modelo": "Hilux",
        "anio": 2018,
        "precio": 19500,
        "tipo": "Pickup",
        "combustible": "Diésel",
        "transmision": "Manual",
        "stock": 1
    },
    {
        "marca": "Kia",
        "modelo": "Sportage",
        "anio": 2020,
        "precio": 15900,
        "tipo": "SUV",
        "combustible": "Gasolina",
        "transmision": "Automática",
        "stock": 2
    }
]


st.markdown("""
<style>
    .stApp {
        background-color: #0b0d12;
        color: #f5f5f7;
    }

    [data-testid="stSidebar"] {
        background-color: #12151d;
        border-right: 1px solid #292d38;
    }

    .hero {
        background: linear-gradient(120deg, #191f2c, #10131a);
        padding: 32px;
        border: 1px solid #303747;
        border-radius: 22px;
        margin-bottom: 25px;
    }

    .hero h1 {
        font-size: 38px;
        margin-bottom: 8px;
        color: #ffffff;
    }

    .hero p {
        color: #aeb8ca;
        font-size: 16px;
    }

    .metric-card {
        background: #151923;
        border: 1px solid #2b3140;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 12px;
    }

    .vehicle-card {
        background: #151923;
        border: 1px solid #2b3140;
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 15px;
    }

    .price {
        color: #8ab4ff;
        font-size: 25px;
        font-weight: 700;
    }

    .muted {
        color: #aeb8ca;
    }

    div.stButton > button {
        border-radius: 10px;
        min-height: 42px;
    }

    [data-testid="stChatMessage"] {
        border: 1px solid #292d38;
        border-radius: 14px;
    }
</style>
""", unsafe_allow_html=True)


def conectar_lm_studio():
    return OpenAI(
        base_url="http://127.0.0.1:1234/v1",
        api_key="sk-lm-yR4NfT1J:0FfIe1Q2dTCaLZ99PIIJ",
        timeout=120.0
    )


def dinero(cantidad):
    return f"${cantidad:,.2f}"


def inventario_texto():
    lineas = []

    for v in VEHICULOS:
        lineas.append(
            f"- {v['marca']} {v['modelo']} {v['anio']}: "
            f"{dinero(v['precio'])}; tipo {v['tipo']}; "
            f"combustible {v['combustible']}; "
            f"transmisión {v['transmision']}; "
            f"unidades disponibles: {v['stock']}."
        )

    return "\n".join(lineas)


def consultar_modelo(mensajes, modelo):
    cliente = conectar_lm_studio()

    respuesta = cliente.chat.completions.create(
        model=modelo,
        messages=mensajes,
        temperature=0.4
    )

    return respuesta.choices[0].message.content



if "historial" not in st.session_state:
    st.session_state.historial = []

if "mensajes_api" not in st.session_state:
    st.session_state.mensajes_api = []

# ==========================================
# BARRA LATERAL
# ==========================================
with st.sidebar:
    st.markdown("## AutoSV-Op")
    st.caption("Asistente inteligente para vehículos")

    pagina = st.radio(
        "NAVEGACIÓN",
        ["Inicio", "Catálogo", "Asistente IA"]
    )

    st.divider()

    st.markdown("### Configuración del modelo")

    modelo_texto = st.text_input(
        "Modelo de LM Studio",
        value="llama-3.2-3b-instruct",
        help="Usa el identificador del modelo que aparece en LM Studio."
    )

    st.caption("Servidor local: 127.0.0.1:1234")

    if st.button("Probar conexión", use_container_width=True):
        try:
            cliente = conectar_lm_studio()
            modelos = cliente.models.list()

            st.success("Conexión con LM Studio establecida.")

            with st.expander("Modelos detectados"):
                for modelo in modelos.data:
                    st.write(modelo.id)

        except Exception as e:
            st.error("No se pudo conectar con LM Studio.")
            st.caption(str(e))

    st.divider()
    st.caption("Laboratorio III")


st.markdown("""
<div class="hero">
    <h1>AutoSV-Op</h1>
    <p>Tu próximo vehículo comienza con una conversación inteligente.</p>
    <p>Catálogo de vehículos usados · Asistencia mediante inteligencia artificial</p>
</div>
""", unsafe_allow_html=True)


if pagina == "Inicio":
    st.subheader("Panel principal")

    unidades = sum(v["stock"] for v in VEHICULOS)

    precio_promedio = (
        sum(v["precio"] for v in VEHICULOS) / len(VEHICULOS)
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="muted">Modelos registrados</p>'
            f'<h2>{len(VEHICULOS)}</h2>'
            f'</div>',
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="muted">Unidades disponibles</p>'
            f'<h2>{unidades}</h2>'
            f'</div>',
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f'<div class="metric-card">'
            f'<p class="muted">Precio promedio</p>'
            f'<h2>{dinero(precio_promedio)}</h2>'
            f'</div>',
            unsafe_allow_html=True
        )

    st.subheader("Vehículos destacados")

    destacados = st.columns(3)

    for i, vehiculo in enumerate(VEHICULOS[:3]):
        with destacados[i]:
            st.markdown(
                f'<div class="vehicle-card">'
                f'<h3>{vehiculo["marca"]} {vehiculo["modelo"]}</h3>'
                f'<p class="muted">'
                f'{vehiculo["anio"]} · {vehiculo["tipo"]}'
                f'</p>'
                f'<p class="price">{dinero(vehiculo["precio"])}</p>'
                f'<p class="muted">'
                f'{vehiculo["combustible"]} · '
                f'{vehiculo["transmision"]}'
                f'</p>'
                f'<p>Disponibles: {vehiculo["stock"]}</p>'
                f'</div>',
                unsafe_allow_html=True
            )

    st.info(
        "Los precios y las existencias son datos ficticios para la "
        "demostración académica. Sustitúyelos por datos reales antes "
        "de utilizar el sistema comercialmente."
    )


elif pagina == "Catálogo":
    st.subheader("Catálogo de vehículos")

    st.write("Filtra los vehículos según tus preferencias.")

    col1, col2 = st.columns(2)

    with col1:
        tipo = st.selectbox(
            "Tipo de vehículo",
            ["Todos", "Sedán", "SUV", "Pickup"]
        )

    with col2:
        presupuesto = st.number_input(
            "Presupuesto máximo en dólares",
            min_value=0,
            value=25000,
            step=500
        )

    resultados = [
        v for v in VEHICULOS
        if (tipo == "Todos" or v["tipo"] == tipo)
        and v["precio"] <= presupuesto
    ]

    st.caption(f"{len(resultados)} resultado(s)")

    if not resultados:
        st.warning(
            "No hay vehículos que coincidan con esos filtros."
        )

    else:
        for v in resultados:
            with st.container(border=True):
                a, b = st.columns([3, 1])

                with a:
                    st.markdown(
                        f"### {v['marca']} {v['modelo']} ({v['anio']})"
                    )

                    st.write(
                        f"**Tipo:** {v['tipo']} · "
                        f"**Combustible:** {v['combustible']}"
                    )

                    st.write(
                        f"**Transmisión:** {v['transmision']}"
                    )

                    st.write(
                        f"**Unidades disponibles:** {v['stock']}"
                    )

                with b:
                    st.markdown(f"### {dinero(v['precio'])}")


elif pagina == "Asistente IA":
    st.subheader("Asistente virtual")

    st.write(
        "Consulta precios, características y disponibilidad del catálogo."
    )

    for mensaje in st.session_state.historial:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])

    pregunta = st.chat_input(
        "Ejemplo: ¿Qué SUV cuesta menos de $16,000?"
    )

    if pregunta:
        st.session_state.historial.append(
            {"role": "user", "content": pregunta}
        )

        with st.chat_message("user"):
            st.markdown(pregunta)

        instrucciones = f"""
Eres AutoSV-Op, el asistente virtual de una agencia de vehículos usados.

Responde en español, de forma amable, profesional y clara.
Ayuda a los clientes a comparar vehículos y elegir según sus necesidades.
No inventes precios, existencias, garantías ni especificaciones.
Si no conoces un dato, dilo claramente.
Aclara que los precios mostrados son datos de demostración.

CATÁLOGO DISPONIBLE:
{inventario_texto()}
"""

        mensajes = [
            {"role": "system", "content": instrucciones}
        ]

        for m in st.session_state.historial[-12:]:
            mensajes.append({
                "role": m["role"],
                "content": m["content"]
            })

        with st.chat_message("assistant"):
            with st.spinner(
                "El asistente está preparando la respuesta..."
            ):
                try:
                    respuesta = consultar_modelo(
                        mensajes,
                        modelo_texto
                    )

                    st.markdown(respuesta)

                    st.session_state.historial.append(
                        {
                            "role": "assistant",
                            "content": respuesta
                        }
                    )

                except Exception as e:
                    st.error(
                        "No se pudo obtener respuesta. Comprueba que "
                        "LM Studio tenga el modelo cargado y el servidor iniciado."
                    )

                    st.code(str(e))

    if st.button("Limpiar conversación"):
        st.session_state.historial = []
        st.rerun()


# PIE DE PÁGINA

st.divider()

st.caption(
    "AutoSV-Op · Sistemas Expertos· "
    "Integrantes: José Salas y Jonathan Constanza "
)