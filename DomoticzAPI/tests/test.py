import DomoticzAPI as dom

def main():
    print("********************************************************************************")
    s = dom.Server("192.168.0.16")
    print(s)
    d1 = dom.Device(s, 82)
    print(d1)

if __name__ == "__main__":
    main()
