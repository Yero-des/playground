from django.shortcuts import render
from django.http import HttpResponseNotFound


calculator_symbols = [
    ('+', "Sumatory"), 
    ('-', "Substraction"), 
    ('*', "Multiplication"), 
    ('/', "Division")
]

# Create your views here
def calculator(request, symbol, num1, num2):
    
    result = 0
    operation = ''
    
    if symbol in [s for s, _ in calculator_symbols]:
        if symbol == calculator_symbols[0][0]:
            result = num1 + num2
            operation = calculator_symbols[0][1]
        elif symbol == calculator_symbols[1][0]:
            result = num1 - num2
            operation = calculator_symbols[1][1]
        elif symbol == calculator_symbols[2][0]:
            result = num1 * num2
            operation = calculator_symbols[2][1]
        elif symbol == calculator_symbols[3][0]:
            result = num1 / num2
            operation = calculator_symbols[3][1]
        else: 
            return HttpResponseNotFound("No se ha encontrado la ruta solicitada")
           
        context = {
            "symbol": symbol,
            "num1": num1,
            "num2": num2,
            "operation": operation,
            "result": result,
        } 
        
        return render(request, 'calculator/calculator.html', context)
                
    else:
        return HttpResponseNotFound("No se ha encontrado la ruta solicitada")