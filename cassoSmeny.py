import os
from datetime import datetime
from collections import namedtuple
from dataclasses import dataclass
import random
import sys
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

weekDays = ["Po", "Ut", "St", "Ct", "Pa", "So", "Ne"]

class chlap:
    def __init__(self, jmeno, volna, posledni, dennich, nocnich, prvniDen, smeny):
        self.weekDays = ["Po", "Ut", "St", "Ct", "Pa", "So", "Ne"]
        self.jmeno = jmeno
        self.volna = volna
        self.posledni = posledni
        self.dennich = int(dennich)
        self.nocnich = int(nocnich)
        self.dennichO = int(dennich)
        self.nocnichO = int(nocnich)
        self.smeny = {}
        self.pocetVolna = len(self.volna)
        self.streak = 0
        self.volnoStreak = 0
        self.vikendu = 0
        self.posledniDenIndex = self.weekDays.index(prvniDen) - 1
        self.posledniDen = self.weekDays[self.posledniDenIndex]
        self.punishPoints = len(self.volna)

    def printInfo(self):
        print(self.jmeno)
        print(self.volna)
        #print(self.posledni)
        #print(self.dennich)y
        
        #print(self.nocnich)
        print(self.smeny)

    def addSmena(self, kdy, jaka):
        self.smeny[kdy] = jaka
        self.posledni = jaka
        if self.posledniDenIndex < 6:
            self.posledniDenIndex += 1
        else:
            self.posledniDenIndex = 0
        
        self.posledniDen = self.weekDays[self.posledniDenIndex]

        if jaka == "D":
            self.dennich -= 1
            self.streak += 1
            if self.streak == 4:
                self.punishPoints -= 3
            self.volnoStreak = 0
        elif jaka == "N":
            self.nocnich -= 1
            self.streak += 1
            if self.streak == 4:
                self.punishPoints -= 3
            self.volnoStreak = 0
        else:
            self.streak = 0
            self.volnoStreak += 1
        if self.punishPoints < 0:
            self.punishPoints = 0

    def getSmeny(self):
        return self.smeny

    def getDennich(self):
        return self.dennichO
    
    def getNocnich(self):
        return self.nocnichO
    
    def getVolna(self):
        return self.volna

    def getLast(self):
        return self.posledni

    def getPocetVolna(self):
        return self.pocetVolna

    def getStreak(self):
        return self.streak

    def getName(self):
        return self.jmeno

    def getLastDay(self):
        return self.weekDays[self.posledniDenIndex]

    def getVolnoStreak(self):
        return self.volnoStreak

    def getPseudo(self, arr, den, dniCelkem):
        sance = (self.dennich, self.nocnich)
        celkem = sance[0] + sance[1]

        zbyva = int(dniCelkem) - int(den) 

        if celkem <= 0:
            return 0

        isDenni = 'D' in arr
        isNocni = 'N' in arr
        nr = len(arr)
        nrVolna = arr.count('')
        if zbyva == 0:
            return 0

        if self.streak >= 2 and '' in arr and float(zbyva / float(celkem)) > 1.25: #+ self.punishPoints
            return 0
        
        kladivo = random.randint(1, zbyva)

        if kladivo > celkem or nr == nrVolna:
            volno = True
        else:
            volno = False

        kladivo2 = random.randint(0, 2)
        if self.getVolnoStreak() != 0 and float(zbyva / float(celkem)) < 1.25:
            if kladivo2 <= self.getVolnoStreak():
                volno = False

        kladivo3 = random.randint(0, 2)
        if self.getStreak() != 0 and float(zbyva / float(celkem)) > 1.25: #+ self.punishPoints
            if kladivo3 <= self.getStreak():
                volno = True

        if nr == nrVolna:
            return 0

        if volno and nrVolna > 0:
            return 0
        else:
            if ((int(den) > 2 and self.getSmeny()[int(den) - 2] == 'N' and self.getSmeny()[int(den) - 1] == '') and (sance[0] + sance[1] - zbyva < 0)):
                if 'N' in arr:
                    return arr.index('N')
                else:
                    return 0
            if isNocni and isDenni:
                rnd = random.randint(1, celkem)
                if rnd < sance[0]:
                    return nrVolna
                else:
                    return nrVolna + 1
            else:
                return nrVolna
    
class chlapi:
    def __init__(self, mInfo):
        self.zamestnanci = []
        self.mInfo = mInfo
        self.initialize()
        self.names = self.getNames()
        self.legal = True
    
    def addChlap(self, chlap):
        self.zamestnanci.append(chlap)
    
    def initialize(self):
        global __location__
        in_smeny = open(os.path.join(__location__, 'in_smeny.txt'), "r")
        in_volna = open(os.path.join(__location__, 'in_volna.txt'), "r")

        for lineS in in_smeny:
            volna = []
            smeny = []
            lineS = lineS.split()
            smeny = lineS[4:]
            for lineV in in_volna:
                lineV = lineV.split()
                if(lineV[0] == lineS[0]):
                    del lineV[0]
                    volna = lineV
                    break
            
            self.addChlap(chlap(lineS[0], volna, lineS[3], lineS[1], lineS[2], self.mInfo.firstDay, smeny))
        in_smeny.close()
        in_volna.close()
    
    def getNames(self):
        names = []
        for zamestnanec in self.zamestnanci:
            names.append(str(zamestnanec.jmeno))

        return names

    def getHead(self, names):
        line = "Datum;Den;"
        for name in names:
            line += str(name) + ';'
        line += '\n'

        return line

    def getChlapi(self):
        return self.zamestnanci

    def rozdelSmeny(self, monthInfo):
        nrArgs = 5

        for i in range(1, int(monthInfo.numberOfDays) + 1):
            if self.legal == False:
                break
            nejvicVolna = []
            free = ['D', 'N']

            for p in range(0, len(self.zamestnanci) - 2):
                free.insert(0, '')

            #zmena poradi v listu podle podminek
            for n in range(0, nrArgs):
                for b, boi in enumerate(self.zamestnanci):
                    args = [(i > 2 and boi.getSmeny()[i - 2] == 'N' and boi.getSmeny()[i - 1] == ''), #nocni do volna do denni
                    ((i == 1 and boi.getLast() == "N") or (i > 1 and boi.getSmeny()[i - 1] == "N")), #nocni do denni
                    (boi.getStreak() == 2), #2 smena
                    (boi.getStreak() == 3), #3 smena
                    (boi.getStreak() == 4)] #4 smena

                    if str(i) in boi.getVolna() and n == 0: #volno
                        boi.addSmena(i, free.pop(0))
                        continue
                    if args[n]:
                        self.zamestnanci = swapPositions(self.zamestnanci, b )

            for boi in self.zamestnanci:
                count = 0
                legal = True
                if i in boi.getSmeny():
                    continue
                while(legal):
                    number = boi.getPseudo(free, i, monthInfo.numberOfDays)

                    if (i == 1 and free[i - 1] == "N" and boi.getLast() == "D") or (i > 1 and free[number] != '' and free[number] == "D" and boi.getSmeny()[i - 1] == "N"):
                        count += 1
                        if count > 10:
                            self.legal = False
                            boi.addSmena(i, free.pop(number))
                            legal = False
                            
                        continue
                    else:
                        boi.addSmena(i, free.pop(number))
                        legal = False
                

    def zapisSnemy(self, mInfo, out):
        first = 0
        global weekDays
        for count, day in enumerate(weekDays):
            if str(day) == str(mInfo.firstDay):
                first = count

        for i in range(1, int(mInfo.numberOfDays) + 1):
            line = str(i) + ';' + str(weekDays[first]) + ';'
            for a, boi in enumerate(self.zamestnanci):
                if a == len(self.zamestnanci) - 1:
                    line += str(boi.getSmeny()[i]) + '\n'
                else:
                    line += str(boi.getSmeny()[i]) + ";"
            out.write(line)
            if first == 6:
                first = 0
            else:    
                first += 1

    def fixOrder(self, OGjmena):
        for i, chlap in enumerate(self.zamestnanci):
            idx = OGjmena.index(chlap.getName())
            tmp = None
            if not idx == i:
                tmp = self.zamestnanci[idx]
                self.zamestnanci[idx] = chlap
                done = False
                while not done:
                    idx = OGjmena.index(tmp.getName())
                    ttmp = self.zamestnanci[idx]
                    self.zamestnanci[idx] = tmp
                    if tmp == ttmp:
                        done = True
                    else:
                        tmp = ttmp

    def getAccuracy(self, b_print):
        daysOff = 0
        DNoff = 0
        times4 = 0
        times3 = 0
        times5 = 0
        streak = 0
        d = 0
        n = 0

        for boi in self.zamestnanci:
            d = 0
            n = 0
            streak = 0
            smeny = boi.getSmeny()
            for smena in smeny:
                if smeny[smena] == "D":
                    d += 1
                    streak += 1
                elif smeny[smena] == "N":
                    n += 1
                    streak += 1
                else:
                    streak = 0
                if streak == 3:
                    times3 += 1
                if streak == 4:
                    times4 += 1
                    times3 -= 1
                if streak == 5:
                    times5 += 1
                    times4 -= 1
            daysOff += abs((boi.getDennich() + boi.getNocnich()) - (d + n))
            DNoff += abs(boi.getDennich() - d) + abs(boi.getNocnich() - n)

        if b_print:
            print("daysOff: " + str(daysOff))
            print("Denni/Nocni Off: " + str(DNoff))
            print("5 smeny: " + str(times5))
            print("4 smeny: " + str(times4))
            print("3 smeny: " + str(times3))

        else:
            return daysOff + DNoff + times5 * 5 + times4 * 2 + times3


@dataclass
class monthInfo:
    firstDay: str
    numberOfDays: int

def getFileName():
    today = datetime.today()
    fileName = str(today.time())
    fileName = fileName.replace(':', '')
    fileName = fileName.replace('.', '')
    fileName += ".csv"
    
    return fileName

def swapPositions(v_list, pos): 
    tmp = v_list[0]
    v_list[0] = v_list[pos]
    
    for i in range(1, pos + 1):
        tmp, v_list[i] = v_list[i], tmp

    return v_list

def swapPositions2(v_list, pos1, pos2):
    v_list[pos1], v_list[pos2] = v_list[pos2], v_list[pos1]

    return v_list

def getMonthInfo():
    in_info = open(os.path.join(__location__, 'in_info.txt'), "r")
    lines = []
    for line in in_info:
        lines.append(line.replace('\n', ''))
    mInfo = monthInfo(lines[0], lines[1])

    in_info.close()
    
    return mInfo

def restart_program():
    input("Nepodarilo se najit smeny s pozadovanou odchylkou. Stiskni Enter a zkus znovu s vetsi odchylkou")
    os._exit(0)


def main():

    legal = False

    maxAcc = int(input("Zadej maximalni povolenou odchylku."))

    best = (0, 100)

    it = int (input("Zadej pocet pruchodu (doporuceno 1):"))

    print('Generuji...')



    for i in range(0, it):
        breaker = 0

        while not legal:

            global __location__

            global weekDays

            mInfo = getMonthInfo()

            zamestnanci = chlapi(mInfo)

            pracovnici = zamestnanci.getChlapi()

            jmena = zamestnanci.getNames()

            zamestnanci.rozdelSmeny(mInfo)

            legal = zamestnanci.legal

            if zamestnanci.getAccuracy(False) > maxAcc:
                legal = False
                breaker += 1
                if breaker > 30000:
                    restart_program()


        acc = zamestnanci.getAccuracy(False)
        if best[1] >= acc:
            best = (zamestnanci, acc)
        legal = False


    print(("Skore: " + str(best[1])))

    fileName = getFileName()

    out_rozpis = open(os.path.join(__location__, fileName), 'a')

    out_rozpis.write(best[0].getHead(jmena)) 

    best[0].fixOrder(jmena)
    
    best[0].zapisSnemy(mInfo, out_rozpis)

    out_rozpis.close()
    
    best[0].getAccuracy(True)

    delete = input("Delete? Y/N")

    if delete == 'Y':
        input("Press Enter")
        os.remove(os.path.join(__location__, fileName))

    
if __name__== "__main__":
  main()

