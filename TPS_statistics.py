import itertools
import matplotlib.pyplot as plt
import numpy as np
import xlsxwriter

# Calcula a nota de uma possibilidade de marcação
# Os elementos do vetor 'responses' apenas indicam se o usuário acertou ou não a questão
# True não significa necessariamente certo, nem False significa necessariamente errado 
def calculate_score(responses, score_true, score_false):
    score = 0

    for response in responses:
        if response == True:
            score += score_true
        else:
            score += score_false

    return score

# Função auxiliar para calcular armazenar quantas vezes uma
# determinado pontuação se repete
def update_score_info(score_list, score):

    new_score = True

    for score_info in score_list:
        if score_info[0] == score:
            new_score = False
            score_info[1] += 1

    if (new_score == True):
        score_list.append([score, 1])

# Função auxiliar para plotar o gráfico estatístico para determinado
# número 'n' de itens
def plot_graph(x, y, title):
    x = np.array([score_info[0] for score_info in possible_scores]) # pontuações
    y = np.array([score_info[1]/n_possibilities for score_info in possible_scores]) # probabilidade teórica de se obter determinada pontuação
    plt.plot(x, y, 'o')
    plt.axvline(x=0, color='r', linestyle='--', label='Pontuação igual a 0')
    plt.fill_between(x, y, where=(x >= 0), color='skyblue', alpha=0.5, label="Pontuação não negativa")
    plt.xlabel("Pontuação")
    plt.ylabel("Probabilidade de se obter uma pontuação")
    plt.title(title)
    plt.legend()
    plt.show()

# Função auxiliar para salvar os dados em uma planilha
def save(number_of_items, scores, probabilities):

    workbook = xlsxwriter.Workbook("statistics_for_" + str(number_of_items) + "_items.xlsx")
    worksheet = workbook.add_worksheet()

    worksheet.write('A1', 'Score')
    worksheet.write('B1', 'Theoretical probability')

    line = 2
    for i in range(0, len(scores)):
        worksheet.write('A'+str(line), scores[i])
        worksheet.write('B'+str(line), probabilities[i])
        
        line += 1

    workbook.close()
    


score_true = 0.25
score_false = -0.125
set = [True, False]

table_of_probabilities = []

for i in range(1, 25):
    number_of_items = i

    possibilities = list(itertools.product(set, repeat=number_of_items))

    count = 0
    possible_scores = []
    for possibility in possibilities:
        score = calculate_score(possibility, score_true, score_false)

        update_score_info(possible_scores, score)

        if score >= 0:
            count += 1


    n_possibilities = 2 ** number_of_items

    table_of_probabilities.append([number_of_items, count/n_possibilities])

    print("n = ", i)
    print(possible_scores)
    print("Probabilidade teórica de ter uma pontuação maior ou igual a zero: " + str(count/n_possibilities) + '\n')

    x = np.array([score_info[0] for score_info in possible_scores]) # scores
    y = np.array([score_info[1]/n_possibilities for score_info in possible_scores]) # theoretical probability to get a score
    #plot_graph(x, y, "Chute em 24 itens")
    save(number_of_items, x, y)




# Planilha que sintetiza as informações
workbook = xlsxwriter.Workbook("summary.xlsx")
worksheet = workbook.add_worksheet()

worksheet.write('A1', 'Number of items')
worksheet.write('B1', 'Theoretical probability')

line = 2
for i in range(0, len(table_of_probabilities)):
    worksheet.write('A'+str(line), table_of_probabilities[i][0])
    worksheet.write('B'+str(line), table_of_probabilities[i][1])
    
    line += 1

workbook.close()