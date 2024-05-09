from tabulate import tabulate
while True:
    nome= input("Digite o nome do produto: ")
    if not nome.isalpha():
        print("Digite somente letras!")
    else:
        variaveis= True
        while variaveis:
            try:
                ml=float(input("Insira a margem de lucro do produto: "))
                cp=float(input("Insira o custo do produto: "))
                cf=float(input("Insira o custo fixo/adminstrativo do produto: "))
                cv=float(input("Insira a comissão de Vendas   do produto: "))
                iv=float(input("Insira os impostos (sobre venda)  do produto: "))

            except ValueError:
                print("Somente valores NÚMERICOS!")
            else:
                variaveis= False
                ml= float("{:.2f}".format(ml/100))
                cf= float("{:.2f}".format(cf/100))
                cv= float("{:.2f}".format(cv/100))
                iv= float("{:.2f}".format(iv/100))
                pv= float("{:.2f}".format(cp/(1-(cf+cv+iv+ml))))
                pvP= 100
                cpP= round(cp/pv*100)
                cfV= float("{:.2f}".format(cf*pv))
                cvV= float("{:.2f}".format(cv*pv))
                ivV= float("{:.2f}".format(iv*pv))
                receita_bruta_V= round(pv-cp,2) 
                receita_bruta_P=pvP-cpP
                cfP=cf*100
                cvP=cv*100
                ivP=iv*100
                outros_custos_V=round(cfV+cvV+ivV,2)
                outros_custos_P=round((cf+iv+cv)*100)
                rent_V=(receita_bruta_V)-(outros_custos_V)
                rent_P=(receita_bruta_P)-(outros_custos_P)

            dados = [
                        [nome, "Valor", " %",],
                        ["A. Preço de venda", pv, pvP],
                        ["B. Custo do produto", cp, cpP],
                        ["C. Receita Bruta (A-B)", receita_bruta_V, receita_bruta_P],
                        ["D. Custo Fixo/Administrativo", cfV, cfP],
                        ["E. Comissão de Vendas ", cvV, cvP],
                        ["F. Impostos sobre venda", ivV, ivP],
                        ["G. Outros custos(D+E+F)", outros_custos_V, outros_custos_P],
                        ["H. Rentabilidade (C-G)", rent_V, rent_P]
                            ]
            tabela = tabulate(dados, headers="firstrow", tablefmt="fancy_grid")
            print (tabela)

            print("\n\n\n\n")

            dados = [
                ["Classificação", "Lucro"],
                ["Alto", ">20%"],
                ["Médio", ">10-20%"],
                ["Baixo", ">0-10%"],
                ["Equlíbrio", "=0"],
                ["Prejuízo", "<0%"]
                ]
            nome= ["Tabela de lucros", ""]
            tabela = tabulate(dados, headers=  nome, tablefmt="fancy_grid")
            print(tabela)

            if rent_P>20:
                print("O lucro obtido é alto!")
            elif rent_P>10:
                print("O lucro obtido é médio!")
            elif rent_P>0:
                print("O lucro obtido é baixo!")
            elif rent_P==0:
                print("Não houve lucro!")
            elif rent_P<0:
                print("Houve pejuízo!")


