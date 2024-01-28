import numpy as np
from typing import Union
import math

import numpy as np

import numpy as np
from typing import Union


class Transformator12:
    def __init__(self, n: int):
        self.iloscPulsow = 12
        self.blokowanie = 10_000.0
        self.przewodzenie = 0.01
        self.spadek = 0.5

        self.Rz = np.array([1.0, 1.0, 1.0, 0.33, 0.33, 0.33])
        self.R = 25.0

        self.d = np.zeros(12)
        self.a = np.zeros((8, 8))
        self.w = np.zeros(8)
        self.uD = np.zeros(12)
        self.i = np.zeros(6)
        self.v = None
        self.iloscKrokow = n
        self.prady = np.zeros((self.iloscKrokow, 6))

    @property
    def Prady(self) -> np.ndarray:
        return self.prady

    @property
    def V(self) -> Union[float, None]:
        return self.v[7] if self.v is not None else None

    def GaussElimination(self, A: np.ndarray, b: np.ndarray, n: int) -> float:
        x = np.zeros(n)

        tmpA = np.zeros((n, n + 1))

        for i in range(n):
            for j in range(n):
                tmpA[i, j] = A[i, j]
            tmpA[i, n] = b[i]

        tmp = 0.0

        for k in range(n - 1):
            for i in range(k + 1, n):
                tmp = tmpA[i, k] / tmpA[k, k]
                for j in range(k, n + 1):
                    tmpA[i, j] -= tmp * tmpA[k, j]

        for k in range(n - 1, -1, -1):
            tmp = 0
            for j in range(k + 1, n):
                tmp += tmpA[k, j] * x[j]
            x[k] = (tmpA[k, n] - tmp) / tmpA[k, k]

        return x

    def LiczAdmitancje(self) -> None:
        self.a[0, 0] = 1 / self.Rz[3] + 1 / self.Rz[4] + 1 / self.Rz[5]
        self.a[0, 1:4] = -1 / self.Rz[3], -1 / self.Rz[4], -1 / self.Rz[5]

        self.a[1, 0] = -1 / self.Rz[3]
        self.a[1, 1] = 1 / self.Rz[3] + 1 / self.d[0] + 1 / self.d[1]
        self.a[1, 7] = -1 / self.d[0]

        self.a[2, 0] = -1 / self.Rz[4]
        self.a[2, 2] = 1 / self.Rz[4] + 1 / self.d[2] + 1 / self.d[3]
        self.a[2, 7] = -1 / self.d[2]

        self.a[3, 0] = -1 / self.Rz[5]
        self.a[3, 3] = 1 / self.Rz[5] + 1 / self.d[4] + 1 / self.d[5]
        self.a[3, 7] = -1 / self.d[4]

        self.a[4, 4] = 1 / self.Rz[0] + 1 / self.Rz[2] + 1 / self.d[6] + 1 / self.d[7]
        self.a[4, 5:8] = -1 / self.Rz[0], -1 / self.Rz[2], -1 / self.d[6]

        self.a[5, 4] = -1 / self.Rz[0]
        self.a[5, 5] = 1 / self.Rz[0] + 1 / self.Rz[1] + 1 / self.d[8] + 1 / self.d[9]
        self.a[5, 6] = -1 / self.Rz[1]
        self.a[5, 7] = -1 / self.d[8]

        self.a[6, 4] = -1 / self.Rz[2]
        self.a[6, 5] = -1 / self.Rz[1]
        self.a[6, 6] = 1 / self.Rz[2] + 1 / self.Rz[1] + 1 / self.d[10] + 1 / self.d[11]
        self.a[6, 7] = -1 / self.d[10]

        self.a[7, 1] = -1 / self.d[0]
        self.a[7, 2] = -1 / self.d[2]
        self.a[7, 3] = -1 / self.d[4]
        self.a[7, 4] = -1 / self.d[6]
        self.a[7, 5] = -1 / self.d[8]
        self.a[7, 6] = -1 / self.d[10]
        self.a[7, 7] = (
            1 / self.d[0]
            + 1 / self.d[2]
            + 1 / self.d[4]
            + 1 / self.d[6]
            + 1 / self.d[8]
            + 1 / self.d[10]
            + 1 / self.R
        )

    def LiczWymuszenia(self, u: np.ndarray) -> None:
        self.w[0] = -u[3] / self.Rz[3] - u[4] / self.Rz[4] - u[5] / self.Rz[5]
        self.w[1] = u[3] / self.Rz[3]
        self.w[2] = u[4] / self.Rz[4]
        self.w[3] = u[5] / self.Rz[5]
        self.w[4] = u[0] / self.Rz[0] - u[2] / self.Rz[2]
        self.w[5] = u[1] / self.Rz[1] - u[0] / self.Rz[0]
        self.w[6] = u[2] / self.Rz[2] - u[1] / self.Rz[1]
        self.w[7] = 0.0

    def LiczUD(self, v: np.ndarray) -> None:
        self.uD[0] = v[1] - v[7]
        self.uD[1] = -v[1]
        self.uD[2] = v[2] - v[7]
        self.uD[3] = -v[2]
        self.uD[4] = v[3] - v[7]
        self.uD[5] = -v[3]
        self.uD[6] = v[4] - v[7]
        self.uD[7] = -v[4]
        self.uD[8] = v[5] - v[7]
        self.uD[9] = -v[5]
        self.uD[10] = v[6] - v[7]
        self.uD[11] = -v[6]

    def Test(self) -> bool:
        for i in range(self.iloscPulsow):
            if self.uD[i] > self.spadek and self.d[i] == self.blokowanie:
                return False
            elif self.uD[i] < 0.0 and self.d[i] == self.przewodzenie:
                return False
        return True

    def Iteracja(self, u: np.ndarray) -> None:
        # zamkniecie wszystkich diod
        for i in range(self.iloscPulsow):
            self.d[i] = self.blokowanie

        it = 0

        self.LiczAdmitancje()
        self.LiczWymuszenia(u)
        self.v = self.GaussElimination(self.a, self.w, 8)
        self.LiczUD(self.v)

        while not self.Test() and it <= self.iloscPulsow + 1:
            self.zmiana = False
            # sprawdzenie czy nie ma tu za dużo otwartych
            for i in range(self.iloscPulsow):
                if self.uD[i] < 0.0 and self.d[i] == self.przewodzenie:
                    self.d[i] = self.blokowanie
                    self.zmiana = True

            # wlaczanie najbardziej dodatnich
            if not self.zmiana:
                indeks = np.argmax(self.uD)
                # odblokowanie wszystkich z maksymalną wartością
                for i in range(self.iloscPulsow):
                    if (
                        np.abs(self.uD[i] - self.uD[indeks]) < 0.0001
                        and self.uD[i] > self.spadek
                    ):
                        self.d[i] = self.przewodzenie

                # nowe wyznaczenie Admintancji i Wymuszenia
            self.LiczAdmitancje()
            self.LiczWymuszenia(u)

            self.v = self.GaussElimination(self.a, self.w, 8)
            self.LiczUD(self.v)
            it += 1

    def LiczPrad(self, u: np.ndarray, k: int) -> None:
        self.prady[k, 0] = (self.v[5] + u[0] - self.v[4]) / self.Rz[0]
        self.prady[k, 1] = (self.v[6] + u[1] - self.v[5]) / self.Rz[1]
        self.prady[k, 2] = (self.v[4] + u[2] - self.v[6]) / self.Rz[2]
        self.prady[k, 3] = (self.v[0] + u[3] - self.v[1]) / self.Rz[3]
        self.prady[k, 4] = (self.v[0] + u[4] - self.v[2]) / self.Rz[4]
        self.prady[k, 5] = (self.v[0] + u[5] - self.v[3]) / self.Rz[5]

    def Symulacja(self, u: np.ndarray, n: int) -> np.ndarray:
        vtmp = np.zeros(n)
        utk = np.zeros(6)
        for i in range(n):
            utk[0] = u[0, i]
            utk[1] = u[1, i]
            utk[2] = u[2, i]
            utk[3] = u[3, i]
            utk[4] = u[4, i]
            utk[5] = u[5, i]
            self.Iteracja(utk)
            vtmp[i] = self.V
            self.LiczPrad(utk, i)

        return vtmp

    def ZapiszPrady(self, plik: str) -> None:
        napis = ""
        for i in range(self.iloscKrokow):
            napis += f"{self.prady[i, 0]} "
            for j in range(1, 6):
                napis += f"{self.prady[i, j]} "
            napis += "\n"
        with open(plik, "w") as f:
            f.write(napis)


class FunkcjaCelu12:
    def __init__(self, u: np.ndarray, n: int, t12: Transformator12, deltaT: float):
        self.R25 = 15
        self.R75 = 25

        self.t12 = t12
        self.pierwiastek = math.sqrt(3.0)

        self.u = u
        self.n = n
        self.deltaT = deltaT

    def WartoscSkuteczna(self, v: list[float], krok: float) -> float:
        n = len(v)
        s = sum(val**2 for val in v)
        return math.sqrt(s / n)

    def DrukujWSkuteczne(self, x: list[float]) -> str:
        napis = ""
        # v = self.Wartosc(x) # unused
        pK = np.zeros((6, self.n))
        p = self.t12.Prady

        for i in range(6):
            for j in range(self.n):
                pK[i][j] = p[j, i]

        for i in range(6):
            napis += f"{i} {self.WartoscSkuteczna(pK[i], self.deltaT)}"
            napis += "\n"
        return napis

    def Wartosc2(self) -> float:
        wU = 0.0
        if self.t12.R > self.R75:
            wU = 1.0
        elif self.t12.R > self.R25:
            wU = (self.t12.R - self.R25) / (self.R75 - self.R25)

        wI = 1.0 - wU

        v = self.t12.Symulacja(self.u, self.n)
        p = self.t12.Prady

        pierw3 = math.sqrt(3)

        p0 = np.zeros(self.n)
        p1 = np.zeros(self.n)
        p2 = np.zeros(self.n)
        p3 = np.zeros(self.n)
        p4 = np.zeros(self.n)
        p5 = np.zeros(self.n)

        suma = 0.0
        for i in range(self.n):
            p0[i] = p[i, 0]
            p1[i] = p[i, 1]
            p2[i] = p[i, 2]
            p3[i] = p[i, 3]
            p4[i] = p[i, 4]
            p5[i] = p[i, 5]

        suma += abs(
            self.WartoscSkuteczna(p1, self.deltaT)
            - self.WartoscSkuteczna(p0, self.deltaT)
        )
        suma += abs(
            self.WartoscSkuteczna(p2, self.deltaT)
            - self.WartoscSkuteczna(p0, self.deltaT)
        )
        suma += abs(
            self.WartoscSkuteczna(p2, self.deltaT)
            - self.WartoscSkuteczna(p1, self.deltaT)
        )
        suma += abs(
            self.WartoscSkuteczna(p4, self.deltaT)
            - self.WartoscSkuteczna(p3, self.deltaT)
        )
        suma += abs(
            self.WartoscSkuteczna(p5, self.deltaT)
            - self.WartoscSkuteczna(p3, self.deltaT)
        )
        suma += abs(
            self.WartoscSkuteczna(p5, self.deltaT)
            - self.WartoscSkuteczna(p4, self.deltaT)
        )

        suma += abs(
            pierw3
            - self.WartoscSkuteczna(p3, self.deltaT)
            / self.WartoscSkuteczna(p0, self.deltaT)
        )
        suma += abs(
            pierw3
            - self.WartoscSkuteczna(p4, self.deltaT)
            / self.WartoscSkuteczna(p1, self.deltaT)
        )
        suma += abs(
            pierw3
            - self.WartoscSkuteczna(p5, self.deltaT)
            / self.WartoscSkuteczna(p2, self.deltaT)
        )

        min_val = v[0]
        max_val = v[0]
        for i in range(1, self.n):
            if min_val > v[i]:
                min_val = v[i]
            elif max_val < v[i]:
                max_val = v[i]
        return wU * (max_val - min_val) + wI * suma

    def Wartosc(self, *x: float) -> float:
        for i in range(3):
            for j in range(self.n):
                self.u[i + 3, j] = x[i] * self.u[i, j] / self.pierwiastek
        return self.Wartosc2()

    def V(self, *x: float) -> float:
        for i in range(3):
            for j in range(self.n):
                self.u[i + 3, j] = x[i] * self.u[i, j] / self.pierwiastek
        return self.t12.Symulacja(self.u, self.n)


class Transformator12:
    def __init__(self, n: int):
        self.iloscPulsow = 12
        self.blokowanie = 10_000.0
        self.przewodzenie = 0.01
        self.spadek = 0.5

        self.Rz = np.array([1.0, 1.0, 1.0, 0.33, 0.33, 0.33])
        self.R = 25.0

        self.d = np.zeros(12)
        self.a = np.zeros((8, 8))
        self.w = np.zeros(8)
        self.uD = np.zeros(12)
        self.i = np.zeros(6)
        self.v = None
        self.iloscKrokow = n
        self.prady = np.zeros((self.iloscKrokow, 6))

    @property
    def Prady(self) -> np.ndarray:
        return self.prady

    @property
    def V(self) -> Union[float, None]:
        return self.v[7] if self.v is not None else None

    def GaussElimination(self, A: np.ndarray, b: np.ndarray, n: int) -> float:
        x = np.zeros(n)

        tmpA = np.zeros((n, n + 1))

        for i in range(n):
            for j in range(n):
                tmpA[i, j] = A[i, j]
            tmpA[i, n] = b[i]

        tmp = 0.0

        for k in range(n - 1):
            for i in range(k + 1, n):
                tmp = tmpA[i, k] / tmpA[k, k]
                for j in range(k, n + 1):
                    tmpA[i, j] -= tmp * tmpA[k, j]

        for k in range(n - 1, -1, -1):
            tmp = 0
            for j in range(k + 1, n):
                tmp += tmpA[k, j] * x[j]
            x[k] = (tmpA[k, n] - tmp) / tmpA[k, k]

        return x

    def LiczAdmitancje(self) -> None:
        self.a[0, 0] = 1 / self.Rz[3] + 1 / self.Rz[4] + 1 / self.Rz[5]
        self.a[0, 1:4] = -1 / self.Rz[3], -1 / self.Rz[4], -1 / self.Rz[5]

        self.a[1, 0] = -1 / self.Rz[3]
        self.a[1, 1] = 1 / self.Rz[3] + 1 / self.d[0] + 1 / self.d[1]
        self.a[1, 7] = -1 / self.d[0]

        self.a[2, 0] = -1 / self.Rz[4]
        self.a[2, 2] = 1 / self.Rz[4] + 1 / self.d[2] + 1 / self.d[3]
        self.a[2, 7] = -1 / self.d[2]

        self.a[3, 0] = -1 / self.Rz[5]
        self.a[3, 3] = 1 / self.Rz[5] + 1 / self.d[4] + 1 / self.d[5]
        self.a[3, 7] = -1 / self.d[4]

        self.a[4, 4] = 1 / self.Rz[0] + 1 / self.Rz[2] + 1 / self.d[6] + 1 / self.d[7]
        self.a[4, 5:8] = -1 / self.Rz[0], -1 / self.Rz[2], -1 / self.d[6]

        self.a[5, 4] = -1 / self.Rz[0]
        self.a[5, 5] = 1 / self.Rz[0] + 1 / self.Rz[1] + 1 / self.d[8] + 1 / self.d[9]
        self.a[5, 6] = -1 / self.Rz[1]
        self.a[5, 7] = -1 / self.d[8]

        self.a[6, 4] = -1 / self.Rz[2]
        self.a[6, 5] = -1 / self.Rz[1]
        self.a[6, 6] = 1 / self.Rz[2] + 1 / self.Rz[1] + 1 / self.d[10] + 1 / self.d[11]
        self.a[6, 7] = -1 / self.d[10]

        self.a[7, 1] = -1 / self.d[0]
        self.a[7, 2] = -1 / self.d[2]
        self.a[7, 3] = -1 / self.d[4]
        self.a[7, 4] = -1 / self.d[6]
        self.a[7, 5] = -1 / self.d[8]
        self.a[7, 6] = -1 / self.d[10]
        self.a[7, 7] = (
            1 / self.d[0]
            + 1 / self.d[2]
            + 1 / self.d[4]
            + 1 / self.d[6]
            + 1 / self.d[8]
            + 1 / self.d[10]
            + 1 / self.R
        )

    def LiczWymuszenia(self, u: np.ndarray) -> None:
        self.w[0] = -u[3] / self.Rz[3] - u[4] / self.Rz[4] - u[5] / self.Rz[5]
        self.w[1] = u[3] / self.Rz[3]
        self.w[2] = u[4] / self.Rz[4]
        self.w[3] = u[5] / self.Rz[5]
        self.w[4] = u[0] / self.Rz[0] - u[2] / self.Rz[2]
        self.w[5] = u[1] / self.Rz[1] - u[0] / self.Rz[0]
        self.w[6] = u[2] / self.Rz[2] - u[1] / self.Rz[1]
        self.w[7] = 0.0

    def LiczUD(self, v: np.ndarray) -> None:
        self.uD[0] = v[1] - v[7]
        self.uD[1] = -v[1]
        self.uD[2] = v[2] - v[7]
        self.uD[3] = -v[2]
        self.uD[4] = v[3] - v[7]
        self.uD[5] = -v[3]
        self.uD[6] = v[4] - v[7]
        self.uD[7] = -v[4]
        self.uD[8] = v[5] - v[7]
        self.uD[9] = -v[5]
        self.uD[10] = v[6] - v[7]
        self.uD[11] = -v[6]

    def Test(self) -> bool:
        for i in range(self.iloscPulsow):
            if self.uD[i] > self.spadek and self.d[i] == self.blokowanie:
                return False
            elif self.uD[i] < 0.0 and self.d[i] == self.przewodzenie:
                return False
        return True

    def Iteracja(self, u: np.ndarray) -> None:
        # zamkniecie wszystkich diod
        for i in range(self.iloscPulsow):
            self.d[i] = self.blokowanie

        it = 0

        self.LiczAdmitancje()
        self.LiczWymuszenia(u)
        self.v = self.GaussElimination(self.a, self.w, 8)
        self.LiczUD(self.v)

        while not self.Test() and it <= self.iloscPulsow + 1:
            self.zmiana = False
            # sprawdzenie czy nie ma tu za dużo otwartych
            for i in range(self.iloscPulsow):
                if self.uD[i] < 0.0 and self.d[i] == self.przewodzenie:
                    self.d[i] = self.blokowanie
                    self.zmiana = True

            # wlaczanie najbardziej dodatnich
            if not self.zmiana:
                indeks = np.argmax(self.uD)
                # odblokowanie wszystkich z maksymalną wartością
                for i in range(self.iloscPulsow):
                    if (
                        np.abs(self.uD[i] - self.uD[indeks]) < 0.0001
                        and self.uD[i] > self.spadek
                    ):
                        self.d[i] = self.przewodzenie

                # nowe wyznaczenie Admintancji i Wymuszenia
            self.LiczAdmitancje()
            self.LiczWymuszenia(u)

            self.v = self.GaussElimination(self.a, self.w, 8)
            self.LiczUD(self.v)
            it += 1

    def LiczPrad(self, u: np.ndarray, k: int) -> None:
        self.prady[k, 0] = (self.v[5] + u[0] - self.v[4]) / self.Rz[0]
        self.prady[k, 1] = (self.v[6] + u[1] - self.v[5]) / self.Rz[1]
        self.prady[k, 2] = (self.v[4] + u[2] - self.v[6]) / self.Rz[2]
        self.prady[k, 3] = (self.v[0] + u[3] - self.v[1]) / self.Rz[3]
        self.prady[k, 4] = (self.v[0] + u[4] - self.v[2]) / self.Rz[4]
        self.prady[k, 5] = (self.v[0] + u[5] - self.v[3]) / self.Rz[5]

    def Symulacja(self, u: np.ndarray, n: int) -> np.ndarray:
        vtmp = np.zeros(n)
        utk = np.zeros(6)
        for i in range(n):
            utk[0] = u[0, i]
            utk[1] = u[1, i]
            utk[2] = u[2, i]
            utk[3] = u[3, i]
            utk[4] = u[4, i]
            utk[5] = u[5, i]
            self.Iteracja(utk)
            vtmp[i] = self.V
            self.LiczPrad(utk, i)

        return vtmp

    def ZapiszPrady(self, plik: str) -> None:
        napis = ""
        for i in range(self.iloscKrokow):
            napis += f"{self.prady[i, 0]} "
            for j in range(1, 6):
                napis += f"{self.prady[i, j]} "
            napis += "\n"
        with open(plik, "w") as f:
            f.write(napis)


import math

import numpy as np


class ObjectiveFunction:
    def __init__(self):
        self.n = 401
        self.deltaT = 0.00005

        self.omega = 100 * math.pi
        self.alpha = 2.0 * math.pi / 3.0
        self.wsp = math.sin(7.5 * math.pi / 180.0) / math.sin(52.5 * math.pi / 180.0)
        self.uabc = np.zeros((self.n, 3))

        self.t12 = Transformator12(self.n)
        self.u = np.zeros((6, self.n))
        self.t = 0

        self.t12.R = 15

        self.GenerujNapiecieSieci2(
            100.0,
            100.0,
            100.0,
            1.5,
            2.3,
            1.2,
            2.2,
            0.5,
            1.1,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        )

        for i in range(self.n):
            self.u[0, i] = self.uabc[i][0]
            self.u[1, i] = self.uabc[i][1]
            self.u[2, i] = self.uabc[i][2]
            self.u[3, i] = self.u[0, i] / math.sqrt(3.0)
            self.u[4, i] = self.u[1, i] / math.sqrt(3.0)
            self.u[5, i] = self.u[2, i] / math.sqrt(3.0)
            self.t += self.deltaT

        self.a = [0.5, 0.5, 0.5]
        self.b = [1.5, 1.5, 1.5]

        self.FunkcjaCelu = FunkcjaCelu12(self.u, 401, self.t12, self.deltaT)

    def GenerujNapiecieSieci2(self, *param: float) -> None:
        t = 0.0
        # res = "" # unused
        for i in range(self.n):
            self.uabc[i] = [
                param[0] * math.sin(self.omega * t)
                + param[3] * math.sin(2 * (self.omega * t + param[9]))
                + param[4] * math.sin(3 * (self.omega * t + param[10]))
                + param[5] * math.sin(5 * (self.omega * t + param[11]))
                + param[6] * math.sin(7 * (self.omega * t + param[12]))
                + param[7] * math.sin(11 * (self.omega * t + param[13]))
                + param[8] * math.sin(13 * (self.omega * t + param[14])),
                param[1] * math.sin(self.omega * t + self.alpha)
                + param[3] * math.sin(2 * (self.omega * t + param[9]))
                + param[4] * math.sin(3 * (self.omega * t + param[10]))
                + param[5] * math.sin(5 * (self.omega * t + param[11] + self.alpha))
                + param[6] * math.sin(7 * (self.omega * t + param[12] + self.alpha))
                + param[7] * math.sin(11 * (self.omega * t + param[13] + self.alpha))
                + param[8] * math.sin(13 * (self.omega * t + param[14] + self.alpha)),
                param[2] * math.sin(self.omega * t + 2.0 * self.alpha)
                + param[3] * math.sin(2 * (self.omega * t + param[9]))
                + param[4] * math.sin(3 * (self.omega * t + param[10]))
                + param[5]
                * math.sin(5 * (self.omega * t + param[11] + 2.0 * self.alpha))
                + param[6]
                * math.sin(7 * (self.omega * t + param[12] + 2.0 * self.alpha))
                + param[7]
                * math.sin(11 * (self.omega * t + param[13] + 2.0 * self.alpha))
                + param[8]
                * math.sin(13 * (self.omega * t + param[14] + 2.0 * self.alpha)),
            ]
            t += self.deltaT


def __main__(X):
    obj = ObjectiveFunction()

    return obj.FunkcjaCelu.Wartosc(*X)
