from Classes import *


def dinamicar(
        corpo: Corpo,
        ang: float,
        raio: float,
        coef: float
) -> float:
    """
    Descrição:
        Função responsável por aplicar as forças no corpo

    Retorno:
        Retornará o valor da normal no momento
    """

    # Temos todos os vetores em condições de serem usadas.

    # Vesor da Normal
    v_nor = Vetor(
        (
            - corpo.pos.x / raio,
            # Note que enquanto ele estiver em baixo, isso aqui será negativo.
            # Mas ao subir, será positivo.
            1 - (corpo.pos.y / raio)
        )
    )

    # Vesor da Tangente
    v_tan = Vetor(
        (
            1 - (corpo.pos.y / raio),
            corpo.pos.x / raio
        )
    )

    # A partir desses versores, vamos definir nossa física

    # A aceleração centripeta
    an = v_nor.por_escalar(
        (corpo.vel * corpo.vel) / raio
    )

    valor_normal = corpo.massa * ((corpo.vel * corpo.vel) / raio + GRAVIDADE.y * cos(ang))

    # A aceleração tangencial que sempre existirá
    at = v_tan.por_escalar(
        - GRAVIDADE.y * sin(ang)
    )

    # Vamos colocar as forças dissipativas
    # Versor de Velocidade
    Far = corpo.vel.por_escalar(
        - coef
    )

    # Note que como estamos pegando vetores
    at = at + Far.por_escalar(1 / corpo.massa)

    # Agora, podemos pegar esses vetores e passar para carteasiano
    a_result = at + an

    corpo.acel = Vetor(
        (
            a_result * Vetor((1, 0)),
            a_result * Vetor((0, 1))
        )
    )

    return valor_normal





