"""
Descrição:
    Vamos desenvolver uma forma de obter soluções de equações
    inviáveis de serem solucionadas analiticamente.
"""
import matplotlib.pyplot as plt
from matplotlib import pyplot as pp
from math import sqrt, acos, sin

R = 10


def plotagem(
        eixo_x: list[float],
        eixo_y: list[float],
        label_x: str,
        label_y: str,
        titulo: str = "",
) -> None:
    """
        Já comentado.
    """

    pp.plot(
        eixo_x,
        eixo_y
    )

    pp.xlabel(
        label_x
    )

    pp.ylabel(
        label_y
    )

    pp.title(
        titulo
    )

    pp.grid(True)
    pp.show()


def obtendo_coeficientes(
        seno: float
) -> tuple[float, float, float]:
    """
    Descrição:
        Função responsável por obter os coeficientes da trajetória
        que será descrita pelo corpo neste caso específico em que
        o seno é valor dado.
    """

    inverso_seno = 1 / seno
    inverso_seno_cubico = inverso_seno * inverso_seno * inverso_seno
    cos = sqrt(1 - seno * seno)

    return (
        # Coeficiente Independente
        1 + inverso_seno - cos * cos * inverso_seno_cubico * 0.5,
        # Coeficiente Linear
        - cos * inverso_seno + cos * inverso_seno_cubico,
        # Coeficiente Quadrático
        - 0.5 * inverso_seno_cubico
    )


def obtendo_ponto_de_impacto(
        se_esta_parte_de_baixo: bool,
        C1: float,
        C2: float,
        C3: float
):
    """
    Descrição:
        Dos coeficientes, sabemos a trajetória da parábola.
        Vamos pegar a da circunferência e da parábola e tentar
        obter o ponto de impacto.

    Parâmetros:
        se_esta_parte_de_baixo -> apenas identificará quais funções estaremos manipulando.
        C1 -> independentes
        C2 -> linear
        C3 -> quadrático

    Retorno:
        Coordenadas do ponto de impacto
    """

    definidor_de_funcao = -1 if se_esta_parte_de_baixo else 1
    limite = 1 if se_esta_parte_de_baixo else 0

    def Distancia(
            x: float
    ) -> float:

        return (
            abs(1 + definidor_de_funcao * sqrt(1 - x * x) - C1 - C2 * x - C3 * x * x)
        )

    # Vamos obter pela proximidade
    menor_proximidade = 1000
    a_encontrado = 0

    for possivel_a in range(-1 * 1000, limite * 1000, 1):
        possivel_a = possivel_a / 1000

        proximidade = Distancia(
            possivel_a
        )

        if proximidade < menor_proximidade:
            menor_proximidade = proximidade
            a_encontrado = possivel_a

    # De posse de a
    b_encontrado = 1 + definidor_de_funcao * sqrt(1 - a_encontrado * a_encontrado)

    return a_encontrado, b_encontrado


def obtendo_tangente_da_parabola(
        C2: float,
        C3: float,
        abcissa_do_impacto: float,
        ordenada_do_impacto
) -> float:
    """
    Descrição:
        Função responsável por calcular o vetor diretor
        da reta tangente à parabola no instante do impacto
    """

    diretor_tg_parabola = (
        1,
        C2 + 2 * abcissa_do_impacto * C3
    )

    diretor_tg_circunf = (
        1,
        - abcissa_do_impacto / (ordenada_do_impacto - 1)
    )

    mod_dir_parab = sqrt(1 + diretor_tg_parabola[1] * diretor_tg_parabola[1])

    mod_dir_circunf = sqrt(1 + diretor_tg_circunf[1] * diretor_tg_circunf[1])

    prod_escalar = 1 + diretor_tg_parabola[1] * diretor_tg_circunf[1]

    angulo = acos(
        prod_escalar / (
                mod_dir_parab * mod_dir_circunf
        )
    )

    if b > 1:
        angulo = 3.1415 - angulo

    return angulo


# Vamos iniciar a simulação
CASAS_DECIMAIS_DO_SENO = 2
INCREMENTO = pow(
    10,
    -CASAS_DECIMAIS_DO_SENO
)
# Se for zero, os coeficientes explodem.
s = INCREMENTO  # Valor inicial do seno do ângulo de queda
valores_senos = []
valores_abcissas = []
valores_ordenadas = []
valores_de_velocidade_de_impacto = []
valores_de_angulo_de_impacto = []
valores_componente = []
while s <= 1:  # Afinal, o seno não pode ser maior

    # Vamos calcular os coeficientes da trajetória do corpo
    c1, c2, c3 = obtendo_coeficientes(
        s
    )  # CORRETO ATÉ AQUI

    # Vamos obter o ponto em que a trajetória da parábola
    # encontra a circunferência.
    a, b = obtendo_ponto_de_impacto(
        s < sqrt(3) / 2,
        c1, c2, c3
    )

    valores_senos.append(s)
    valores_abcissas.append(a)
    valores_ordenadas.append(round(b, 3))
    valores_de_velocidade_de_impacto.append(
        3 * s - 2 * b + 2
    )

    angulo_de_impacto = obtendo_tangente_da_parabola(
        c2,
        c3,
        a,
        b
    )

    valores_de_angulo_de_impacto.append(
        round(angulo_de_impacto, 2)
    )

    valores_componente.append(
        round(
            abs(3 * s - 2 * b + 2) * sin(angulo_de_impacto)
            ,2
        )
    )

    s = round(
        s + INCREMENTO,
        CASAS_DECIMAIS_DO_SENO
    )


def plotando_ponto_de_impacto():
    pp.subplot(1, 2, 1)
    pp.plot(
        valores_senos,
        valores_abcissas
    )
    pp.xlabel(
        "seno(a)"
    )
    pp.ylabel(
        "abcissa"
    )
    pp.title(
        "Abcissa do Impacto"
    )
    pp.grid(True)

    pp.subplot(1, 2, 2)
    pp.plot(
        valores_senos,
        valores_ordenadas
    )
    pp.xlabel(
        "seno(a)"
    )
    pp.ylabel(
        "ordenada"
    )
    pp.title(
        "Ordenada do Impacto"
    )
    pp.grid(True)
    pp.show()


plotagem(
    valores_senos,
    valores_componente,
    "seno(a)",
    "Fração da Componente Normal",
    ""
)
