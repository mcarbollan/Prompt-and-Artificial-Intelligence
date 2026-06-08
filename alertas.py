"""
alertas.py — Thresholds e regras de decisão para o EnviroSat (Trilha 2).
Retorna lista de alertas com nível CRÍTICO, ALERTA ou INFO.
"""
# ─── Definição de thresholds por parâmetro ────────────────────────────────────
THRESHOLDS = {
    # Sensor Térmico
    "temp_brilho_K": {
        "info": {"max": 330},   # Temperatura levemente elevada
        "alerta": {"max": 340},   # Possível foco de calor
        "critico": {"max": None},  # Acima de 340 = foco confirmado (ver abaixo)
    },
    "focos_calor_detectados": {
        "info": {"max": 1},
        "alerta": {"max": 5},
        "critico": {"max": None},
    },
    "confianca_termica_pct": {
        "alerta": {"min": 65},
        "critico": {"min": 55},
    },
    # Sensor Óptico
    "ndvi": {
        "alerta": {"min": 0.3},   # Vegetação degradada
        "critico": {"min": 0.1},   # Vegetação severamente degradada / solo exposto
    },
    "cobertura_nuvens_pct": {
        "alerta": {"max": 70},    # Imagem parcialmente comprometida
        "critico": {"max": None},  # Acima de 85% = imagem inutilizável
    },
    # Buffer
    "buffer_uso_pct": {
        "alerta": {"max": 70},
        "critico": {"max": 90},
    },
    "downlink_mbps": {
        "alerta": {"min": 60},
        "critico": {"min": 30},
    },
    # Geolocalização
    "erro_geolocalizacao_m": {
        "alerta": {"max": 15},
        "critico": {"max": 30},
    },
    # Energia
    "tensao_painel_solar_V": {
        "alerta": {"min": 27},
        "critico": {"min": 24},
    },
    "bateria_pct": {
        "alerta": {"min": 25},
        "critico": {"min": 15},
    },
}
# Thresholds com lógica especial (não cabe na tabela genérica)
FOCOS_CRITICO = 5
TEMP_CRITICO_K = 340
NUVENS_CRITICO_PCT = 85

def avaliar(dados: dict) -> list[str]:
    """
    Avalia os dados de telemetria e retorna lista de alertas formatados.
    Args:
        dados: Dicionário retornado por telemetria.coletar()
    Returns:
        Lista de strings com os alertas ativos, ordenados por severidade.
    """
    alertas_criticos = []
    alertas_alerta = []
    alertas_info = []
    # ── Regras com lógica especial ──────────────────────────────────────────
    # Temperatura térmica crítica
    temp = dados.get("temp_brilho_K", 0)
    focos = dados.get("focos_calor_detectados", 0)
    if temp > TEMP_CRITICO_K or focos > FOCOS_CRITICO:
        alertas_criticos.append(
            f"🔴 [CRÍTICO] INCÊNDIO DETECTADO — {focos} focos de calor, "
            f"temperatura de brilho {temp} K na região {dados.get('regiao_imageada', '?')}"
        )
    elif temp > 330 or focos > 1:
        alertas_alerta.append(
            f"⚠️  [ALERTA] Atividade térmica elevada — {focos} focos, {temp} K "
            f"em {dados.get('regiao_imageada', '?')}"
        )
    # Cobertura de nuvens crítica
    nuvens = dados.get("cobertura_nuvens_pct", 0)
    if nuvens > NUVENS_CRITICO_PCT:
        alertas_criticos.append(
            f"🔴 [CRÍTICO] Imageamento óptico INVÁLIDO — cobertura de nuvens {nuvens}%"
        )
    elif nuvens > 70:
        alertas_alerta.append(
            f"⚠️  [ALERTA] Cobertura de nuvens elevada ({nuvens}%) — imagem parcialmente comprometida"
        )
    # ── Regras genéricas baseadas nos thresholds ────────────────────────────
    regras_genericas = [
        ("ndvi", "NDVI baixo — vegetação degradada/desmatamento", "alerta", "critico"),
        ("buffer_uso_pct", "Buffer de imagens próximo da capacidade", "alerta", "critico"),
        ("downlink_mbps", "Velocidade de downlink abaixo do nominal", "alerta", "critico"),
        ("erro_geolocalizacao_m", "Erro de geolocalização fora da especificação", "alerta", "critico"),
        ("tensao_painel_solar_V", "Tensão dos painéis solares abaixo do nominal", "alerta", "critico"),
        ("bateria_pct", "Nível de bateria crítico", "alerta", "critico"),
        ("confianca_termica_pct", "Baixa confiança na detecção térmica", "alerta", "critico"),
    ]
    for param, descricao, nivel_alerta, nivel_critico in regras_genericas:
        valor = dados.get(param)
        if valor is None:
            continue
        th = THRESHOLDS.get(param, {})
        # Verifica crítico
        lim_crit = th.get("critico", {})
        if _violou(valor, lim_crit.get("min"), lim_crit.get("max")):
            alertas_criticos.append(
                f"🔴 [CRÍTICO] {descricao} — {param}: {valor}"
            )
            continue
        # Verifica alerta
        lim_alerta = th.get("alerta", {})
        if _violou(valor, lim_alerta.get("min"), lim_alerta.get("max")):
            alertas_alerta.append(
                f"⚠️  [ALERTA] {descricao} — {param}: {valor}"
            )
            continue
        # Verifica info
        lim_info = th.get("info", {})
        if _violou(valor, lim_info.get("min"), lim_info.get("max")):
            alertas_info.append(
                f"ℹ️  [INFO] {descricao} — {param}: {valor}"
            )
    return alertas_criticos + alertas_alerta + alertas_info

def _violou(valor: float, min_val, max_val) -> bool:
    """Retorna True se o valor ultrapassar algum limite."""
    if min_val is not None and valor < min_val:
        return True
    if max_val is not None and valor > max_val:
        return True
    return False