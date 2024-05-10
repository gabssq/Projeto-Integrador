import mysql.connector

mydb = mysql.connector.connect(
host = "127.0.0.1", 
user = "root",
password ="gabiru04",
database ="pj" 
)
mycursor = mydb.cursor()

def umTexto (solicitacao, mensagem, valido): # printa mensagens e verifica validez de digitação
    digitouDireito=False
    while not digitouDireito:
        txt = input(solicitacao)

        if txt not in valido:
            print(mensagem, '- Favor redigitar...')
        else:
            digitouDireito=True

    return txt
          
def opcaoEscolhida (mnu): # menu 
  print ()

  opcoesValidas=[]
  posicao=0
  while posicao<len(mnu):
      print (posicao+1,') ',mnu[posicao],sep='')
      opcoesValidas.append(str(posicao+1))
      posicao+=1
  return umTexto('Qual é a sua opção? ', 'Opção inválida', opcoesValidas)

def listar():
  consulta_sql = "select * from produto" # nome da tabela
  mycursor.execute(consulta_sql)
  linhas = mycursor.fetchall() 
  for linha in linhas:
      cp = float(linha[3])
      cf = float("{:.2f}".format(linha[4]/100))
      cv = float("{:.2f}".format(linha[5]/100))
      iv = float("{:.2f}".format(linha[6]/100))
      ml = float("{:.2f}".format(linha[7]/100))
      try:
        pv= float("{:.2f}".format(cp / (1-(cf + cv + iv + ml))))
      except ZeroDivisionError:
        print(f"Valores inválidos para calcular o preço de venda do produto {linha[1], linha[2]}")
      else:
        pvP = 100
        cpP = round(cp / pv * 100)
        cfV = float("{:.2f}".format(cf * pv))
        cvV = float("{:.2f}".format(cv * pv))
        ivV = float("{:.2f}".format(iv * pv))
        receita_bruta_V = round(pv - cp ,2) 
        receita_bruta_P = pvP - cpP
        cfP = cf * 100
        cvP = cv * 100
        ivP = iv * 100
        outros_custos_V = round(cfV + cvV + ivV ,2)
        outros_custos_P = round((cf + iv + cv) * 100)
        rent_V = round((receita_bruta_V) - (outros_custos_V))
        rent_P = (receita_bruta_P) - (outros_custos_P)
        print(f"Código: {linha[0]}")
        print(f"Nome: {linha[1]}")
        print(f"Descrição: {linha[2]}")
        print(f"A. Preço de venda R${pv}   {pvP}%")
        print(f"B. Custo do produto R${cp}   {cpP}%")
        print(f"C. Receita Bruta (A-B) R${receita_bruta_V}   {receita_bruta_P}%")
        print(f"D. Custo Fixo/Administrativo R${cfV}   {cfP}%")
        print(f"E. Comissão de Vendas  R${cvV}   {cvP}%")
        print(f"F. Impostos sobre venda R${ivV}   {ivP}%")
        print(f"G. Outros custos(D+E+F), R${outros_custos_V}   {outros_custos_P}%")
        print(f"H. Rentabilidade (C-G) R${rent_V}  {rent_P}%") 
        print()
        if rent_P > 20:
            print("O lucro obtido é alto!")
        elif rent_P > 10:
            print("O lucro obtido é médio!")
        elif rent_P > 0:
            print("O lucro obtido é baixo!")
        elif rent_P == 0:
            print("Não houve lucro!")
        elif rent_P < 0:
            print("Houve pejuízo!")
        print()

def inserir():
  ml=-1
  while ml<=0:
    try:
      cod = int(input("Digite o código do produto:  "))
      nome = input("Digite o nome do produto:  ")
      descricao = input("Digite a descrição do produto:  ")
      cp = float(input("Digite o custo do produto em reais:  "))
      cf = int(input("Digite o custo fixo do produto em porcentagem:  "))
      cv = int(input("Digite a comissão de vendas do produto em porcentagem:  "))
      iv = int(input("Digite o imposto sobre venda do produto em porcentagem :  "))
      ml = int(input("Digite a margem de lucro do produto em porcentagem :  "))
    except ValueError:
      print("Digite somente números!")

  insert_sql = "INSERT INTO produto (cod, nome, descricao, cp, cf, cv, iv, ml) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
  values = (cod,nome,descricao,cp,cf,cv,iv,ml)
  mycursor.execute(insert_sql, values)
  mydb.commit()
  print(values, "foi inserido com sucesso")
        
def alterar():
  menu_alterar=['Alterar código', \
                'Alterar nome', \
                'Alterar descrição', \
                'Alterar custo do produto', \
                'Alterar custo fixo', \
                'Alterar comissão de vendas', \
                'Alterar imposto sobre venda', \
                'Alterar margem de lucro', \
                'Voltar']
  try:
      cod = int(input("Digite o código do produto que deseja alterar: ")) 
      consulta_sql = "SELECT * FROM produto WHERE cod = %s"
      mycursor.execute(consulta_sql, (cod,))
      produto = mycursor.fetchone()
      if produto is None:
        print("Produto não encontrado")
        return
      else:
        while True:
          escolha = int(opcaoEscolhida(menu_alterar)) 
          if escolha == 1:
            new_cod = int(input("Digite o novo código do produto: ")) 
            query = "UPDATE produto SET cod = %s WHERE cod = %s"
            values = (new_cod, cod)
            mycursor.execute(query, values)
            mydb.commit()
            print("Alterado com sucesso!")
          if escolha == 2:
            new_nome = input("Digite o novo nome do produto: ")
            query = "UPDATE produto SET nome = %s WHERE cod = %s"
            values = (new_nome, cod)
            mycursor.execute(query, values)
            mydb.commit()
            print("Alterado com sucesso!")
          if escolha == 3:
            new_desc = input("Digite a nova descrição do produto: ")
            query = "UPDATE produto SET descricao = %s WHERE cod = %s"
            values = (new_desc, cod)
            mycursor.execute(query, values)
            mydb.commit()
            print("Alterado com sucesso!")
          if escolha == 4:
            new_cp = float(input("Digite o novo custo do produto: "))
            query = "UPDATE produto SET cp = %s WHERE cod = %s"
            values = (new_cp, cod)
            mycursor.execute(query, values)
            mydb.commit()
            print("Alterado com sucesso!")
          if escolha == 5:
            new_cf = int(input("Digite o novo custo fixo do produto: "))
            query = "UPDATE produto SET cf = %s WHERE cod = %s"
            values = (new_cf, cod)
            mycursor.execute(query, values)
            mydb.commit()
            print("Alterado com sucesso!") 
          if escolha == 6:
            new_cv = int(input("Digite a nova comissão de vendas do produto: "))
            query = "UPDATE produto SET cv = %s WHERE cod = %s"
            values = (new_cv, cod)
            mycursor.execute(query, values)
            mydb.commit()
            print("Alterado com sucesso!")     
          if escolha == 7:
            new_iv = int(input("Digite o novo imposto sobre venda do produto: "))
            query = "UPDATE produto SET iv = %s WHERE cod = %s"
            values = (new_iv, cod)
            mycursor.execute(query, values)
            mydb.commit()
            print("Alterado com sucesso!") 
          if escolha == 8:
            new_ml = int(input("Digite a nova margem de lucro do produto: "))
            query = "UPDATE produto SET ml = %s WHERE cod = %s"
            values = (new_ml, cod)
            mycursor.execute(query, values)
            mydb.commit()
            print("Alterado com sucesso!") 
          if escolha == 9:
            return
  except ValueError:
    print("Digite somente números")  

  

def excluir():
  try:
    cod = -1
    while cod < 0:
      cod = int(input("Digite o código do produto que deseja excluir: ")) 
      consulta_sql = "SELECT * FROM produto WHERE cod = %s"
      mycursor.execute(consulta_sql, (cod,))
      produto = mycursor.fetchone()
      if produto is None:
        print("Produto não encontrado")
        return
      else:
        query = "DELETE from produto WHERE cod = %s"
        values = cod 
        mycursor.execute(query, (values,))
        mydb.commit()
        print("Deletado com sucesso!")
  except ValueError:
    print("Digite somente números!")
    
          

   
# programa 
escolha = 69
menu=['Inserir produto',\
      'Alterar produto',\
      'Excluir produto',\
      'Listar produtos',\
      'Sair do Programa']

while escolha != 5:
  escolha = int(opcaoEscolhida(menu)) 
  if escolha == 1:
    inserir()
  if escolha == 2:
    alterar()
  if escolha == 3:
    excluir()
  if escolha == 4:
    listar()

print('OBRIGADO POR USAR ESTE PROGRAMA!')
            
      
