# Clasificacion Ordinal
# Python 3.7.0
# UTF-8

# Librerias que se deben instalar de antemano:
from tabulate import tabulate # Libreria tabulate [pip install tabulate]
from PIL import ImageFont # Libreria PIL (Pillow) [pip install Pillow]
from PIL import ImageDraw
from PIL import Image

# Librerias que vienen con Python:
from itertools import combinations, permutations
from operator import itemgetter
from fractions import Fraction
from decimal import Decimal
import codecs
import math
import re

def pixel_scanner(alphabet, language):
    """Es necesario instalar la fuente Arial Unicode
    Para poder visualizar caracteres de todos los idiomas.
    """
    t, total = 0, 0
    for character, frequency in alphabet.items():
        font = ImageFont.truetype("ARIALUNI.TTF", 12)
        img = Image.new("RGB", (30, 30), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.text((10, 7), u"{}".format(character), (0,0,0), font=font)
        img.save(f"dataset/imgs/{language}/{t}.png")
        image = Image.open(f"dataset/imgs/{language}/{t}.png")
        pixels = list(image.getdata())
        width, height = image.size
        pixels = [pixels [i * width:(i + 1) * width] for i in range(height)]
        count = 0
        for pixel in pixels:
            for rgb in pixel:
                if all(color is 255 for color in rgb):
                    pass
                else:
                    current_pixel = (int(rgb[0] * Decimal(f"{0.2126}") + rgb[1] * Decimal(f"{.7152}") + rgb[2] * Decimal(f"{0.0722}")))
                    if current_pixel <= 150:
                        count += 1
                        
        total += (count * frequency)
        t += 1

    return total

def ordinal_asignment(*data):
    # Longitud total de caracteres en un libro.
    var1_ranges = (range(0, 1000000 + 1),
                   range(1000000, 1200000 + 1),
                   range(1200000, 1500000 + 1))
    # Cantidad de pixeles total para la impresion de todos los caracteres.
    var2_ranges = (range(0, 18000000 + 1),
                   range(18000000, 20000000 + 1),
                   range(20000000, 22000000 + 1),
                   range(22000000, 28000000))
    # Agrupacion para evaluarlos por pares.
    var_ranges = [var1_ranges, var2_ranges]
    new_variables = list()
    for raw_data, ranges in zip(data, var_ranges):
        temp_var = []
        for element in raw_data:
            for i, each in enumerate(ranges):
                if element in each:
                    temp_var.append(i+1)
                    break
                
        new_variables.append(temp_var)
        
    return new_variables

def get_info(path):
    data = dict()
    with open(f"dataset/txt/{path}.txt", "r", encoding='utf-8-sig') as f:
        file = f.read()
        file = re.sub(r"\s+", "", file, flags=re.UNICODE)
        for character in file:
            if character not in data:
                data[character] = 1
            else:
                data[character] += 1
                
    return len(file), pixel_scanner(data, path)#, len(data)

def ranking_entropy(var, upwards=True):
    universe = len(var)
    ranking_entropy = 0
    for element in var:
        num_of_elements = 0
        for subelement in var:
            if upwards:
                if element <= subelement:
                    num_of_elements += 1
            else:
                if element >= subelement:
                    num_of_elements += 1
                    
        ranking_entropy -= Fraction(f"1/{universe}") * math.log2(Fraction(f"{num_of_elements}/{universe}"))

    return round(float(ranking_entropy), 4)

# Similar pero ahora se comparan los elementos (A>=) y (B>=) y se usa la interseccion en ellos
def ranking_joint_entropy(var1, var2, upwards=True):
    universe = len(var1)
    ranking_entropy = 0
    for element1, element2 in zip(var1, var2):
        arr1 = []
        arr2 = []
        for i, subelement1 in enumerate(var1):
            if upwards:
                if element1 <= subelement1:
                    arr1.append(i)
            else:
                if element1 >= subelement1:
                    arr1.append(i)

        for i, subelement2 in enumerate(var2):
            if upwards:
                if element2 <= subelement2:
                    arr2.append(i)
            else:
                if element2 >= subelement2:
                    arr2.append(i)
        
        intersection = len(list(set(arr1) & set(arr2)))
        ranking_entropy -= Fraction(f"1/{universe}") * math.log2(Fraction(f"{intersection}/{universe}"))

    return round(float(ranking_entropy), 4)

# Igual pero se divide entre la cantidad de elementos (B>=) en lugar del universo
def ranking_conditional_entropy(var1, var2, upwards=True):
    universe = len(var1)
    ranking_entropy = 0
    for element1, element2 in zip(var1, var2):
        arr1 = []
        arr2 = []
        
        for i, subelement1 in enumerate(var1):
            if upwards:
                if element1 <= subelement1:
                    arr1.append(i)
            else:
                if element1 >= subelement1:
                    arr1.append(i)

        for i, subelement2 in enumerate(var2):
            if upwards:
                if element2 <= subelement2:
                    arr2.append(i)
            else:
                if element2 >= subelement2:
                    arr2.append(i)

        
        intersection = len(list(set(arr1) & set(arr2)))
        
        ranking_entropy -= Fraction(f"1/{universe}") * math.log2(Fraction(f"{intersection}/{len(arr2)}"))

    return round(float(ranking_entropy), 4)

def ranking_mutual_information(var1, var2, upwards=True):
    universe = len(var1)
    ranking_mutual_info = 0
    for element1, element2 in zip(var1, var2):
        arr1 = []
        arr2 = []
        
        for i, subelement1 in enumerate(var1):
            if upwards:
                if element1 <= subelement1:
                    arr1.append(i)
            else:
                if element1 >= subelement1:
                    arr1.append(i)

        for i, subelement2 in enumerate(var2):
            if upwards:
                if element2 <= subelement2:
                    arr2.append(i)
            else:
                if element2 >= subelement2:
                    arr2.append(i)
        
        intersection = len(list(set(arr1) & set(arr2)))
        ranking_mutual_info -= Fraction(f"1/{universe}") * math.log2((Fraction(f"{len(arr1)}")*Fraction(f"{len(arr2)}")) /
                                                                     (Fraction(f"{universe}")*Fraction(f"{intersection}")))

    return round(float(ranking_mutual_info), 4)

def decision_making(variables):
    ranges = [range(0, 3), range(3, 6), range(5, 8)]
    decision_list = []
    for var1, var2 in zip(variables[0], variables[1]):
        total = var1 + var2
        for i, rng in enumerate(ranges):
            if total in rng:
                decision_list.append(i+1)
                break

    return [variables[0], variables[1], decision_list]
        
         
def main(lang, abrev):
    print("Ordinal Classification.\n")
    print("Processing data...\n")
    # Obtencion de informacion.
    var1, var2 = [], []
    for language in lang:
        print(f"{language}:", end=' ')
        data = get_info(f'{language}')
        print("Ready")
        var1.append(data[0])
        var2.append(data[1])
        #var3.append(data[2])
        #u_ranking_entropy = ranking_entropy(data[0], True)
        #d_ranking_entropy = ranking_entropy(data[0], False))

    upwards = True
    rtype = 'Upwards' if upwards else 'Downwards'
    names = ('a1','a2','D')

    print("\nRaw data table:\n")
    print(tabulate(list(zip(abrev, var1, var2)), headers=['lang','str_length','pixel_size']))

    # Aqui inician las formulas para version normal.

    print("\nOrdinal Data table:\n")
    ordinal_variables = ordinal_asignment(var1, var2)
    ordinal_variables = decision_making(ordinal_variables)
    
    print(tabulate(ordinal_variables, headers=abrev))

    print(f"\n{rtype} ranking entropy:\n")
    for name, var in zip(names, ordinal_variables):
        print(f"RH[{rtype}]({name}) = {ranking_entropy(var, upwards)}.")

    print(f"\n{rtype} ranking joint entropy:\n")
    for name, joint in zip(combinations(names, 2), combinations(ordinal_variables, 2)):
        print(f"RH[{rtype}]({name[0]}∪{name[1]}) = {ranking_joint_entropy(joint[0], joint[1], True)}")

    print(f"\n{rtype} ranking conditional entropy:\n")
    for name, joint in zip(permutations(names, 2), permutations(ordinal_variables, 2)):
        print(f"RH[{rtype}]({name[0]}|{name[1]}) = {ranking_conditional_entropy(joint[0], joint[1], True)}")

    print(f"\n{rtype} ranking mutual information:\n")
    for name, joint in zip(combinations(names, 2), combinations(ordinal_variables, 2)):
        print(f"RMI[{rtype}](({name[0]}),{name[1]}) = {ranking_mutual_information(joint[0], joint[1], True)}")

    upwards = False
    rtype = 'Upwards' if upwards else 'Downwards'

    print(f"\n{rtype} ranking entropy:\n")
    for name, var in zip(names, ordinal_variables):
        print(f"RH[{rtype}]({name}) = {ranking_entropy(var, upwards)}.")

    print(f"\n{rtype} ranking joint entropy:\n")
    for name, joint in zip(combinations(names, 2), combinations(ordinal_variables, 2)):
        print(f"RH[{rtype}]({name[0]}∪{name[1]}) = {ranking_joint_entropy(joint[0], joint[1], True)}")

    print(f"\n{rtype} ranking conditional entropy:\n")
    for name, joint in zip(permutations(names, 2), permutations(ordinal_variables, 2)):
        print(f"RH[{rtype}]({name[0]}|{name[1]}) = {ranking_conditional_entropy(joint[0], joint[1], True)}")

    print(f"\n{rtype} ranking mutual information:\n")
    for name, joint in zip(combinations(names, 2), combinations(ordinal_variables, 2)):
        print(f"RMI[{rtype}](({name[0]}),{name[1]}) = {ranking_mutual_information(joint[0], joint[1], True)}")


if __name__ == '__main__':
    lang = ['afrikaans','chinese','danish','dutch','english','finnish','french',
            'german','haitian','icelandic','italian','korean','norwegian',
            'portuguese','russian','serbian','slovak','spanish','swedish','tagalog']

    abrev = ['AFR','CHI','DAN','DUT','ENG','FIN','FRE','GER','HAT','ICE',
             'ITA','KOR','NOR','POR','RUS','SRP','SLO','SPA','SWE','TGL']
    
    main(lang, abrev)
    input("\nPress [Enter] to exit.")
    
    """
    print("Ordinal Classification.")
    # Ejemplo del libro:
    a1 = [1, 1, 3, 2, 2, 3, 3, 4, 5, 5]
    a2 = [1, 2, 2, 3, 3, 3, 4, 4, 4, 5]
    D = [1, 1, 1, 2, 2, 2, 2, 3, 3, 3]

    ordinal_variables = [a1, a2, D]

    upwards = True

    rtype = 'Upwards' if upwards else 'Downwards'

    abrev = ['x1','x2','x3','x4','x5','x6','x7','x8','x9','x10']

    names = ['a1','a2','D']

    print("\nOrdinal Data table:\n")
    #ordinal_variables = ordinal_asignment(var1, var2)
    #ordinal_variables = decision_making(ordinal_variables)
    
    print(tabulate(ordinal_variables, headers=abrev))

    print(f"\n{rtype} ranking entropy:\n")
    for name, var in zip(names, ordinal_variables):
        print(f"RH[{rtype}]({name}) = {ranking_entropy(var, upwards)}.")
    
    print(f"\n{rtype} ranking joint entropy:\n")
    for name, joint in zip(combinations(names, 2), combinations(ordinal_variables, 2)):
        print(f"RH[{rtype}]({name[0]}∪{name[1]}) = {ranking_joint_entropy(joint[0], joint[1], True)}")

    print(f"\n{rtype} ranking conditional entropy:\n")
    for name, joint in zip(permutations(names, 2), permutations(ordinal_variables, 2)):
        print(f"RH[{rtype}]({name[0]}|{name[1]}) = {ranking_conditional_entropy(joint[0], joint[1], True)}")
        
    print(f"\n{rtype} ranking mutual information:\n")
    for name, joint in zip(combinations(names, 2), combinations(ordinal_variables, 2)):
        print(f"RMI[{rtype}](({name[0]}),{name[1]}) = {ranking_mutual_information(joint[0], joint[1], True)}")
    """

    








