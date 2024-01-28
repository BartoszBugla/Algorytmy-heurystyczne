import numpy as np
import math


class Transformer12:
    def __init__(self, n):
        self.iloscPulsow = 12
        self.blokowanie = 10000.0
        self.przewodzenie = 0.01
        self.spadek = 0.5

        self.Rz = np.array([1.0, 1.0, 1.0, 0.33, 0.33, 0.33], dtype=np.float64)
        self.R = 25.0

        self.d = np.zeros(12, dtype=np.float64)
        self.a = np.zeros((8, 8), dtype=np.float64)
        self.w = np.zeros(8, dtype=np.float64)
        self.uD = np.zeros(12, dtype=np.float64)
        self.i = np.zeros(6, dtype=np.float64)
        self.v = None
        self.iloscKrokow = n
        self.prady = np.zeros((self.iloscKrokow, 6), dtype=np.float64)
    @property
    def V(self):
        return self.v[7]

    def gauss_elimination(self, A, b, n):
        
        x = np.zeros(n, dtype=np.float64)
        tmpA = np.zeros((n, n + 1), dtype=np.float64)

        for i in range(n):
            for j in range(n):
                tmpA[i, j] = A[i, j]
            tmpA[i, n] = b[i]

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

    def licz_admitancje(self):
        self.a[0, 0] = 1 / self.Rz[3] + 1 / self.Rz[4] + 1 / self.Rz[5]
        self.a[0, 1] = -1 / self.Rz[3]
        self.a[0, 2] = -1 / self.Rz[4]
        self.a[0, 3] = -1 / self.Rz[5]

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
        self.a[4, 5] = -1 / self.Rz[0]
        self.a[4, 6] = -1 / self.Rz[2]
        self.a[4, 7] = -1 / self.d[6]

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
        self.a[7, 7] = 1 / self.d[0] + 1 / self.d[2] + 1 / self.d[4] + 1 / self.d[6] + 1 / self.d[8] + 1 / self.d[10] + 1 / self.R


    def licz_wymuszenia(self, u):
        self.w[0] = -u[3] / self.Rz[3] - u[4] / self.Rz[4] - u[5] / self.Rz[5]
        self.w[1] = u[3] / self.Rz[3]
        self.w[2] = u[4] / self.Rz[4]
        self.w[3] = u[5] / self.Rz[5]
        self.w[4] = u[0] / self.Rz[0] - u[2] / self.Rz[2]
        self.w[5] = u[1] / self.Rz[1] - u[0] / self.Rz[0]
        self.w[6] = u[2] / self.Rz[2] - u[1] / self.Rz[1]
        self.w[7] = 0.0

    def licz_ud(self, v):
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

    def test(self):
        for i in range(self.iloscPulsow):
            if self.uD[i] > self.spadek and self.d[i] == self.blokowanie:
                return False
            elif self.uD[i] < 0.0 and self.d[i] == self.przewodzenie:
                return False
        return True

    def iteracja(self, u):
        for i in range(self.iloscPulsow):
            self.d[i] = self.blokowanie

        it = 0

        self.licz_admitancje()
        self.licz_wymuszenia(u)
        self.v = self.gauss_elimination(self.a, self.w, 8)
        self.licz_ud(self.v)

        while not self.test() and it <= self.iloscPulsow + 1:
            it += 1
            self.zmiana = False

            for i in range(self.iloscPulsow):
                if self.uD[i] < 0.0 and self.d[i] == self.przewodzenie:
                    self.d[i] = self.blokowanie
                    self.zmiana = True

            if not self.zmiana:
                max_val = np.max(self.uD)

                # Odblokowanie wszystkich z maksymalną wartością
                for i in range(self.iloscPulsow):
                    if abs(self.uD[i] - max_val) < 0.0001 and self.uD[i] > self.spadek:
                        self.d[i] = self.przewodzenie

            self.licz_admitancje()
            self.licz_wymuszenia(u)
            self.v = self.gauss_elimination(self.a, self.w, 8)
            self.licz_ud(self.v)

                

    def symulacja(self, u, n):
        vtmp = np.zeros(n, dtype=np.float64)
        utk = np.zeros(6, dtype=np.float64)

        for i in range(n):
            utk[0] = u[0, i]
            utk[1] = u[1, i]
            utk[2] = u[2, i]
            utk[3] = u[3, i]
            utk[4] = u[4, i]
            utk[5] = u[5, i]
            self.iteracja(utk)
            vtmp[i] = self.V
            self.licz_prad(utk, i)

        return vtmp

    def licz_prad(self, u, k):
        self.prady[k, 0] = (self.v[5] + u[0] - self.v[4]) / self.Rz[0]
        self.prady[k, 1] = (self.v[6] + u[1] - self.v[5]) / self.Rz[1]
        self.prady[k, 2] = (self.v[4] + u[2] - self.v[6]) / self.Rz[2]
        self.prady[k, 3] = (self.v[0] + u[3] - self.v[1]) / self.Rz[3]
        self.prady[k, 4] = (self.v[0] + u[4] - self.v[2]) / self.Rz[4]
        self.prady[k, 5] = (self.v[0] + u[5] - self.v[3]) / self.Rz[5]

    def zapisz_prady(self, plik):
        with open(plik, 'w') as file:
            for i in range(self.iloscKrokow):
                line = ' '.join(map(str, self.prady[i, :]))
                file.write(f"{line}\n")
                
class FunkcjaCelu12:
    def __init__(self, u, n, t12, deltaT):
        self.R25 = 15
        self.R75 = 25
        self.t12 = t12
        self.u = u
        self.n = n
        self.deltaT = deltaT
        self.pierwiastek = math.sqrt(3.0)

    def wartosc_skuteczna(self, v, krok):
        n = len(v)
        s = sum([i ** 2 for i in v])
        return math.sqrt(s / n)

    def drukuj_w_skuteczne(self, x):
        napis = ""
        v = self.wartosc_param(x)
        pK = []
        p = self.t12.prady

        for i in range(6):
            pK.append([p[j, i] for j in range(self.n)])

        for i in range(6):
            napis += f"{i} {self.wartosc_skuteczna(pK[i], self.deltaT)}\n"

        return napis

    def wartosc(self):
        wU = 1.0 if self.t12.R > self.R75 else ((self.t12.R - self.R25) / (self.R75 - self.R25)) if self.t12.R > self.R25 else 0.0
        wI = 1.0 - wU

        v = self.t12.symulacja(self.u, self.n)
        p = self.t12.prady

        pierw3 = math.sqrt(3)

        p0, p1, p2, p3, p4, p5 = np.zeros((6, self.n), dtype=np.float64)

        for i in range(self.n):
            p0[i], p1[i], p2[i], p3[i], p4[i], p5[i] = [p[i, j] for j in range(6)]

        suma = sum([abs(self.wartosc_skuteczna(p1, self.deltaT) - self.wartosc_skuteczna(p0, self.deltaT)),
                    abs(self.wartosc_skuteczna(p2, self.deltaT) - self.wartosc_skuteczna(p0, self.deltaT)),
                    abs(self.wartosc_skuteczna(p2, self.deltaT) - self.wartosc_skuteczna(p1, self.deltaT)),
                    abs(self.wartosc_skuteczna(p4, self.deltaT) - self.wartosc_skuteczna(p3, self.deltaT)),
                    abs(self.wartosc_skuteczna(p5, self.deltaT) - self.wartosc_skuteczna(p3, self.deltaT)),
                    abs(self.wartosc_skuteczna(p5, self.deltaT) - self.wartosc_skuteczna(p4, self.deltaT)),
                    abs(pierw3 - self.wartosc_skuteczna(p3, self.deltaT) / self.wartosc_skuteczna(p0, self.deltaT)),
                    abs(pierw3 - self.wartosc_skuteczna(p4, self.deltaT) / self.wartosc_skuteczna(p1, self.deltaT)),
                    abs(pierw3 - self.wartosc_skuteczna(p5, self.deltaT) / self.wartosc_skuteczna(p2, self.deltaT))])

        min_v = min(v)
        max_v = max(v)
        return wU * (max_v - min_v) + wI * suma

    def wartosc_param(self, x):
        # obliczenia napięć 

        for i in range(3):
            self.u[i + 3, :] = x[i] * self.u[i, :] / self.pierwiastek

        return self.wartosc()

    def v(self, *x):
        for i in range(3):
            self.u[i + 3, :self.n] = x[i] * self.u[i, :self.n] / self.pierwiastek
        return self.t12.symulacja(self.u, self.n)

class ObjectiveFunction:
    def __init__(self):
        self.n = 401
        self.deltaT = 0.00005
        self.omega = 100 * math.pi
        self.alpha = 2.0 * math.pi / 3.0
        self.wsp = math.sin(7.5 * math.pi / 180.0) / math.sin(52.5 * math.pi / 180.0)
        self.uabc = np.zeros((self.n, 3), dtype=np.float64)

        self.generuj_napiecie_sieci2([100.0, 100.0, 100.0, 1.5, 2.3, 1.2, 2.2, 0.5, 1.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

        self.t12 = Transformer12(self.n)
        self.t12.R = 15
        self.u = np.zeros((6, self.n), dtype=np.float64)
        self.t = 0
        for i in range(self.n):
            self.u[0, i] = self.uabc[i][0]
            self.u[1, i] = self.uabc[i][1]
            self.u[2, i] = self.uabc[i][2]
            self.u[3, i] = self.u[0, i] / math.sqrt(3.0)
            self.u[4, i] = self.u[1, i] / math.sqrt(3.0)
            self.u[5, i] = self.u[2, i] / math.sqrt(3.0)
            self.t += self.deltaT
        np.set_printoptions(precision=16)


        a = np.array([0.5, 0.5, 0.5])
        b = np.array([1.5, 1.5, 1.5])

        self.funkcja_celu = FunkcjaCelu12(self.u, 401, self.t12, self.deltaT)

    def generuj_napiecie_sieci2(self, param):
        t = 0.0
        for i in range(self.n):
            self.uabc[i][0] = param[0] * math.sin(self.omega * t) + \
                               param[3] * math.sin(2 * (self.omega * t + param[9])) + \
                               param[4] * math.sin(3 * (self.omega * t + param[10])) + \
                               param[5] * math.sin(5 * (self.omega * t + param[11])) + \
                               param[6] * math.sin(7 * (self.omega * t + param[12])) + \
                               param[7] * math.sin(11 * (self.omega * t + param[13])) + \
                               param[8] * math.sin(13 * (self.omega * t + param[14]))

            self.uabc[i][1] = param[1] * math.sin(self.omega * t + self.alpha) + \
                               param[3] * math.sin(2 * (self.omega * t + param[9])) + \
                               param[4] * math.sin(3 * (self.omega * t + param[10])) + \
                               param[5] * math.sin(5 * (self.omega * t + param[11] + self.alpha)) + \
                               param[6] * math.sin(7 * (self.omega * t + param[12] + self.alpha)) + \
                               param[7] * math.sin(11 * (self.omega * t + param[13] + self.alpha)) + \
                               param[8] * math.sin(13 * (self.omega * t + param[14] + self.alpha))

            self.uabc[i][2] = param[2] * math.sin(self.omega * t + 2.0 * self.alpha) + \
                               param[3] * math.sin(2 * (self.omega * t + param[9])) + \
                               param[4] * math.sin(3 * (self.omega * t + param[10])) + \
                               param[5] * math.sin(5 * (self.omega * t + param[11] + 2.0 * self.alpha)) + \
                               param[6] * math.sin(7 * (self.omega * t + param[12] + 2.0 * self.alpha)) + \
                               param[7] * math.sin(11 * (self.omega * t + param[13] + 2.0 * self.alpha)) + \
                               param[8] * math.sin(13 * (self.omega * t + param[14] + 2.0 * self.alpha))
            t += self.deltaT


def __main__(x):
    of = ObjectiveFunction()
    Y = of.funkcja_celu.wartosc_param(x)
    return Y
