
"""
Motor de análise da Mission Control AI — Trilha EnviroSat.
"""

from pathlib import Path
import json
import os

from dotenv import load_dotenv
from ollama import Client

from src import telemetria, alertas

load_dotenv()

TRILHA = "envirosat"
MODELO = "gpt-oss:120b"

client = Client(
    host="https://ollama.com/api",
    headers={
        "Authorization": "Bearer " + os.environ.get("OLLAMA_API_KEY", "")
    },
)

def llm(prompt, system=None, max_tokens=800, temperature=0.3):
    """Envia prompt ao Ollama Cloud."""

    messages = []

    if system:
        messages.append({
            "role": "system",
            "content": system
        })

    messages.append({
        "role": "user",
        "content": prompt
    })

    try:
        resposta = client.chat(
            model=MODELO,
            messages=messages,
            options={
                "num_predict": max_tokens,
                "temperature": temperature,
            },
            stream=False,
        )

        return resposta["message"]["content"].strip()

    except Exception as erro:
        return f"⚠️ Erro ao consultar IA: {erro}"

def load_system_prompt():
    """Carrega o system prompt."""

    path = Path("prompts/system_prompt.md")

    if path.exists():
        return path.read_text(encoding="utf-8")

    return (
        "Você é um especialista em monitoramento ambiental "
        "via satélite."
    )

class MissionEngine:
    """Motor principal da trilha EnviroSat."""

    def __init__(self):

        self.trilha = TRILHA
        self.system_prompt = load_system_prompt()

        self._ultimo_dados = None
        self._ultimos_alertas = []

        self.historico = []

    def is_ready(self):
        return True

    def _registrar_historico(self, dados, alertas_ativos):

        self.historico.append({
            "dados": dados,
            "alertas": alertas_ativos
        })

        self.historico = self.historico[-5:]

    def status_snapshot(self):
        """Retorna resumo operacional da missão."""

        dados = telemetria.coletar()

        self._ultimo_dados = dados

        lista_alertas = alertas.avaliar(dados)

        self._ultimos_alertas = lista_alertas

        self._registrar_historico(dados, lista_alertas)

        linhas = [

            f"🛰 {dados['satelite']} | Órbita #{dados['orbita_numero']}",
            f"📍 Região: {dados['regiao_imageada']}",
            f"🕒 {dados['timestamp']}",
            "",

            "── SENSOR TÉRMICO ──────────────────────",
            f"Temperatura de brilho : {dados['temp_brilho_K']} K",
            f"Focos de calor        : {dados['focos_calor_detectados']}",
            f"Confiança detecção    : {dados['confianca_termica_pct']}%",
            "",

            "── SENSOR ÓPTICO ───────────────────────",
            f"NDVI                  : {dados['ndvi']}",
            f"Cobertura nuvens      : {dados['cobertura_nuvens_pct']}%",
            f"Resolução efetiva     : {dados['resolucao_efetiva_m']} m",
            "",

            "── BUFFER & DOWNLINK ───────────────────",
            f"Buffer                : {dados['imagens_buffer']}/{dados['buffer_capacidade']}",
            f"Uso buffer            : {dados['buffer_uso_pct']}%",
            f"Downlink              : {dados['downlink_mbps']} Mbps",
            "",

            "── GEOLOCALIZAÇÃO ──────────────────────",
            f"Erro GPS              : {dados['erro_geolocalizacao_m']} m",
            f"Satélites em lock     : {dados['gps_satellites_lock']}",
            "",

            "── ENERGIA ─────────────────────────────",
            f"Tensão painel         : {dados['tensao_painel_solar_V']} V",
            f"Bateria               : {dados['bateria_pct']}%",
            f"Consumo               : {dados['consumo_W']} W",
            "",
        ]

        if lista_alertas:

            linhas.append(
                "── ALERTAS ATIVOS ──────────────────────"
            )

            linhas.extend(
                f"- {alerta}"
                for alerta in lista_alertas
            )

        else:

            linhas.append(
                "✅ Todos os parâmetros operando normalmente."
            )

        return "\n".join(linhas)

    def _montar_prompt(
        self,
        pergunta_usuario,
        dados,
        lista_alertas
    ):
        """Monta prompt contextual para IA."""

        historico_resumido = self.historico[-3:]

        return f"""
PERGUNTA DO OPERADOR:
{pergunta_usuario}

CONTEXTO DA MISSÃO:
- Projeto: Mission Control AI
- Trilha: EnviroSat
- Satélite: {dados['satelite']}
- Setor impactado:
  sustentabilidade, combate a incêndios,
  monitoramento ambiental e desmatamento.

PERSONAS:
- Operador ambiental
- Coordenador de brigada anti-incêndio
- Analista de compliance ambiental

TELEMETRIA ATUAL (JSON):
{json.dumps(dados, ensure_ascii=False, indent=2)}

ALERTAS DETECTADOS:
{json.dumps(lista_alertas, ensure_ascii=False, indent=2)}

HISTÓRICO RECENTE:
{json.dumps(historico_resumido, ensure_ascii=False, indent=2)}

TAREFA:
Responda em português brasileiro.

Explique:
1. Estado atual da missão
2. Principal risco operacional
3. Ação recomendada
4. Impacto terrestre
5. Prioridade operacional

Se houver risco crítico,
seja direto e objetivo.
""".strip()

    def analyze(self, pergunta_usuario):
        """Executa análise completa da missão."""

        dados = telemetria.coletar()

        self._ultimo_dados = dados

        lista_alertas = alertas.avaliar(dados)

        self._ultimos_alertas = lista_alertas

        self._registrar_historico(
            dados,
            lista_alertas
        )

        prompt = self._montar_prompt(
            pergunta_usuario,
            dados,
            lista_alertas
        )

        resposta_ia = llm(
            prompt,
            system=self.system_prompt
        )

        status = self.status_snapshot()

        return f"""
{status}

── ANÁLISE DA IA ─────────────────────

{resposta_ia}
""".strip()

