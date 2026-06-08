# Prompt-and-Artificial-Intelligence
**Laura Godoy Callegari RM569181 / Mariana Dreset Carbollan RM569207**

O projeto **Mission Control IA** é responsável por criar dados simulados de telemetria de satélites, monitorar automaticamente possíveis ocorrências por meio de regras desenvolvidas em Python e utilizar inteligência artificial generativa, integrada via Ollama Cloud, para produzir explicações claras sobre a situação da missão em linguagem natural.

A plataforma relaciona informações e eventos ocorridos no ambiente espacial com aplicações práticas na Terra, demonstrando seus impactos em áreas como transporte inteligente, operações logísticas, agricultura de precisão e sistemas de navegação para veículos autônomos.

O público-alvo principal da solução é o engenheiro responsável pelo segmento espacial, cuja função envolve supervisionar o desempenho do satélite, identificar falhas operacionais e tomar decisões técnicas diante de situações anormais.

Além disso, o sistema também atende perfis secundários, como gestores de frotas de transporte e profissionais da agricultura de precisão. Esses usuários dependem da confiabilidade dos sinais GNSS para atividades como monitoramento de veículos, definição de rotas eficientes, automação de processos agrícolas e navegação com alta precisão.

**Plataformas utilizadas:**
. Pyton 3.10+
. Ollama
. JSON
. Chat GPT
. Prompt-toolkit
. Pyton-dotenv
. Rish
. Pyfiglet
. Requests

**Como Executar o Programa**

1. Clone o repositório do projeto.

2. Crie e ative o ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

No Windows:

```bash
.venv\Scripts\activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Crie o arquivo `.env` na raiz do projeto utilizando o modelo disponível em `.env.example` e preencha as variáveis necessárias.

5. Execute o programa:

```bash
python main.py
```

Após a inicialização, o sistema estará pronto para uso através do terminal.
