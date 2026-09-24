import streamlit as st

from utils.simulacao import gerar_passos
from utils.avaliacao import comparar_politicas

from politicas.first_fit import FirstFit
from politicas.first_fit_decreasing import FirstFitDecreasing
from politicas.best_fit import BestFit
from politicas.completa_exata import CompletaExataVisual


st.set_page_config(
    page_title="Simulador Visual de Bin Packing",
    page_icon="📦",
    layout="wide"
)


if "passos" not in st.session_state:
    st.session_state.passos = []

if "passo_atual" not in st.session_state:
    st.session_state.passo_atual = 0

if "politica_atual" not in st.session_state:
    st.session_state.politica_atual = ""

if "resultados_comparacao" not in st.session_state:
    st.session_state.resultados_comparacao = []


def criar_politica(nome):
    if nome == "First Fit":
        return FirstFit()
    if nome == "First Fit Decreasing":
        return FirstFitDecreasing()
    if nome == "Best Fit":
        return BestFit()
    if nome == "Completa Exata (Visual)":
        return CompletaExataVisual()
    raise ValueError("Política desconhecida.")


def obter_resultados_comparacao(itens, capacidade):
    politicas = {
        "First Fit": FirstFit(),
        "First Fit Decreasing": FirstFitDecreasing(),
        "Best Fit": BestFit(),
        "Completa Exata": CompletaExataVisual(),
    }

    return comparar_politicas(
        itens,
        capacidade,
        politicas
    )


def iniciar_simulacao(itens, capacidade, politica, nome_politica):
    st.session_state.passos = gerar_passos(
        itens,
        capacidade,
        politica
    )
    st.session_state.passo_atual = 0
    st.session_state.politica_atual = nome_politica


def resetar():
    st.session_state.passos = []
    st.session_state.passo_atual = 0
    st.session_state.politica_atual = ""
    st.session_state.resultados_comparacao = []


st.title("📦 Simulador Visual de Bin Packing")
st.write(
    "Visualize heurísticas clássicas e a política Completa Exata, "
    "incluindo Lower Bound, Upper Bound, bitsets e busca exata."
)


st.sidebar.header("⚙️ Configuração")

nome_politica = st.sidebar.selectbox(
    "Política de alocação",
    [
        "First Fit",
        "First Fit Decreasing",
        "Best Fit",
        "Completa Exata (Visual)",
    ]
)

capacidade = st.sidebar.number_input(
    "Capacidade da caixa",
    min_value=1,
    value=10,
    step=1
)

texto_itens = st.sidebar.text_input(
    "Itens",
    value="2, 5, 7, 8, 3, 4, 6, 1, 9, 5"
)


def ler_itens():
    itens = [
        int(x.strip())
        for x in texto_itens.split(",")
        if x.strip()
    ]

    if not itens:
        raise ValueError("Informe pelo menos um item.")

    if any(item <= 0 for item in itens):
        raise ValueError("Todos os itens devem ser maiores que zero.")

    if any(item > capacidade for item in itens):
        raise ValueError(
            "Existe um item maior que a capacidade da caixa."
        )

    return itens


if st.sidebar.button(
    "▶ Iniciar simulação",
    use_container_width=True
):
    try:
        itens = ler_itens()
        politica = criar_politica(nome_politica)
        iniciar_simulacao(
            itens,
            capacidade,
            politica,
            nome_politica
        )
        st.rerun()

    except ValueError as e:
        st.error(str(e))


if st.sidebar.button(
    "📊 Comparar políticas",
    use_container_width=True
):
    try:
        itens = ler_itens()
        st.session_state.resultados_comparacao = (
            obter_resultados_comparacao(
                itens,
                capacidade
            )
        )
        st.rerun()

    except ValueError as e:
        st.error(str(e))


if st.session_state.passos:
    passos = st.session_state.passos
    indice = st.session_state.passo_atual
    passo = passos[indice]
    caixas = passo.get("caixas", [])

    st.subheader(
        f"Política: {st.session_state.politica_atual}"
    )

    st.caption(
        f"Passo {indice + 1} de {len(passos)}"
    )

    tipo = passo.get("tipo", "")

    if tipo in {
        "lower_bound",
        "upper_bound",
        "bitset",
        "tentativa_k",
        "solucao_k",
        "otimo",
        "final",
    }:
        st.info(passo["mensagem"])
    elif tipo == "backtrack":
        st.warning(passo["mensagem"])
    else:
        st.write(passo["mensagem"])

    # Painel didático exclusivo da política completa.
    if st.session_state.politica_atual == "Completa Exata (Visual)":
        lb = passo.get("lower_bound")
        ub = passo.get("upper_bound")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Lower Bound (LB)",
                lb if lb is not None else "-"
            )

        with c2:
            st.metric(
                "Upper Bound (UB)",
                ub if ub is not None else "-"
            )

        with c3:
            k = passo.get("k")
            st.metric(
                "K em teste",
                k if k is not None else "-"
            )

        if passo.get("somas") is not None:
            st.subheader("🧠 Somas alcançáveis")
            st.write(
                "A programação dinâmica com bitset indica quais "
                "somas podem ser formadas pelos itens."
            )
            st.code(
                str(passo["somas"]),
                language="text"
            )

        if passo.get("pode_completar_exato") is not None:
            if passo["pode_completar_exato"]:
                st.success(
                    "Existe uma combinação dos itens restantes "
                    "capaz de preencher exatamente a sobra desta caixa."
                )
            else:
                st.caption(
                    "Nenhuma combinação dos itens restantes preenche "
                    "exatamente esta sobra. A busca ainda pode continuar "
                    "porque uma caixa não precisa ficar cheia."
                )

    if passo.get("item") is not None:
        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "📦 Item atual",
                passo["item"]
            )

        with col2:
            st.metric(
                "🏗️ Caixas visíveis",
                len(caixas)
            )

    st.subheader("📦 Caixas")

    if caixas:
        quantidade_colunas = min(
            max(len(caixas), 1),
            4
        )
        colunas = st.columns(quantidade_colunas)

        for i, caixa in enumerate(caixas):
            coluna = colunas[
                i % quantidade_colunas
            ]

            total = sum(caixa)
            restante = capacidade - total
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
                    min(max(utilizacao, 0.0), 1.0)
                )
                st.write(
                    f"**{total} / {capacidade}**"
                )
                st.caption(
                    f"Espaço restante: {restante}"
                )
    else:
        st.write(
            "Nenhuma caixa montada neste passo."
        )

    st.subheader("📊 Estatísticas do passo")

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
    utilizacao_total = (
        total_utilizado / espaco_total * 100
        if espaco_total > 0
        else 0
    )

    col1, col2, col3, col4 = st.columns(4)

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

    st.subheader("🎮 Controles")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button(
            "◀ Anterior",
            use_container_width=True
        ):
            if st.session_state.passo_atual > 0:
                st.session_state.passo_atual -= 1
                st.rerun()

    with col2:
        if st.button(
            "Próximo ▶",
            use_container_width=True
        ):
            if (
                st.session_state.passo_atual
                < len(passos) - 1
            ):
                st.session_state.passo_atual += 1
                st.rerun()

    with col3:
        if st.button(
            "🔄 Reiniciar",
            use_container_width=True
        ):
            resetar()
            st.rerun()

    st.progress(
        (indice + 1) / len(passos)
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
        Ordena os itens do maior para o menor e aplica First Fit.

        **Best Fit**  
        Escolhe a caixa que deixa a menor sobra.

        **Completa Exata (Visual)**  
        Calcula o Lower Bound, obtém um Upper Bound com BFD,
        calcula somas alcançáveis com bitsets e usa busca exata
        para tentar chegar ao menor número possível de caixas.
        """
    )


if st.session_state.resultados_comparacao:
    st.divider()
    st.header("📊 Comparação das Políticas")

    resultados = (
        st.session_state.resultados_comparacao
    )

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

            if resultado.get("lower_bound") is not None:
                st.caption(
                    f"LB: {resultado['lower_bound']} | "
                    f"UB: {resultado['upper_bound']} | "
                    f"Ótimo: "
                    f"{'sim' if resultado['otimo_comprovado'] else 'não'}"
                )

    st.subheader("📋 Tabela comparativa")

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
                "Tempo (ms)": round(
                    resultado["tempo"],
                    6
                ),
                "LB": resultado.get("lower_bound"),
                "UB": resultado.get("upper_bound"),
                "Ótimo comprovado": (
                    resultado.get(
                        "otimo_comprovado"
                    )
                ),
            }
        )

    st.dataframe(
        dados_tabela,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("🧪 Instância utilizada")
    st.code(
        f"Capacidade: {capacidade}\n"
        f"Itens: {texto_itens}",
        language="text"
    )
