err = {
    'ValueError' : 'O numero deve ser numerico',
    'IndexError' : 'Este index nao existe'
}


def soma():
    loop = True
    error = {}
    while loop:
        try:
            a = int(input('A : ') or 0)
            b = int(input('B : ') or 0)
            loop = False
            return a + b
        except Exception as e:
            error_name = e.__class__.__name__
            if error_name in err.keys():
                print(err[error_name])

print(soma())