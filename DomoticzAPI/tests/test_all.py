import test_api
import test_utilities

WIDTH_LABEL = 30
WIDTH_FULL = 80

H1 = "*"
H2 = "-"
SUFFIX = "."
CRLF =  "\r"

FILE = "{:{}<{}}".format(H1, H1, WIDTH_FULL)
TEST = "{:{}<{}}".format(H2, H2, WIDTH_FULL)

if __name__ == '__main__':
    test_api.main()
    test_utilities.main()
