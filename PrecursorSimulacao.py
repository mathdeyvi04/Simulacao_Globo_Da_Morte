"""
Descrição:
    Código responsável por iniciar a simulação e realizar as plotagens.
"""

from Física import *

INTERVALO_DE_TEMPO = 0.0001  # Definindo quantas iterações faremos.
TEMPO_TOTAL = 10  # Tempo em que haverá finalização.


def simulando(vel_inicial, COEF):
    # 16.5 -> Minima para chegar em alpha = 0
    # 27.1 -> Mínima para chegar em alpha = 90°
    corpo = Corpo(
        1,
        Vetor(
            (
                # Velocidade Inicial em X
                # Para Metade: 14,1
                # Para topo: 22,3
                vel_inicial,
                # Velocidade Inicial em Y
                0
            )
        )
    )
    RAIO = 1  # Raio da esfera
    ENERGIA_INICIAL = corpo.cinetica()

    # Vamos ter listas para guardar resultados
    valores_tempo = []
    valores_angulo = []
    valores_energia_cinetica = []
    valores_energia_potencial = []
    valores_dissipada = []
    valores_normal = []

    # Iniciando a simulação
    tempo_total = 0

    while tempo_total <= TEMPO_TOTAL:

        # Vamos apresentar os dados do corpo
        distancia_ao_centro, angulo = corpo.apresentar(
            RAIO
        )

        if angulo == -9:
            # Sabemos que houve um erro
            break

        # Vamos realizar operações
        normal = dinamicar(corpo, angulo, RAIO, COEF)

        # Vamos mover o corpo
        corpo.movimentar(
            INTERVALO_DE_TEMPO
        )

        # Salvando valores
        valores_tempo.append(
            tempo_total
        )
        valores_angulo.append(
            angulo
        )
        valores_energia_cinetica.append(
            corpo.cinetica()
        )
        valores_energia_potencial.append(
            corpo.potencial()
        )
        valores_dissipada.append(
            ENERGIA_INICIAL - corpo.potencial() - corpo.cinetica()
        )
        valores_normal.append(
            normal
        )

        if normal <= 0:
            print("Houve queda")
            return angulo - (PI / 2)

        if corpo.vel.y <= 0 and corpo.vel.x <= 0:
            # Quer dizer que iniciou movimento de descida, mesmo
            # que a normal não tenha sido atingida
            return -1

        if corpo.vel.y <= 0:
            return -1

        # Avançando no tempo
        tempo_total = tempo_total + INTERVALO_DE_TEMPO

    # Quer dizer que chegamos ao final sem precisar tocar o 0
    return -1

    pp.subplot(1, 3, 1)
    pp.plot(
        valores_tempo,
        valores_angulo
    )
    pp.xlabel(
        "Tempo(s)"
    )
    pp.ylabel(
        "Angulo(rad)"
    )
    pp.title(
        f"v0 = {vel_inicial}(m/s)"
    )
    pp.grid(True)

    pp.subplot(1, 3, 2)
    pp.plot(
        valores_tempo,
        valores_energia_cinetica,
        label="Cinética"
    )
    pp.plot(
        valores_tempo,
        valores_energia_potencial,
        label="Potencial"
    )
    pp.plot(
        valores_tempo,
        valores_dissipada,
        label="Dissipada"
    )
    pp.title(
        f" coef = {COEF}"
    )
    pp.xlabel("Tempo(s)")
    pp.ylabel("Energia(J)")
    pp.legend()
    pp.grid(True)

    pp.subplot(1, 3, 3)
    pp.plot(
        valores_tempo,
        valores_normal
    )
    pp.xlabel(
        "Tempo(s)"
    )
    pp.ylabel(
        "Normal(N)"
    )
    pp.grid(True)

    pp.show()

