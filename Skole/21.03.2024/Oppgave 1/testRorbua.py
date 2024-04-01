import gjest, rorbu

gjest_class = gjest.Gjest()
rorbu_class = rorbu.Rorbu()

def main():
    a = 0

    while a <= 100:
        rorbu_class.leggTilGjest(gjest_class)
        a += 1
    rorbu_class.fortellVits(200)
    print(rorbu_class.hvorMorsomtHarViDet())
    rorbu_class.fortellVits(1000)
    print(rorbu_class.hvorMorsomtHarViDet())

if __name__ == "__main__":
    main()