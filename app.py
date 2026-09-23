import streamlit as st

from utils.simulacao import gerar_passos
from utils.avaliacao import comparar_politicas

from politicas.first_fit import FirstFit
from politicas.first_fit_decreasing import FirstFitDecreasing
from politicas.best_fit import BestFit


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Simulador de Empacotamento",
    page_icon="📦",
    layout="wide"
)


# ============================================================
# ESTADO DA APLICAÇÃO
# ============================================================

if "passos" not in st.session_state:
    st.session_state.passos = []

if "passo_atual" not in st.session_state:
    st.session_state.passo_atual = 0

if "executando" not in st.session_state:
    st.session_state.executando = False

if "politica_atual" not in st.session_state:
    st.session_state.politica_atual = ""

if "resultados_comparacao" not in st.session_state:
    st.session_state.resultados_comparacao = []


# ============================================================
# FUNÇÃO PARA CRIAR A POLÍTICA
# ============================================================

def criar_politica(nome):

    if nome == "First Fit":
        return FirstFit()

    if nome == "First Fit Decreasing":
        return FirstFitDecreasing()

    if nome == "Best Fit":
        return BestFit()

    raise ValueError(
        "Política desconhecida."
    )


# ============================================================
# FUNÇÃO PARA OBTER RESULTADOS DA COMPARAÇÃO
# ============================================================

def obter_resultados_comparacao(
    itens,
    capacidade
):

    politicas = {
        "First Fit": FirstFit(),
        "First Fit Decreasing": FirstFitDecreasing(),
        "Best Fit": BestFit()
    }

    return comparar_politicas(
        itens,
        capacidade,
        politicas
    )


# ============================================================
# INICIAR SIMULAÇÃO
# ============================================================

def iniciar_simulacao(
    itens,
    capacidade,
    politica,
    nome_politica
):

    st.session_state.passos = gerar_passos(
        itens,
        capacidade,
        politica
    )

    st.session_state.passo_atual = 0

    st.session_state.politica_atual = (
        nome_politica
    )


# ============================================================
# RESETAR SIMULAÇÃO
# ============================================================

def resetar():

    st.session_state.passos = []

    st.session_state.passo_atual = 0

    st.session_state.executando = False

    st.session_state.politica_atual = ""

    st.session_state.resultados_comparacao = []


# ============================================================
# TÍTULO
# ============================================================

st.title(
    "📦 Simulador de Empacotamento"
)

st.write(
    "Simulador visual para análise de políticas "
    "de alocação em problemas de empacotamento."
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header(
    "⚙️ Configuração"
)


# ------------------------------------------------------------
# Política
# ------------------------------------------------------------

nome_politica = st.sidebar.selectbox(
    "Política de alocação",
    [
        "First Fit",
        "First Fit Decreasing",
        "Best Fit"
    ]
)


# ------------------------------------------------------------
# Capacidade
# ------------------------------------------------------------

capacidade = st.sidebar.number_input(
    "Capacidade da caixa",
    min_value=1,
    value=10,
    step=1
)


# ------------------------------------------------------------
# Itens
# ------------------------------------------------------------

texto_itens = st.sidebar.text_input(
    "Itens",
    value="2, 5, 7, 8, 3, 4, 6, 1, 9, 5"
)


# ============================================================
# BOTÃO — INICIAR SIMULAÇÃO
# ============================================================

if st.sidebar.button(
    "▶ Iniciar simulação",
    use_container_width=True
):

    try:

        # ----------------------------------------------------
        # Converte os itens para números
        # ----------------------------------------------------

        itens = [
            int(x.strip())
            for x in texto_itens.split(",")
            if x.strip()
        ]


        # ----------------------------------------------------
        # Validação
        # ----------------------------------------------------

        if not itens:

            st.error(
                "Informe pelo menos um item."
            )

        elif any(
            item <= 0
            for item in itens
        ):

            st.error(
                "Todos os itens devem ser maiores que zero."
            )

        elif any(
            item > capacidade
            for item in itens
        ):

            st.error(
                "Existe um item maior que a capacidade da caixa."
            )

        else:

            # ------------------------------------------------
            # Cria a política
            # ------------------------------------------------

            politica = criar_politica(
                nome_politica
            )


            # ------------------------------------------------
            # Inicia a simulação
            # ------------------------------------------------

            iniciar_simulacao(
                itens,
                capacidade,
                politica,
                nome_politica
            )

            st.rerun()


    except ValueError:

        st.error(
            "Digite os itens separados por vírgula."
        )


# ============================================================
# BOTÃO — COMPARAR POLÍTICAS
# ============================================================

if st.sidebar.button(
    "📊 Comparar políticas",
    use_container_width=True
):

    try:

        # ----------------------------------------------------
        # Converte os itens
        # ----------------------------------------------------

        itens = [
            int(x.strip())
            for x in texto_itens.split(",")
            if x.strip()
        ]


        # ----------------------------------------------------
        # Validação
        # ----------------------------------------------------

        if not itens:

            st.error(
                "Informe pelo menos um item."
            )

        elif any(
            item <= 0
            for item in itens
        ):

            st.error(
                "Todos os itens devem ser maiores que zero."
            )

        elif any(
            item > capacidade
            for item in itens
        ):

            st.error(
                "Existe um item maior que a capacidade da caixa."
            )

        else:

            # ------------------------------------------------
            # Executa todas as políticas
            # ------------------------------------------------

            resultados = (
                obter_resultados_comparacao(
                    itens,
                    capacidade
                )
            )


            # ------------------------------------------------
            # Salva os resultados
            # ------------------------------------------------

            st.session_state.resultados_comparacao = (
                resultados
            )

            st.rerun()


    except ValueError:

        st.error(
            "Digite os itens separados por vírgula."
        )


# ============================================================
# ÁREA PRINCIPAL — SIMULAÇÃO
# ============================================================

if st.session_state.passos:

    passos = st.session_state.passos

    indice = st.session_state.passo_atual

    passo = passos[indice]

    caixas = passo["caixas"]


    # ========================================================
    # INFORMAÇÕES DA SIMULAÇÃO
    # ========================================================

    st.subheader(
        f"Política: "
        f"{st.session_state.politica_atual}"
    )

    st.caption(
        f"Passo {indice + 1} de {len(passos)}"
    )


    # ========================================================
    # MENSAGEM DO PASSO
    # ========================================================

    st.info(
        passo["mensagem"]
    )


    # ========================================================
    # ITEM ATUAL
    # ========================================================

    if passo["item"] is not None:

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "📦 Item atual",
                passo["item"]
            )

        with col2:

            st.metric(
                "🏗️ Caixas atuais",
                len(caixas)
            )


    # ========================================================
    # CAIXAS
    # ========================================================

    st.subheader(
        "📦 Caixas"
    )


    if caixas:

        quantidade_colunas = min(
            len(caixas),
            4
        )

        colunas = st.columns(
            quantidade_colunas
        )


        for i, caixa in enumerate(caixas):

            coluna = colunas[
                i % quantidade_colunas
            ]

            total = sum(caixa)

            restante = (
                capacidade - total
            )

            utilizacao = (
                total / capacidade
                if capacidade > 0
                else 0
            )


            with coluna:

                st.markdown(
                    f"### Caixa {i + 1}"
                )


                st.write(
                    f"Itens: `{caixa}`"
                )


                st.progress(
                    min(
                        utilizacao,
                        1.0
                    )
                )


                st.write(
                    f"**{total} / {capacidade}**"
                )


                st.caption(
                    f"Espaço restante: {restante}"
                )


    else:

        st.write(
            "Nenhuma caixa criada ainda."
        )


    # ========================================================
    # ESTATÍSTICAS
    # ========================================================

    st.subheader(
        "📊 Estatísticas"
    )


    total_utilizado = sum(
        sum(caixa)
        for caixa in caixas
    )


    numero_caixas = len(caixas)


    espaco_total = (
        numero_caixas * capacidade
    )


    desperdicio = (
        espaco_total - total_utilizado
    )


    if espaco_total > 0:

        utilizacao_total = (
            total_utilizado
            / espaco_total
            * 100
        )

    else:

        utilizacao_total = 0


    col1, col2, col3, col4 = (
        st.columns(4)
    )


    with col1:

        st.metric(
            "📦 Caixas",
            numero_caixas
        )


    with col2:

        st.metric(
            "📊 Utilização",
            f"{utilizacao_total:.1f}%"
        )


    with col3:

        st.metric(
            "🗑️ Desperdício",
            desperdicio
        )


    with col4:

        st.metric(
            "📐 Capacidade total",
            espaco_total
        )


    # ========================================================
    # CONTROLES
    # ========================================================

    st.subheader(
        "🎮 Controles"
    )


    col1, col2, col3 = (
        st.columns(3)
    )


    # --------------------------------------------------------
    # ANTERIOR
    # --------------------------------------------------------

    with col1:

        anterior = st.button(
            "◀ Anterior",
            use_container_width=True
        )


        if anterior:

            if (
                st.session_state.passo_atual
                > 0
            ):

                st.session_state.passo_atual -= 1

                st.rerun()


    # --------------------------------------------------------
    # PRÓXIMO
    # --------------------------------------------------------

    with col2:

        proximo = st.button(
            "Próximo ▶",
            use_container_width=True
        )


        if proximo:

            if (
                st.session_state.passo_atual
                < len(
                    st.session_state.passos
                ) - 1
            ):

                st.session_state.passo_atual += 1

                st.rerun()


    # --------------------------------------------------------
    # REINICIAR
    # --------------------------------------------------------

    with col3:

        reiniciar = st.button(
            "🔄 Reiniciar",
            use_container_width=True
        )


        if reiniciar:

            resetar()

            st.rerun()


    # ========================================================
    # PROGRESSO
    # ========================================================

    progresso = (
        (indice + 1)
        / len(passos)
    )


    st.progress(
        progresso
    )


else:

    st.info(
        "Configure os parâmetros na barra lateral "
        "e clique em **Iniciar simulação**."
    )


    st.markdown(
        """
        ### 🧠 Políticas disponíveis

        **First Fit**

        Coloca o item na primeira caixa onde ele couber.

        **First Fit Decreasing**

        Ordena os itens do maior para o menor e utiliza
        a estratégia First Fit.

        **Best Fit**

        Coloca o item na caixa que deixa o menor espaço
        restante possível.
        """
    )


# ============================================================
# COMPARAÇÃO DAS POLÍTICAS
# ============================================================

if st.session_state.resultados_comparacao:

    st.divider()

    st.header(
        "📊 Comparação das Políticas"
    )

    st.write(
        "Todas as políticas foram executadas "
        "sobre a mesma instância."
    )


    resultados = (
        st.session_state.resultados_comparacao
    )


    # ========================================================
    # CARTÕES DAS POLÍTICAS
    # ========================================================

    colunas = st.columns(
        len(resultados)
    )


    for coluna, resultado in zip(
        colunas,
        resultados
    ):

        with coluna:

            st.subheader(
                resultado["politica"]
            )


            st.metric(
                "📦 Caixas",
                resultado["numero_caixas"]
            )


            st.metric(
                "📊 Utilização",
                f'{resultado["utilizacao"]:.2f}%'
            )


            st.metric(
                "🗑️ Desperdício",
                resultado["desperdicio"]
            )


            st.metric(
                "⏱️ Tempo",
                f'{resultado["tempo"]:.3f} ms'
            )


    # ========================================================
    # TABELA COMPARATIVA
    # ========================================================

    st.subheader(
        "📋 Tabela comparativa"
    )


    dados_tabela = []


    for resultado in resultados:

        dados_tabela.append(
            {
                "Política": resultado["politica"],
                "Caixas": resultado["numero_caixas"],
                "Utilização (%)": round(
                    resultado["utilizacao"],
                    2
                ),
                "Desperdício": resultado["desperdicio"],
                "Tempo (s)": round(
                    resultado["tempo"],
                    6
                )
            }
        )


    st.dataframe(
        dados_tabela,
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # INSTÂNCIA UTILIZADA
    # ========================================================

    st.subheader(
        "🧪 Instância utilizada"
    )


    st.code(
        f"Capacidade: {capacidade}\n"
        f"Itens: {texto_itens}",
        language="text"
    )