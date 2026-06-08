
"""
telemetria.py — Telemetria simulada do satélite EnviroSat.
"""

import json
import random

from datetime import datetime, timezone
from pathlib import Path

REGIOES = [
    "Amazônia Legal - PA",
    "Cerrado - MT",
    "Pantanal - MS",
    "Mata Atlântica - BA",
    "Caatinga - PI",
]

ARQUIVO_CENARIOS = Path("data/cenarios.json")

def carregar_cenarios():

    if not ARQUIVO_CENARIOS.exists():
        return []

    try:

        with open(
            ARQUIVO_CENARIOS,
            "r",
            encoding="utf-8"
        ) as arquivo:

            return json.load(arquivo)

    except Exception:
        return []

def listar_cenarios():

    cenarios = carregar_cenarios()

    return [c["id"] for c in cenarios]

def coletar(cenario_id=None) -> dict:
    """
    Gera telemetria aleatória ou usa cenário fixo.
    """

    cenarios = carregar_cenarios()

    if cenario_id:

        for cenario in cenarios:

            if cenario["id"] == cenario_id:
                return cenario["telemetria"]

    modo_anomalia = random.random() < 0.25

    dados = {

        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),

        "satelite": "EnviroSat-1",

        "orbita_numero": random.randint(
            1200,
            9999
        ),

        "regiao_imageada": random.choice(
            REGIOES
        ),

        "temp_brilho_K": round(
            random.uniform(338, 360)
            if modo_anomalia
            else random.uniform(290, 325),
            1
        ),

        "focos_calor_detectados": (
            random.randint(3, 25)
            if modo_anomalia
            else random.randint(0, 2)
        ),

        "confianca_termica_pct": round(
            random.uniform(55, 99),
            1
        ),

        "ndvi": round(
            random.uniform(-0.1, 0.28)
            if modo_anomalia
            else random.uniform(0.3, 0.85),
            3
        ),

        "cobertura_nuvens_pct": round(
            random.uniform(72, 95)
            if modo_anomalia
            else random.uniform(0, 60),
            1
        ),

        "resolucao_efetiva_m": round(
            random.uniform(10, 30),
            1
        ),

        "imagens_buffer": (
            random.randint(180, 255)
            if modo_anomalia
            else random.randint(0, 120)
        ),

        "buffer_capacidade": 256,

        "downlink_mbps": round(
            random.uniform(10, 45)
            if modo_anomalia
            else random.uniform(80, 300),
            1
        ),

        "erro_geolocalizacao_m": round(
            random.uniform(28, 55)
            if modo_anomalia
            else random.uniform(1, 15),
            2
        ),

        "gps_satellites_lock": random.randint(
            4,
            12
        ),

        "tensao_painel_solar_V": round(
            random.uniform(20, 26)
            if modo_anomalia
            else random.uniform(28, 34),
            2
        ),

        "bateria_pct": round(
            random.uniform(8, 22)
            if modo_anomalia
            else random.uniform(25, 95),
            1
        ),

        "consumo_W": round(
            random.uniform(180, 420),
            1
        ),

        "altitude_km": round(
            random.uniform(740, 760),
            1
        ),

        "velocidade_km_s": round(
            random.uniform(7.4, 7.6),
            3
        ),

        "angulo_nadir_deg": round(
            random.uniform(0, 25),
            2
        ),
    }

    dados["buffer_uso_pct"] = round(
        (
            dados["imagens_buffer"]
            / dados["buffer_capacidade"]
        ) * 100,
        1
    )

    return dados

