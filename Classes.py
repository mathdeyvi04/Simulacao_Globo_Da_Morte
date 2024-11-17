from math import *
from matplotlib import pyplot as pp

PI = 3.141592
CASAS_DECIMAIS = 6
MOSTRAR_STATUS = False


class Vetor:
    """
    Descrição:
        Classe responsável por representar nossas grandezas vetoriais.
    """

    def __init__(
            self,
            FINAL: tuple[float, float],
            INICIO: tuple[float, float] = (0, 0)
    ) -> None:
        """
        Descrição:
            Método responsável por criar vetor.

        Parâmetros:
            FINAL -> Ponto Geométrico de Fim do Vetor
            INICIO -> Ponto Geométrico de Início do Vetor

        Retorno:
            Nenhum
        """

        self.x, self.y = FINAL[0] - INICIO[0], FINAL[1] - INICIO[1]

    def __str__(self) -> str:
        """
        Descrição:
            Método responsável por possibilitar a representação de vetores 2D

        Parâmetros:
            Nenhum

        Retorno:
            String representando o vetor
        """
        return f"{self.x}x + {self.y}y" if self.y >= 0 else f"{self.x}x - {-self.y}y"

    def __add__(self, other):
        """
        Descrição:
            Método responsável por possibilitar a soma entre vetores

        Parâmetro:
            other -> Outro Vetor

        Retorno:
            Vetor Soma
        """

        if not isinstance(other, Vetor):
            raise TypeError

        return Vetor(
            (
                self.x + other.x,
                self.y + other.y
            )
        )

    def __sub__(self, other):
        """
        Descrição:
            Método responsável por possibilitar a diferença entre vetores 2D

        Parâmetro:
            other -> Outro Vetor

        Retorno:
            Vetor Diferença
        """

        if not isinstance(other, Vetor):
            raise TypeError

        return Vetor(
            (
                self.x - other.x,
                self.y - other.y
            )
        )

    def __mul__(self, other) -> float:
        """
        Descrição:
            Método responsável por possibilitar o produto interno entre vetores.

        Parâmetro:
            other -> Outro Vetor

        Retorno:
            Resultado do Produto Interno
        """

        if not isinstance(other, Vetor):
            raise TypeError

        return self.x * other.x + self.y * other.y

    def __round__(self, n=None):
        """
        Descrição:
            Método responsável por permitir uso de round.

        Parâmetros:
            n -> casas decimais

        Retorno:
            Vetor com componentes aproximadas.
        """
        return Vetor(
            (
                round(self.x, n),
                round(self.y, n)
            )
        )

    def por_escalar(self, escalar):
        """
        Descrição:
            Método responsável por possibilitar o produto entre vetor e escalar.

        Parâmetro:
            Autoexplicativo

        Retorno:
            Resultado do Produto por escalar
        """

        if not isinstance(escalar, float) and not isinstance(escalar, int):
            raise TypeError

        return Vetor(
            (
                self.x * escalar,
                self.y * escalar
            )
        )

    def modular(self) -> float:
        """
        Descrição:
            Método responsável por obter o módulo do vetor

        Parâmetro:
            Nenhum

        Retorno:
            Módulo do Vetor
        """

        return sqrt(
            self * self
        )

    # Devemos reeconstruir a função que retornará qual é o ângulo.


GRAVIDADE = Vetor(
    (
        0,
        10
    )
)  # Algumas coisas são como o número pi


class Corpo:
    """
    Descrição:
        Classe responsável por representar nosso objeto.
    """

    def __init__(
            self,
            MASSA: float,
            VELOCIDADE: Vetor = Vetor((0, 0))
    ) -> None:
        """
        Descrição:
            Método responsável por criar nosso corpo

        Parâmetros:
            Massa -> massa do corpo
            Velocidade -> velocidade do corpo

        Retorno:
            Nenhum
        """

        self.massa = MASSA

        self.pos = Vetor((0, 0))
        self.vel = VELOCIDADE
        self.acel = Vetor((0, 0))

    def movimentar(
            self,
            DELTA: float
    ) -> None:
        """
        Descrição:
            Método responsável por movimentar o corpo e modificar
            grandezas cinemáticas.

        Parâmetros:
            DELTA -> intervalo de tempo infinitesimal

        Retorno:
            None.
        """

        self.vel = self.vel + self.acel.por_escalar(
            DELTA
        )

        self.pos = self.pos + self.vel.por_escalar(
            DELTA
        ) + self.acel.por_escalar(
            0.5 * DELTA * DELTA
        )

    def obtendo_polar(
            self,
            raio: float
    ) -> tuple[float, float]:
        """
        Descrição:
            Método responsável por obter o vetor polar
            correspondente ao vetor posição em relação
            do centro

        Retorno:
            Distância ao centro e ângulo em relação à vertical.
        """

        distancia_ao_centro = sqrt(
            self.pos.x * self.pos.x + (self.pos.y - raio) * (self.pos.y - raio)
        )

        angulo = acos(
            (
                    raio - self.pos.y
            ) / (
                distancia_ao_centro
            )
        )

        if self.pos.x < 0:
            # Então estamos do outro lado da circunferência
            angulo = - angulo

        return distancia_ao_centro, angulo

    def apresentar(
            self,
            raio: float
    ) -> tuple[float, float]:
        """
        Descrição:
             Método responsável por apresentar informações do corpo

        Retorno:
            Valor da distância ao centro e do ângulo do corpo.
        """

        distancia_ao_centro, angulo = self.obtendo_polar(
            raio
        )

        distancia_ao_centro = round(
            distancia_ao_centro,
            CASAS_DECIMAIS  # Obvimente teremos flutuações
        )

        if MOSTRAR_STATUS:
            print(
                f"Distancia ao Centro: {round(distancia_ao_centro, CASAS_DECIMAIS)}\nÂngulo Instântaneo: {round(angulo, CASAS_DECIMAIS)}"
            )
            print(
                f"Posição Instântanea: {round(self.pos, CASAS_DECIMAIS)}"
            )
            print(
                f"Velocidade Instântanea: {round(self.vel, CASAS_DECIMAIS)}"
            )
            print(
                f"Aceleração Instântanea: {round(self.acel, CASAS_DECIMAIS)}\n"
            )

        return distancia_ao_centro, angulo

    def cinetica(
            self
    ) -> float:
        """
        Descrição:
            Método responsável por calcular a cinética do corpo
        """

        return 0.5 * self.massa * (self.vel * self.vel)

    def potencial(
            self
    ) -> float:
        """
        Descrição:
            Método responsável por calcular a potencial do corpo.
        """

        return self.massa * abs(GRAVIDADE.y) * self.pos.y
