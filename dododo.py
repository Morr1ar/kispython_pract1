
# 3.5
print('№ 3.5')
def fast_mul(x, y):
    if y == 0:
        return 0
    
    if ((x < 0) & (y > 0)) | ((x > 0) & (y < 0)):
        sign = -1
    else:
        sign = 1
    
    x = abs(x)
    y = abs(y)
    
    result = 0
    
    while y > 0:
        if y & 1:
            result += x

        x <<= 1# Умножение на 2
        y >>= 1# Деление на 2 с отбрасыванием остатка

    assert result * sign == x * y, "Не правильно"
    return result * sign

print(fast_mul(0, 15))

# 3.6
print('№ 3.6')
def fast_pow(a, n):
    if n == 0:
        return 1
    
    if n < 0:
        return 1 / fast_pow(a, -n)
    
    result = 1
    base = a
    power = n
    
    while power > 0:
        # Если текущий бит показателя степени равен 1
        if power & 1:
            result *= base
        
        base *= base
        power >>= 1

    assert result == a ** n, "Не правильно"
    return result

print(fast_pow(4, 6))

# 3.7
print('№ 3.7')
def mul_bits(x, y, bits = 8):
    x &= (2 ** bits - 1)
    y &= (2 ** bits - 1)
    return x * y

def mul16(x, y):
    x0 = x >> 8
    x1 = (x - (x0 << 8))
    y0 = y >> 8
    y1 = (y - (y0 << 8))
    result1 = mul_bits(x1, y1)
    result2 = mul_bits(x0, y1)
    result3 = mul_bits(x1, y0)
    result4 = mul_bits(x0, y0)
    result = (result4 << 16) + ((result2 + result3) << 8) + result1
    assert result == x * y, "Не правильно"
    return result

print(mul16(65535, 65535))
print(mul16(6575, 49525))

# 3.8
print('№ 3.8')
def mul16k(x, y):
    a = x >> 8
    b = (x - (x0 << 8))
    c = y >> 8
    d = (y - (y0 << 8))
    result1 = mul_bits(a, c)
    result2 = mul_bits(b, d)
    result3 = mul_bits(x, y)
    result4 = result3 - result1 - result2
    result = (result1 << 16) + (result4 << 8) + result2
    assert result == x * y, "Не правильно"
    return result

print(mul16(65535, 65535))
print(mul16(6575, 49525))

# 3.9
print('№ 3.9')
def fast_mul_gen(y):
    sign = '-' if y < 0 else ''
    y = abs(y)
    
    print("def f(x):")
    print("    n0 = x")
    
    # Создаем переменные для всех степеней двойки до нужной
    power = 1
    while (1 << power) <= y:
        print(f"    n{power} = n{power-1} + n{power-1}")
        power += 1
    
    # Собираем сумму нужных степеней двойки
    terms = []
    for i in range(power):
        if y & (1 << i):  # если этот бит есть в числе
            terms.append(f"n{i}")
    
    print(f"    result = {' + '.join(terms)}")
    print(f"    result = {sign}result")
    print(f"    assert result == x * numder, 'Не правильно'")
    print(f"    return result")


numder = -32

fast_mul_gen(numder)

def f(x):
    n0 = x
    n1 = n0 + n0
    n2 = n1 + n1
    n3 = n2 + n2
    n4 = n3 + n3
    n5 = n4 + n4
    result = n5
    result = -result
    assert result == x * numder, 'Не правильно'
    return result

print(f(3))


# 4.3
print('№ 4.3')
import math
import tkinter as tk


def draw(shader, width, height):
    image = bytearray((0, 0, 0) * width * height)
    for y in range(height):
        for x in range(width):
            pos = (width * y + x) * 3
            color = shader(x / width, y / height)
            normalized = [max(min(int(c * 255), 255), 0) for c in color]
            image[pos:pos + 3] = normalized
    header = bytes(f'P6\n{width} {height}\n255\n', 'ascii')
    return header + image


def main(shader):
    label = tk.Label()
    img = tk.PhotoImage(data=draw(shader, 256, 256)).zoom(2, 2)
    label.pack()
    label.config(image=img)
    tk.mainloop()


def shader(x, y):
    # Ваш код здесь:
    return x, y, 0 # красный зеленый синий

def shader1(x, y):
    # Ваш код здесь:
    r1 = ((x - 0.5)**2 + (y - 0.5)**2)**0.5
    r2 = ((x - (0.5 + 1 / 9))**2 + (y - (0.5 - 2 / 9))**2)**0.5
    b1 = 1 / 2
    c1 = 1 / 4
    b2 = -1 / 2
    c2 = 3 / 4
    if r1 > (1 / 3):
        return 0, 0, 0 # черный
    else:
        if x > 0.5:
            if (y < b1 * x + c1) & (y > b2 * x + c2):
                return 0, 0, 0
            elif r2 < (1 / 18):
                return 0, 0, 0
    return 1, 1, 0 # желтый


main(shader1)

