    frequencias_id = [xf[i] for i in index]
    
    f_1 = 0
    f_2 = 0
    for i in range(len(frequencias_id)):
        frequencia = frequencias_id[i]
        amplitude = yf[i]
        Amaior1 = 0
        Amaior2 = 0
        if (650 < frequencia < 950) and (amplitude > Amaior1):
            Amaior1 = amplitude
            f_1 = frequencia
        elif (1000 <= frequencia < 1500) and (amplitude > Amaior2):
            Amaior2 = amplitude
            f_2 = frequencia
    
    print(f"f_1 = {f_1} e f_2 = {f_2}")

    for frequencias in numeros:
        if (f_1-erro <= frequencias[0] <= f_1+erro) and (f_2-erro <= frequencias[1] <= f_2+erro):
            print("Pelo máximo:")
            print(f"Número identificado: {numeros.index(frequencias)}")