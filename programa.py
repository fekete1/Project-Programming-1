'''
imports
'''

from tkinter import *
from functools import partial
from tkinter import messagebox
from datetime import *

'''
Parte lógica do programa
'''

def criptografar(item):
    '''
    Criptografa determinado item usando o metodo RSA
    '''
    
    arquivo = open('chavePublica.txt','r')
    textoCripto=[]
    aux = arquivo.read()                       
    for elemento in aux:
        chaves = aux.split()

    e = int(chaves[0])
    n = int(chaves[1])

    y = (ord(item) ** e) % n
    return y


def decriptar(y):
    '''
    Decripta determinado item usando o metodo RSA
    '''
    
    arquivo = open('chavePrivada.txt','r')
    texto=''
    aux = arquivo.read()
    arquivo.close()
    chaves = aux.split()

    arquivo.close()
    d = int(chaves[0])
    n = int(chaves[1])
    x = chr((y**d) % n)
    return x

def ler_usuarios():
    '''
    Executa uma varredura no arquivo criptografado de usuários para ler todos os cadastros
    '''

    arquivo = open('usuarios.txt','r')
    conteudo = arquivo.readlines()
    listaUsuario = []
    usuarios = []
    for user in conteudo:
        aux = ''    #Aux faz papel de cada letra criptografada
        palavra = ''
        for letra in user:
            if letra == ' ':
                itemDecript = decriptar(int(aux))
                palavra += itemDecript
                aux = ''
            elif letra == ';':
                listaUsuario.append(palavra)
                palavra = ''

            elif letra != '\n':
                aux += letra
        usuarios.append(tuple(listaUsuario))
        listaUsuario = []

    arquivo.close()
    bd = {}
    for conta in usuarios:
        bd[conta[0]] = (conta[1],conta[2],conta[3],conta[4],conta[5],conta[6],conta[7])
    return bd

def salvar_usuarios(dicionario):
    '''
    Salva os dados dos usuários em um  arquivo criptografado
    '''

    arquivo = open('usuarios.txt','w')
    string = ''
    for chave in dicionario.keys():
        itemCripto = []
        for letra2 in chave:
            aux = str(criptografar(letra2))
            string += aux + ' '
        itemCripto.append(string)
        for elemento in dicionario[chave]:
            string = ''
            for letra in str(elemento):
                aux = str(criptografar(letra))
                string += aux + ' '
            itemCripto.append(string)
        for data in itemCripto:
            arquivo.write(data + ';')
        arquivo.write('\n')
        string = ''
    arquivo.close()




def abrir_arquivo(nomeArquivo):
    '''
    Abre o arquivo que o usuário passar como parâmetro e o transforma em um dicionário
    '''
    
    arquivo = open(nomeArquivo,'r')
    conteudo = arquivo.readlines()
    arquivo.close
    
    listaAux=[]
    dicionario={}
    
    for elemento in conteudo:
        listaAux.append(elemento.split(';'))
    for elemento in listaAux:
        elemento[-1] = elemento[-1].replace('\n', '')
    for x in listaAux:
        usuario = x[0]
        x.remove(x[0])
        dicionario[usuario] = tuple(x)
    return dicionario



def criar_usuario(login,senha,nick,time,campeao,level,elo):
    '''
    Cria o usuário um novo usuário, adicionando ele no dicionário e depois salvado no arquivo
    '''
    
    db= ler_usuarios()
    elos = ['','Bronze','Prata','Ouro','Platina','Diamante','Mestre','Desafiante']
    elo = elo.capitalize() #torna a primeira letra maiuscula
    time = time.capitalize() #torna a primeira letra maiuscula
    campeao = campeao.capitalize() #torna a primeira letra maiuscula
    
    encontrou=True
    if login == '' or senha == '' or nick == '' or time == '' or campeao =='' or level =='':
        return 0
    else:
        if not elo in elos: #Não aceitará se colocarem um elo que não exista
            return 3
        elif not level.isdigit(): #Não aceitará se colocarem algo que não seja número no level
            return 4
        else:
            for usuario in db:
                if login == usuario: #No caso de já existir o login
                    encontrou=False
                    return 1
            
            if encontrou:
                db[login]=(senha,nick,time,campeao,level,elo,'0')
                salvar_usuarios(db)
                '''
                Salvando no log
                '''
                    
                log = 'cadastro do usuário '+login+'.'

                log_exec(log,'Não identificado')
                return 2

def cargoEmPalavra(cargo):
    '''
    Transforma os cargos dos usuários em algo mais legivel de se apresentar
    '''
    
    if cargo == '0':
        return 'Usuario comum'
    if cargo == '1':
        return 'Moderador'
    return 'Admnistrador'

def filtrarInformacao(usuario):
    '''
    Esta função é basicamente para deixar as informações legiveis caso tenha um campo vazio nas informações do usuario
    '''
    
    if type(usuario) == list:
        login,senha,cargo = usuario[0],usuario[1][0],cargoEmPalavra(usuario[1][6])
        nick = usuario[1][1]
        if usuario[1][2] == '':
            time = 'Não possui'
        else:
            time = usuario[1][2]
        if usuario[1][3] == '':
            campeao = 'Não possui'
        else:
            campeao = usuario[1][3]
        if usuario[1][4] == '':
            level = 'Não possui'
        else:
            level = usuario[1][4]
        if usuario[1][5] == '':
            elo = 'Não possui'
        else:
            elo = usuario[1][5]
        return login,senha,cargo,nick,time,campeao,level,elo
    
def selectionSort(dicio):
    '''
    Algoritmo de ordenação, é passado um dicionário como parametro e ele ordena as chaves por ordem alfabética
    '''
    
    dicioOrdenado = {} 
    listaChaves=[]
    for elemento in dicio.keys(): #Cria uma lista com as chaves do dicionário passado
        listaChaves.append(elemento)
       
    listaOrdenada =[]
    
    while (listaChaves != []):  #Algoritmo de ordenação, selection sort, usando a chave dos dicionários para serem ordenadas
        menor = listaChaves[0]
        for elemento in listaChaves:
            if elemento < menor:
                menor = elemento
        listaOrdenada.append(menor)
        listaChaves.remove(menor)
        
    for item in listaOrdenada: #Atribui o valor do conteudo para o dicionário ordenado do dicionário passado como parametro
        dicioOrdenado[item]=dicio[item] 
        
    return dicioOrdenado


def gerar_relatorio(dicio):
    '''
    Gera um arquivo txt com as informações dos usuarios, que no caso é o elemento do meu programa, com excessão da senha e do cargo
    '''
    
    for usuario in dicio:
        dicio[usuario] = (dicio[usuario][1],dicio[usuario][2],dicio[usuario][3],dicio[usuario][4],dicio[usuario][5])
    arquivo = open('impressaoelementos.txt','w')
    arquivo.write('Login  |  Nickname  |  Time que torce  |  Campeão favorito  |  Level  |  Elo  |\n\n')    
    qtdeDicio = len(dicio)
    cont=0
    for chave in dicio:
        arquivo.write(chave)
        arquivo.write('  :  ')
        qtde = len(dicio[chave])
        cont+=1
        
        aux=0
        for conteudo in dicio[chave]:
            if conteudo == '':
                arquivo.write('Não possui')
                aux+=1
            else:

                arquivo.write(conteudo)
                aux+=1
            
            if aux != qtde:
                arquivo.write('  -  ')
            
 
        if qtdeDicio != cont:
            arquivo.write('\n')


def log_exec(variavel,usuario):
    '''
    Escreve no arquivo log.txt a ação realizada pelo usuário
    '''
    arquivo = open('log.txt','a')

    #obtenção de horários
    now = datetime.now()
    day = str(now.day)
    if len(day) == 1: #Se o dia for apenas uma unidade, ele adiciona o 0 na frente
        day = '0' + day
        
    mes = str(now.month)
    if len(mes) == 1: #Se o Mês for apenas uma unidade, adiciona o 0 na frente
        mes = '0' + mes
        
    hour = str(now.hour) #Se a hora for apenas uma unidade, adiciona o 0 na frente
    if len(hour) == 1:
        hour = '0'+ hour
        
    data = day + '/' + mes + '/' + str(now.year)
    hora = hour + ':' + str(now.minute) + ':' + str(now.second)
 
    
    #escrita no arquivo
    arquivo.write(data)
    arquivo.write(' - ')
    arquivo.write(hora)
    arquivo.write(' - ')
    
    arquivo.write('Executado por: '+usuario)
    arquivo.write(' - ')
    arquivo.write('Ação: '+variavel)
    arquivo.write('\n')
    arquivo.close()

        
'''
Parte da interface do programa
'''

#Constantes
azul = '#1e6a84'
azulNovo = '#1d657c'
verde= '#6a9b99'
cinza= '#33334d'
verdeNovo='#009999'
azulEscuro = '#003756'
vermelho = '#6a0500'
platina = '#183431'

'''
Inicio da interface
'''

class programa():
    def __init__(self):
        self.janelas={}
        self.janelas['janela']=Tk()
        #Interface da janela principal
        self.janelas['janela'].title("A melhor janela de todas")
        self.janelas['janela']['bg']=azul
        #Lado x Altura + Esquerda + Teto
        self.janelas['janela'].geometry('300x400+500+150')
        self.janelas['janela'].resizable(False,False)
        self.janelas['janela'].wm_iconbitmap('lol1.ico')
        


        #Labels de login, senha e etc
        login = Label(self.janelas['janela'],text='Login: ',bg=azul,fg='white')
        senha = Label(self.janelas['janela'],text='Senha: ',bg=azul,fg='white')
        self.textoJanela = Label(self.janelas['janela'],bg=azul)
        logo = Label(self.janelas['janela'],text = 'Login',font= 'verdana 20 bold',bg=azul,fg='white' )
        labelCreditos = Label(self.janelas['janela'],width= 300,bg=verde,text='Copyright(c) 2018 José Sheldon Brito Fekete',font='arial 8')
        
    
        #Buttons entrar e criar
        botentrarJanela = Button(self.janelas['janela'], width= 5,text="Entrar", command = self.entrar,bg=verde,bd=1,fg='white')
        botcriarJanela = Button(self.janelas['janela'], width = 5,text='Criar', command = self.criar,bg=verde,bd=1,fg='white')

        #Entrys de login e senha
        self.entloginJanela = Entry(self.janelas['janela'],width = 22,bg='light blue',bd=0,fg=cinza)
        self.entsenhaJanela = Entry(self.janelas['janela'],width = 22,show='*',bg='light blue',bd=0,fg=cinza)
        
        #empacotando
        logo.place(x=105,y=10)
        login.place(x=50, y=80)
        senha.place(x=50, y= 110)
        self.entloginJanela.place(x=92,y=80)
        self.entsenhaJanela.place(x=92, y=110)
        botentrarJanela.place(x=125,y=150)
        botcriarJanela.place(x=125,y=190)
        labelCreditos.pack(side=BOTTOM)
        self.textoJanela.pack(side=BOTTOM)
        
        self.janelas['janela'].mainloop()
        
    
    def entrar(self):
        '''
        Faz a verificação de login e se o login estiver certo atribui as informações do usuario a variavel self.usuarioLogado 
        '''
        
        bd = ler_usuarios()
        usuario = str(self.entloginJanela.get())
        codigo = str(self.entsenhaJanela.get())
        if codigo =='' or usuario == '': #campos vazios
            self.textoJanela['text']='Campo vazio'
            self.textoJanela['fg']='red'
            messagebox.showerror('ERRO!!!','Você deixou algum campo vazio.')
            
        else:   #Se o usuário existir
            if usuario in bd:
                if bd[usuario][0] == codigo:#Senha válida
                    self.textoJanela['text']='Seja bem vindo \n%s'%(bd[usuario][1])
                    self.textoJanela['fg']='light green'
                    self.usuarioLogado = []
                    self.usuarioLogado.append(usuario)
                    self.usuarioLogado.append(bd[usuario]) #Index 0 é o usuario e o Index 1 é as informações do usuario
                    '''
                    Salvando no log
                    '''
                    
                    log = 'Entrou no programa.'

                    log_exec(log,self.usuarioLogado[0])
                    self.entrarJanela_click()

                    
                else:   #Senha invalida
                    self.textoJanela['text']=('Senha invalida')
                    self.textoJanela['fg']='red'
                    messagebox.showerror('ERRO!!!','Senha informada incorreta.')
                    
                
            else:   #Se o usuário não existir
                self.textoJanela['text']=('Login invalido')
                self.textoJanela['fg']='red'
                messagebox.showerror('ERRO!!!','Login informado não existe.')
                
    def criar(self):
        '''
        cria a janela de cadastro, abrindo a mesmo e fechando a janela de login
        '''

        self.janelas['janela'].withdraw() #Fecha a janela de entrada
        self.janelas['janelaCadastro']=Tk() #Cria a janela de cadastro
        #Interface da janela principal
        self.janelas['janelaCadastro'].title("A melhor janela de todas")
        self.janelas['janelaCadastro']['bg']=azul
        #Lado x Altura + Esquerda + Teto
        self.janelas['janelaCadastro'].geometry('300x400+500+150')
        self.janelas['janelaCadastro'].resizable(False,False)
        self.janelas['janelaCadastro'].wm_iconbitmap('lol1.ico')

        #Labels de login, senha e etc
        login = Label(self.janelas['janelaCadastro'],text='Login',bg=azul,fg='white')
        senha = Label(self.janelas['janelaCadastro'],text='Senha',bg=azul,fg='white')
        nick = Label(self.janelas['janelaCadastro'], text='Nickname',bg=azul, fg='white')
        time = Label(self.janelas['janelaCadastro'], text='Time que torce',bg=azul,fg='white')
        campeao = Label(self.janelas['janelaCadastro'], text='Campeão favorito',bg=azul,fg='white')
        logo = Label(self.janelas['janelaCadastro'],text = 'Cadastro',font= 'verdana 20 bold',bg=azul,fg='white' )
        labelCreditos = Label(self.janelas['janelaCadastro'],width= 300,bg=verde,text='Copyright(c) 2018 José Sheldon Brito Fekete',font='arial 8')        
        self.textoCadastro = Label(self.janelas['janelaCadastro'],bg=azul)
        level = Label(self.janelas['janelaCadastro'], text='Level do invocador',bg=azul,fg='white')
        elo = Label(self.janelas['janelaCadastro'], text='Elo do invocador',bg=azul,fg='white')
        informacao = Label(self.janelas['janelaCadastro'], text='Informações do League of Legends',bg=azul,fg='black')

        #Buttons de voltar e cadastrar
        voltarCadastro = Button(self.janelas['janelaCadastro'],text='Voltar', width= 8,command = self.voltarCadastro_click,bg=verde,bd=1,fg='white')
        cadastrarCadastro = Button(self.janelas['janelaCadastro'], text='Cadastrar', width= 8,command = self.cadastrar_click,bg=verde,bd=1,fg='white')

        #Entrys
        self.entloginCadastro = Entry(self.janelas['janelaCadastro'],bg='light blue',bd=0,fg=cinza)
        self.entsenhaCadastro = Entry(self.janelas['janelaCadastro'],show='*',bg='light blue',bd=0,fg=cinza)
        self.entnick = Entry(self.janelas['janelaCadastro'],bg='light blue',bd=0,fg=cinza)
        self.enttime = Entry(self.janelas['janelaCadastro'],bg='light blue',bd=0,fg=cinza)
        self.entcampeao = Entry(self.janelas['janelaCadastro'],bg='light blue',bd=0,fg=cinza)
        self.entlevel = Entry(self.janelas['janelaCadastro'],bg='light blue',bd=0,fg=cinza)
        self.entelo = Entry(self.janelas['janelaCadastro'],bg='light blue',bd=0,fg=cinza)
        

        #Empacotamento
        logo.place(x=75,y=10)
        login.place(x=125,y=60)
        self.entloginCadastro.place(x=85,y=80)
        senha.place(x=125,y=100)
        self.entsenhaCadastro.place(x=85,y=120)
        informacao.place(x=50,y=140)
        nick.place(x=115,y=160)
        self.entnick.place(x=85,y=180)
        time.place(x=105,y=200)
        self.enttime.place(x=85,y=220)
        campeao.place(x=95,y=240)
        self.entcampeao.place(x=85,y=260)
        level.place(x=15, y=280)
        self.entlevel.place(x=10,y=300)
        elo.place(x=175, y=280)
        self.entelo.place(x=165,y=300)
        labelCreditos.pack(side=BOTTOM)
        self.textoCadastro.pack(side=BOTTOM)
        voltarCadastro.place(x=5,y=350)
        cadastrarCadastro.place(x=235,y=350)
        self.janelas['janelaCadastro'].mainloop()
        
        
        
    def voltarCadastro_click(self):
        '''
        Quando voltar é clicado na tela de cadastro, some a tela de cadastro e volta com a tela de login
        '''
        
        self.janelas['janelaCadastro'].withdraw() #Fecha a janela de cadastro
        self.janelas['janela'].deiconify() #Abre a janela de entrada
        self.textoJanela['text']=''
        
    def cadastrar_click(self):
        '''
        Faz o papel de informar ao usuário se o cadastro foi bem sucecido ou não, imprimindo na janela textos de erro ou textos de exito
        Chama a função de criar usuário, caso saia tudo certo, o usuário é criado.
        '''
        
        login = str(self.entloginCadastro.get())
        senha = str(self.entsenhaCadastro.get())
        nick = str(self.entnick.get())
        time = str(self.enttime.get())
        campeao = str(self.entcampeao.get())
        level = str(self.entlevel.get())
        elo = str(self.entelo.get())
        check = criar_usuario(login,senha,nick,time,campeao,level,elo) #Chama a função criar usuário e atribui o que ocorreu a uma variavel em valor de número
        if check == 0:
            self.textoCadastro['text']='Campo vazio'
            self.textoCadastro['fg']='red'
            messagebox.showerror('ERRO!!!','Você deixou algum obrigatório vazio.')
            
        if check == 1:
            self.textoCadastro['text']='Usuário já cadastrado'
            self.textoCadastro['fg']='red'
            messagebox.showerror('ERRO!!!','Este usuário já está cadastrado.')
            
        if check == 2:
            self.textoCadastro['text']='Bem vindo\n%s'%(nick)
            self.textoCadastro['fg']='light green'
            self.janelas['janelaCadastro'].withdraw()
            self.janelas['janela'].deiconify()
            self.textoJanela['text']='Usuário cadastrado com sucesso'
            self.textoJanela['fg']='light green'
            messagebox.showinfo('SUCESSO!!!','Usuário cadastrado com sucesso.')

            
        if check == 3:
            self.textoCadastro['text']='O elo digitado não existe'
            self.textoCadastro['fg']='red'
            messagebox.showerror('ERRO!!!','O elo informado não existe.\nSe não possui elo apenas deixe em branco.')
            
        if check == 4:
            self.textoCadastro['text']='O level preciso ter\n apenas numeros'
            self.textoCadastro['fg']='red'
            messagebox.showerror('ERRO!!!','O level informado só aceita números')
            
    
    def entrarJanela_click(self):
        '''
        Cria a janela principal, a janela do lobby, e abre a mesma, fechando a janela de login.
        Aqui onde estão os botões principais com as funcionalidades do programa.
        '''
        
        self.janelas['janela'].withdraw() #Fecha a janela de entrada
        self.janelas['janelaPrincipal']=Tk() #Cria a janela principal
        self.janelas['janelaPrincipal'].title("A melhor janela de todas")
        self.janelas['janelaPrincipal']['bg']=verdeNovo
        self.janelas['janelaPrincipal'].geometry('600x600+350+80')
        self.janelas['janelaPrincipal'].wm_iconbitmap('lol1.ico')
        
        #Frames
        frame1 = Frame(self.janelas['janelaPrincipal'],bg=verdeNovo, bd=15)
        frame2 = Frame(self.janelas['janelaPrincipal'],bg=verdeNovo)
        frame3 = Frame(self.janelas['janelaPrincipal'],bg=verdeNovo)
        frame4 = Frame(self.janelas['janelaPrincipal'],bg=verdeNovo)
        
        #Labels
        logo = Label(frame1,text = 'Bem vindo ao lobby do\nLeagueData',font= 'verdana 15 bold',bg=verdeNovo,fg='white' )
        self.textoPrincipal = Label(frame2, text='Seja bem vindo\n%s'%(self.usuarioLogado[1][1]),bg=verdeNovo,fg='white',font = 'verdana 8 ')
        self.textoInf = Label(frame4,text='',bg=verdeNovo,font = 'verdana 8 ')
        labelCreditos = Label(frame4,width= 300,bg=azulNovo,text='Copyright(c) 2018 José Sheldon Brito Fekete',font='arial 8')
        
        #Buttons
        desconectar = Button(frame4,text='Desconectar',width=10,bg=azul,fg='white',command= self.desconectar_click)
        buscarUsuario = Button(frame3,text='Busca de usuários', width= 60,height=2,bg=azulNovo,fg='white',font='arial 10',command=self.buscarUsuario_click)
        buscarCampeao = Button(frame3,text='Buscar Campeão', width= 60,height=2,bg=azul,fg='white',command = self.buscarCampeao_click)
        atualizarInf = Button(frame3,text='Atualizar Informações', width= 60,height=2,bg=azulNovo,fg='white',font='arial 10',command=self.atualizarInf_click)
        trocarCargo = Button(frame3,text='Trocar cargos', width= 60,height=2,bg=azul,fg='white',command= self.trocarCargo_click)
        informar = Button(frame3,text='Informações do usuário', width= 60,height=2,bg=azul,fg='white',command = self.informar_click)
        deletarUsuario = Button(frame3,text='Deletar usuario', width= 60,height=2,bg=azulNovo,fg='white',font='arial 10',command=self.deletarUsuario_click)
        gerarRelatorio = Button(frame3,text='Gerar relatório', width= 60,height=2,bg=azul,fg='white',command = self.gerarRelatorio_click)
        
                
        
        #Empacotamento
        frame1.pack()
        frame2.pack(fill=X)
        frame3.pack(fill=Y)
        frame4.pack(fill=Y, expand=True)
        logo.grid(row=0,column=0,sticky='')
        informar.grid(row=0,column=0,pady=5)
        buscarUsuario.grid(row=1,column=0,pady=5)
        buscarCampeao.grid(row=2,column=0,pady=5)
        atualizarInf.grid(row=3,column=0,pady=5)
        trocarCargo.grid(row=4,column=0,pady=5)
        deletarUsuario.grid(row=5,column=0,pady=5)
        gerarRelatorio.grid(row=6,column=0,pady=5)
        labelCreditos.pack(side=BOTTOM)
        desconectar.pack(side=BOTTOM)
        self.textoInf.pack(side=BOTTOM)
        self.textoPrincipal.pack()
        
        self.janelas['janelaPrincipal'].mainloop()
        
    
    def desconectar_click(self):
        '''
        fecha a janela principal e se desloga da conta e abre a tela de login
        '''
        
        '''Salvando no log'''            
        log = 'Se desconectou.'
        log_exec(log,self.usuarioLogado[0])
        
        self.usuarioLogado='' #limpa as informações do usuario
        self.janelas['janelaPrincipal'].withdraw()
        self.textoJanela['text']=''
        self.entloginJanela.delete(0, 'end')
        self.entsenhaJanela.delete(0, 'end')
        self.janelas['janela'].deiconify()

        
    
    def informar_click(self):
        '''
        Cria a janela informação do usuárioEntra, fecha janela principal e abre a de Informação do usuário
        '''
        
        self.janelas['janelaPrincipal'].withdraw() #Fecha a janela principal
        self.janelas['janelaInformar']=Tk() #Cria a janela Informar
        self.janelas['janelaInformar'].title("A melhor janela de todas")
        self.janelas['janelaInformar']['bg']=verdeNovo
        self.janelas['janelaInformar'].geometry('600x600+350+80')
        self.janelas['janelaInformar'].wm_iconbitmap('lol1.ico')

        login,senha,cargo,nick,time,campeao,level,elo = filtrarInformacao(self.usuarioLogado) #Chama a função filtrar informações e separa cada informação do usuário em uma variável
        

        #Frames
        frame1 = Frame(self.janelas['janelaInformar'],bg=verdeNovo,bd=20)
        frame2 = Frame(self.janelas['janelaInformar'],bg=verdeNovo)

        #Labels
        logo = Label(frame1,text = 'Ola %s\nLogo abaixo estão suas informações'%(self.usuarioLogado[0]),font= 'verdana 14 bold',bg=verdeNovo,fg='white' )
        logoConta = Label(frame2, text='Informações da conta',font= 'arial 10 ',bg=azulNovo,fg='black',width=68)
        logoLol = Label(frame2, text='Informações relacionadas ao League of Legends',font= 'arial 10 ',bg=azulNovo,fg='black',width=68)
        labelCreditos = Label(self.janelas['janelaInformar'],width= 300,bg=azulNovo,text='Copyright(c) 2018 José Sheldon Brito Fekete',font='arial 8')
        infConta = Label(frame2, text='Login - %s\n\nSenha - %s\n\nCargo - %s'%(login,senha,cargo),bg=verdeNovo,fg='black')
        infLol = Label(frame2, text='Nickname - %s\n\nTime favorito - %s\n\nCampeão Favorito - %s\n\nLevel - %s\n\nElo - %s'%(nick,time,campeao,level,elo)
                       ,bg=verdeNovo,fg='black')
        espacamento = Label(frame2,bg=verdeNovo)
        
        #Buttons
        voltarInformar = Button(self.janelas['janelaInformar'],text='Voltar', width= 8,command = self.voltarInformar_click,bg=azul,bd=1,fg='white')

        #Empacotamento
        frame1.pack()
        frame2.pack(fill=Y)
        logo.grid(row=0,column=0,sticky='')
        logoConta.grid(row=0,column=0,sticky='')
        infConta.grid(row=1,column=0,sticky='',pady=10)
        espacamento.grid(row=2,column=0,sticky='',pady=5)
        logoLol.grid(row=3,column=0,sticky='')
        infLol.grid(row=4,column=0,sticky='',pady=10)
        labelCreditos.pack(side=BOTTOM)
        voltarInformar.pack(side=BOTTOM)
        

    def voltarInformar_click(self):
        '''
        Fecha a janela Informar e volta pra janela principal
        '''
        
        self.janelas['janelaInformar'].withdraw() 
        self.janelas['janelaPrincipal'].deiconify()
        self.textoPrincipal['text']='O que deseja fazer agora\n%s'%(self.usuarioLogado[1][1])
        self.textoInf['text']=''

    def buscarUsuario_click(self):
        '''
        Cria e abre a janela de menus de busca, fechando a janela principal
        '''
        
        self.janelas['janelaPrincipal'].withdraw() #fecha a janela principal
        self.janelas['janelaBusca']=Tk() #Cria a janela para digitar o usuario que irá se atualizado as informações
        self.janelas['janelaBusca'].title("A melhor janela de todas")
        self.janelas['janelaBusca']['bg']=azulEscuro
        self.janelas['janelaBusca'].geometry('400x400+450+150')
        self.janelas['janelaBusca'].wm_iconbitmap('lol1.ico')
        self.janelas['janelaBusca'].resizable(False,False)


        #Frames
        framePrincipal = Frame(self.janelas['janelaBusca'],bg=azulEscuro)

        #Label
        logo = Label(self.janelas['janelaBusca'],text='Selecione o tipo de busca',fg='white',bg=azulEscuro,font='verdana 10 bold',bd=10)
        
        #Buttons
        pesquisarPorUsuario = Button(framePrincipal,bg = azul,fg='white',width = 25, height = 3,text='Pesquisar por nome\ndo usuário',
                                     command=self.pesquisarPorUsuario_click)

        voltar = Button(self.janelas['janelaBusca'],bg = azul,fg='white',width=8,text='Voltar',command=self.voltarBusca_click)

        #Empacotamento
        logo.pack()
        framePrincipal.pack()
        pesquisarPorUsuario.grid(row=1,column=0,sticky='',pady=5)
        voltar.pack(side=BOTTOM, anchor=W)


    def voltarBusca_click(self):
        '''
        Fecha a janela de menus de busca e abre a janela principal
        '''
        
        self.janelas['janelaBusca'].withdraw() 
        self.janelas['janelaPrincipal'].deiconify()
        self.textoPrincipal['text']='O que deseja fazer agora\n%s'%(self.usuarioLogado[1][1])
        self.textoInf['text']=''

    
    
    def pesquisarPorUsuario_click(self):
        '''
        Abre a janela de busca por usuario pesquisando o login e mostrando as informações do league of legends,  fechando a janela principal
        '''
        
        self.janelas['janelaBusca'].withdraw() #fecha a janela principal
        self.janelas['janelaBuscarUsuario']=Tk() #Cria a janela buscar usuario
        self.janelas['janelaBuscarUsuario'].title("A melhor janela de todas")
        self.janelas['janelaBuscarUsuario']['bg']=verdeNovo
        self.janelas['janelaBuscarUsuario'].geometry('600x600+350+80')
        self.janelas['janelaBuscarUsuario'].wm_iconbitmap('lol1.ico')
        
        #Frames
        frameLogo = Frame(self.janelas['janelaBuscarUsuario'],bg=verdeNovo,bd=20)
        framePesquisa = Frame(self.janelas['janelaBuscarUsuario'],bg=verdeNovo)
        frameTexto = Frame(self.janelas['janelaBuscarUsuario'],bg=verdeNovo,bd=20)
        frameUsuario = Frame(self.janelas['janelaBuscarUsuario'],bg=verdeNovo,bd=20)
        
        #Labels
        logo = Label(frameLogo,text = 'Bem vindo a janela de pesquisa',font= 'verdana 14 bold',bg=verdeNovo,fg='white' )
        logoPesquisa = Label(framePesquisa, text='Pesquisar Usuário',font= 'arial 10 ',bg=azulNovo,fg='black',width=68)
        usuario = Label(framePesquisa, text='Usuario',font= 'arial 9 ',bg=verdeNovo,fg='white')
        self.textoBuscarUsuario = Label(frameTexto,text='',bg=verdeNovo)
        labelCreditos = Label(self.janelas['janelaBuscarUsuario'],width= 300,bg=azul,text='Copyright(c) 2018 José Sheldon Brito Fekete',font='arial 8')

        self.infUsuario = Label(frameUsuario,fg='black',bg=verdeNovo)
        
        #Entrys
        self.entbuscarUsuario = Entry(framePesquisa,bg='light blue',bd=0,fg=cinza,width=30)
        
        #Buttons
        voltarBuscarUsuario = Button(self.janelas['janelaBuscarUsuario'],text='Voltar', width= 8,command = self.voltarBuscarUsuario_click,bg=azul,bd=1,fg='white')
        pesquisarUsuario = Button(framePesquisa,text='Pesquisar', width= 8,command = self.pesquisarUsuario_click,bg=azul,bd=1,fg='white')
        
        #Empacotamento
        frameLogo.pack()
        framePesquisa.pack()
        logoPesquisa.grid(row=0,column=0,sticky='',pady=10)
        logo.grid(row=0,column=0,sticky='')
        usuario.grid(row=1,column=0,sticky='')
        self.entbuscarUsuario.grid(row=2,column=0,sticky='')
        pesquisarUsuario.grid(row=3,column=0,sticky='',pady=8)
        self.textoBuscarUsuario.pack()
        frameUsuario.pack()
        self.infUsuario.grid(row=0,column=0,sticky='')

        labelCreditos.pack(side=BOTTOM)
        voltarBuscarUsuario.pack(side=BOTTOM)
        frameTexto.pack(side=BOTTOM)



    def pesquisarUsuario_click(self):
        '''
        Faz a pesquisa no banco de dados de usuario, se esse usuário existir, mostra as informações na tela
        '''
        
        bd= ler_usuarios()
        if not self.entbuscarUsuario.get() in bd:
            self.textoBuscarUsuario['text']='Este usuário não existe'
            self.textoBuscarUsuario['fg']='red'
            messagebox.showerror('ERRO!!!','Usuário pesquisado não existe.')
        else:
            '''
            Cria uma variavel usuarioPesquisa e filtra os dados para a visualização
            '''
            self.textoBuscarUsuario['text']='' #Tira o texto de erro da tela
            usuarioPesquisa = []
            usuarioPesquisa.append(self.entbuscarUsuario.get())
            usuarioPesquisa.append(bd[self.entbuscarUsuario.get()])
            login,senha,cargo,nick,time,campeao,level,elo = filtrarInformacao(usuarioPesquisa) #Chama a função filtrar informações e separa cada informação do usuário em uma variável


            ''' Atribui um texto para um label já conhecido, mostrando as informações do usuário  '''
            self.infUsuario['text']='Nickname - %s\n\nTime favorito - %s\n\nCampeão Favorito - %s\n\nLevel - %s\n\nElo - %s'%(nick,time,campeao,level,elo)
            

    def voltarBuscarUsuario_click(self):
        '''
        fecha a tela buscar usuario e volta pra principal
        '''
        
        self.janelas['janelaBuscarUsuario'].withdraw() 
        self.janelas['janelaBusca'].deiconify()
        self.textoPrincipal['text']='O que deseja fazer agora\n%s'%(self.usuarioLogado[1][1])
        self.textoInf['text']=''


    def buscarCampeao_click(self):
        '''
        cria a janela buscar campeão, abrindo a mesma e fechando a janela principal
        '''
        
        self.janelas['janelaPrincipal'].withdraw() #fecha a janela principal
        self.janelas['janelaBuscarCampeão'] =Tk() #Cria a janela buscar Campeão
        self.janelas['janelaBuscarCampeão'].title("A melhor janela de todas")
        self.janelas['janelaBuscarCampeão']['bg']=verdeNovo
        self.janelas['janelaBuscarCampeão'].geometry('600x600+350+80')
        self.janelas['janelaBuscarCampeão'].wm_iconbitmap('lol1.ico')

        #frames
        framePrincipal = Frame(self.janelas['janelaBuscarCampeão'],bg=verdeNovo)
        subFrame = Frame(framePrincipal,bg=verdeNovo)

        #labels
        logo = Label(self.janelas['janelaBuscarCampeão'],bg=verdeNovo,text='Buscar Campeões',fg='white',font='verdana 12 bold',bd=15)
        logoCampeao = Label(framePrincipal, text='Pesquisar Campeão',font= 'arial 10 ',bg=azulNovo,fg='black',width=68)
        self.textoBuscarCampeao = Label(self.janelas['janelaBuscarCampeão'],text='',bg=verdeNovo,bd=5)
        self.campeao = Label(framePrincipal,bg=verdeNovo,fg=azulEscuro,font='arial 30 bold')
        self.titulo = Label(framePrincipal,bg=verdeNovo,fg=vermelho,font='arial 12 ')
        self.regiao = Label(subFrame,bg=verdeNovo,fg='black',font='arial 10')
        self.classe = Label(subFrame,bg=verdeNovo,fg='black',font='arial 10')
        self.frase = Label(framePrincipal,bg=verdeNovo,fg=platina,font='arial 12 bold',wraplength=550)
        
        self.historia = Label(framePrincipal,bg=verdeNovo,fg='#470601',font='arial 8 bold',wraplength=550)

        labelCreditos = Label(self.janelas['janelaBuscarCampeão'],width= 300,bg=azul,text='Copyright(c) 2018 José Sheldon Brito Fekete',font='arial 8')
        #Entrys
        self.entbuscarCampeao = Entry(framePrincipal,bg='light blue',bd=0,fg=cinza,width=30)
        
        #Buttons
        pesquisarCampeao = Button(framePrincipal,text='Buscar', width= 8,fg='white',command = self.pesquisarCampeao_click,bg=azul)
        voltarBuscarCampeao = Button(self.janelas['janelaBuscarCampeão'],text='Voltar', width= 8,command = self.voltarBuscarCampeao_click,bg=azul,bd=1,fg='white')
        
        #Empacotamento
        logo.pack(fill=X,anchor=CENTER)
        framePrincipal.pack(fill=Y)
        logoCampeao.grid(row=0,column =0,sticky='',pady=20)
        self.entbuscarCampeao.grid(row=1,column=0,sticky='')
        pesquisarCampeao.grid(row=2,column=0,sticky='',pady=5)
        self.campeao.grid(row=3,column=0,sticky='',pady=5)
        self.titulo.grid(row=4,column=0,sticky='')
        
        subFrame.grid(row=5,column=0,sticky='',pady=10)
        self.regiao.grid(row=0,column=0,sticky=W,padx=15)
        self.classe.grid(row=0,column=1,sticky=E,padx=15)
        
        self.frase.grid(row=6,column=0,sticky='',pady=10)
        self.historia.grid(row=7,column=0)
        
        
        labelCreditos.pack(side=BOTTOM)
        voltarBuscarCampeao.pack(side=BOTTOM,anchor=CENTER)
        self.textoBuscarCampeao.pack(side = BOTTOM)

    def pesquisarCampeao_click(self):
        '''
        cria um dicionário com as informações dos campeões, e se o campeão pesquisado estiver certo, mostra as informaçoes na tela
        '''
        
        campeos = abrir_arquivo('campeões.txt')
        encontrou = False
        for campeao in campeos:
            if campeao.upper() == self.entbuscarCampeao.get().upper():
                self.textoBuscarCampeao['text']=''  #Limpa a mensagem de erro
                self.campeao['text']=campeao
                self.titulo['text']=campeos[campeao][1].upper()
                self.regiao['text']='Região: '+campeos[campeao][0]
                self.classe['text']='Classe: '+campeos[campeao][2]
                self.frase['text']=campeos[campeao][3]
                self.historia['text']='Historia:\n\n'+campeos[campeao][4]

                encontrou = True
                
        if not encontrou:
            
            self.textoBuscarCampeao['text']='este campeão não existe'
            self.textoBuscarCampeao['fg']='red'
            messagebox.showerror('ERRO!!!','Campeão pesquisado não existe.')
                
    def voltarBuscarCampeao_click(self):
        '''
        fecha a tela buscar usuario e volta pra principal
        '''
        
        self.janelas['janelaBuscarCampeão'].withdraw() 
        self.janelas['janelaPrincipal'].deiconify()
        self.textoPrincipal['text']='O que deseja fazer agora\n%s'%(self.usuarioLogado[1][1])
        self.textoInf['text']=''

    
    def trocarCargo_click(self):
        '''
        Cria a janela trocar cargo, abrindo a mesma e fechando a janela principal, só abrirá se o usuário tiver o cargo de admnistrador
        '''
        
        if int(self.usuarioLogado[1][6]) < 2:
            self.textoInf['text']='Seu cargo não permite\nutilizar essa função'
            self.textoInf['fg']='red'
            messagebox.showerror('Permissão insuficiente','Seu cargo nao permite utilizar essa função')
        else:
            self.janelas['janelaPrincipal'].withdraw()
            self.janelas['janelaTrocarCargo']=Tk()
            self.janelas['janelaTrocarCargo'].title("A melhor janela de todas")
            self.janelas['janelaTrocarCargo']['bg']=azul
            self.janelas['janelaTrocarCargo'].geometry('400x400+465+165')
            self.janelas['janelaTrocarCargo'].wm_iconbitmap('lol1.ico')
            self.janelas['janelaTrocarCargo'].resizable(False,False)
            
            #Frames
            frame1 = Frame(self.janelas['janelaTrocarCargo'],bg=azul)
            frame2 = Frame(self.janelas['janelaTrocarCargo'],bg=azul,bd=5)
            frame3 = Frame(self.janelas['janelaTrocarCargo'],bg=azul)
            
            #Labels
            logo = Label(frame1,text = 'Trocar Cargos',font= 'verdana 14 bold',bg=azul,fg='white' )
            labelUsuario = Label(frame1,text='Digite aqui o usuário\na ter o cargo alterado',bg=azul,fg='white')
            labelCreditos = Label(self.janelas['janelaTrocarCargo'],width= 300,bg=verde,text='Copyright(c) 2018 José Sheldon Brito Fekete',font='arial 8')
            self.textoCargo = Label(frame3,text='',bg=azul)
            labelCargos = Label(frame1,text='Escolha o novo cargo',bg=azul,fg='white') 
            
            #Entrys
            self.usuarioTrocarCargo = Entry(frame1,width = 30,bg='light blue',bd=0,fg=cinza)
            
            #Buttons
            voltarTrocarCargo = Button(self.janelas['janelaTrocarCargo'],text='Voltar', width= 8,command = self.voltarTrocarCargo_click,bg=verde,bd=1,fg='white')
            botAdm = Button(frame2,text='Administrador',width=12,bg=verde,fg='white',command = partial(self.trocandoDeCargo_click,'2')) #Uso do partial passando a função e logo em seguida o que eu quero passar para função
            botMod = Button(frame2,text='Moderador',width=12,bg=verde,fg='white',command = partial(self.trocandoDeCargo_click,'1')) 
            botComum = Button(frame2,text='Usuario Comum',width=12,bg=verde,fg='white',command = partial(self.trocandoDeCargo_click,'0'))

            #Empacotamento
            frame1.pack()
            frame2.pack()
            frame3.pack(expand=True)
            logo.grid(row=0,column=0,sticky='',pady=30)
            labelUsuario.grid(row=1,column=0,sticky='')
            self.usuarioTrocarCargo.grid(row=2,column=0,sticky='',pady=5)
            labelCargos.grid(row=3,column=0,sticky='')
            botAdm.grid(row=0,column=0)
            botMod.grid(row=0,column=1,padx=5)
            botComum.grid(row=0,column=2)
            self.textoCargo.grid(row=0,column=0,sticky=S)
            labelCreditos.pack(side=BOTTOM)
            voltarTrocarCargo.pack(side=BOTTOM, anchor=W)
            
           
    def voltarTrocarCargo_click(self):
        '''
        Fecha a janela trocar usuario e volta pra janela principal
        '''
        
        self.janelas['janelaTrocarCargo'].withdraw()
        self.janelas['janelaPrincipal'].deiconify()
        self.textoPrincipal['text']='O que deseja fazer agora\n%s'%(self.usuarioLogado[1][1])
        self.textoInf['text']=''
        
    
    def trocandoDeCargo_click(self,cargo):
        '''
        Recebe o cargo passado e transforma o usuário digitado no determinado cargo
        '''

        bd = ler_usuarios()
        self.textoCargo['text']=bd
        encontrou = False

        for usuario in bd:
            
            if self.usuarioTrocarCargo.get() == usuario: #Se o usuário digitado existir
                encontrou = True
                if bd[usuario][6] == cargo:
                    self.textoCargo['text']='O usuário já possui esse cargo'
                    self.textoCargo['fg']='red'
                    messagebox.showerror('ERRO!!!','Usuário já possui esse cargo.')
                else:
                    cargoAntigo = bd[usuario][6]
                    bd[usuario] = (bd[usuario][0],bd[usuario][1],bd[usuario][2],bd[usuario][3],bd[usuario][4],bd[usuario][5],cargo)
                    self.textoCargo['text']='O cargo do usuário foi atualizado'
                    self.textoCargo['fg']='light green' 
                    self.usuarioTrocarCargo.delete(0,'end') #deleta o texto escrito no entry do usuário
                    salvar_usuarios(bd) #Salva alterações no usuarios.txt
                    messagebox.showinfo('Sucesso!!!','Cargo do usuário alterado com sucesso.')
                    
                    '''
                    Salvando no log
                    '''
                                        
                    log = 'Cargo de '+usuario+' alterado de '+cargoEmPalavra(cargoAntigo)+' para '+cargoEmPalavra(cargo)+'.'

                    log_exec(log,self.usuarioLogado[0])
                    
        if not encontrou:
            self.textoCargo['text']='Esse usuario não existe'
            self.textoCargo['fg']='red'
            messagebox.showerror('ERRO!!!','Esse usuário não existe.')
                                        
            
    
    def atualizarInf_click(self):
        '''
        Cria e abre janela de atualizar informações do usuário, fechando a janela principal
        Só entrará aqui se o usuário não for admnistrador
        '''
        
        if self.usuarioLogado[1][6] != '2':
            self.janelas['janelaPrincipal'].withdraw() #fecha a janela principal
            self.janelas['janelaAtualizarInf']=Tk() #Cria a janela atuallizar informações do usuario
            self.janelas['janelaAtualizarInf'].title("A melhor janela de todas")
            self.janelas['janelaAtualizarInf']['bg']=azul
            self.janelas['janelaAtualizarInf'].geometry('600x600+350+80')
            self.janelas['janelaAtualizarInf'].wm_iconbitmap('lol1.ico')

            #Frames
            frameLogo = Frame(self.janelas['janelaAtualizarInf'],bg=azul)
            framePrincipal = Frame(self.janelas['janelaAtualizarInf'],bg=azul,bd=10)
            subFrameSenha = Frame(framePrincipal,bg=azul)
            subFrameLol = Frame(framePrincipal,bg=azul)
                
            #Labels
            senhaAtual = Label(framePrincipal,text='Senha atual',bg=azul,fg='white')
            senha = Label(subFrameSenha,text='Senha',bg=azul,fg='white')
            senhaConfirmar = Label(subFrameSenha,text='Confirmar senha',bg=azul,fg='white')
            nick = Label(framePrincipal, text='Nickname',bg=azul, fg='white')
            time = Label(subFrameLol, text='Time que torce',bg=azul,fg='white')
            campeao = Label(subFrameLol, text='Campeão favorito',bg=azul,fg='white')
            level = Label(subFrameLol, text='Level do invocador',bg=azul,fg='white')
            elo = Label(subFrameLol, text='Elo do invocador ',bg=azul,fg='white')
            logo = Label(frameLogo,text = 'Atualizar Informações',font= 'verdana 16 bold',bg=azul,fg='white' )
            labelCreditos = Label(self.janelas['janelaAtualizarInf'],width= 300,bg=verde,text='Copyright(c) 2018 José Sheldon Brito Fekete',font='arial 8')
            informacao = Label(frameLogo,text='Deixe em vazio apenas as informações\nque não deseja alterar',bg=azul)
            self.textoAtualizarInf = Label(framePrincipal,bg=azul,text='')
            logoConta = Label(framePrincipal, text='Informações da conta',bg=verdeNovo,fg='white',width=80)
            logoLol = Label(framePrincipal,text='Informações sobre o League of Legends',bg=verdeNovo,fg='white',width=80)
            textoSenha = Label(frameLogo,text='Senha atual é um campo obrigatório',bg=azul,fg='red')
                
            #Entrys
            self.entsenhaAtualInf = Entry(framePrincipal,bg='light blue',bd=0,fg=cinza,width=25,show='*')
            self.entsenhaInf = Entry(subFrameSenha,show='*',bg='light blue',bd=0,fg=cinza,width=25)
            self.entsenhaConfirmarInf = Entry(subFrameSenha,show='*',bg='light blue',bd=0,fg=cinza,width=25)
            self.entnickInf = Entry(framePrincipal,bg='light blue',bd=0,fg=cinza,width=25)
            self.enttimeInf = Entry(subFrameLol,bg='light blue',bd=0,fg=cinza,width=25)
            self.entcampeaoInf = Entry(subFrameLol,bg='light blue',bd=0,fg=cinza,width=25)
            self.entlevelInf = Entry(subFrameLol,bg='light blue',bd=0,fg=cinza,width=25)
            self.enteloInf = Entry(subFrameLol,bg='light blue',bd=0,fg=cinza,width=25)
                
            #Buttons
            voltarAtualizarInf = Button(self.janelas['janelaAtualizarInf'],text='Voltar', width= 8,command = self.voltarAtualizarInf_click,bg=azulNovo,bd=1,fg='white')
            alterarInformacao = Button(framePrincipal,text='Alterar',bg=azulNovo,fg='white',width=8,command= partial(self.alterarInformacao_click,self.usuarioLogado[0]))
                

            #Empacotamento
            frameLogo.pack()
            framePrincipal.pack()
            logo.grid(row=0,column=0,sticky='',pady=20)
            informacao.grid(row=1,column=0,sticky='')
            textoSenha.grid(row=2,column=0,sticky='')
            logoConta.grid(row=0,column=0,sticky='',pady=5)
                
            senhaAtual.grid(row=1,column=0,sticky='')
            self.entsenhaAtualInf.grid(row=2,column=0,sticky='')

            subFrameSenha.grid(row=3,column=0,sticky='',pady=5)
                
            senha.grid(row=0,column=0)
            self.entsenhaInf.grid(row=1,column=0,padx=10)
                
            senhaConfirmar.grid(row=0,column=1)
            self.entsenhaConfirmarInf.grid(row=1,column=1)
                
            logoLol.grid(row=4,column=0,sticky='',pady=10)
                
            nick.grid(row=5,column=0,stick='')
            self.entnickInf.grid(row=6,column=0,sticky='')

            subFrameLol.grid(row=7,column=0,sticky='',pady=5)

            time.grid(row=0,column=0)
            self.enttimeInf.grid(row=1,column=0,padx=10,pady=5)
            campeao.grid(row=0,column=1)
            self.entcampeaoInf.grid(row=1,column=1,pady=5)
            elo.grid(row=2,column=0)
            self.enteloInf.grid(row=3,column=0,padx=10)
            level.grid(row=2,column=1)
            self.entlevelInf.grid(row=3,column=1)
            alterarInformacao.grid(row=8,column=0,sticky='',pady=20)
            self.textoAtualizarInf.grid(row=9,column=0,sticky='',pady=10)
                
            labelCreditos.pack(side=BOTTOM)
            voltarAtualizarInf.pack(side=BOTTOM,anchor=W)
        else:
            '''
            Cria e Abre uma janela para informar o usuário a ter suas informações alteradas, fechando a janela principal
            No caso de ser administrador, abrirá uma janela para buscar o usuário a ter as informações alteradas
            '''
            
            self.janelas['janelaPrincipal'].withdraw() #fecha a janela principal
            self.janelas['janelaAtualizarInfAdm']=Tk() #Cria a janela para digitar o usuario que irá se atualizado as informações
            self.janelas['janelaAtualizarInfAdm'].title("A melhor janela de todas")
            self.janelas['janelaAtualizarInfAdm']['bg']=azulEscuro
            self.janelas['janelaAtualizarInfAdm'].geometry('400x400+450+150')
            self.janelas['janelaAtualizarInfAdm'].wm_iconbitmap('lol1.ico')
            self.janelas['janelaAtualizarInfAdm'].resizable(False,False)

            #Frames
            framePrincipal = Frame(self.janelas['janelaAtualizarInfAdm'],bg=azulEscuro)
            

            #Labels
            logoUsuario = Label(self.janelas['janelaAtualizarInfAdm'],text='Digite o usuário a ter suas\ninformações atualizadas',bg=azulEscuro,bd=20,fg='white',font='verdana 12 bold')
            usuario = Label(framePrincipal,text='Usuário',bg=azulEscuro,fg='white',font='arial 8 bold')
            self.textoInfAdm = Label(self.janelas['janelaAtualizarInfAdm'],bg=azulEscuro,text='',bd=10)
            labelCreditos = Label(self.janelas['janelaAtualizarInfAdm'],width= 300,bg=azulNovo,text='Copyright(c) 2018 José Sheldon Brito Fekete',font='arial 8')
            
            #Entry
            self.entUsuario = Entry(framePrincipal,bg='light blue',fg=cinza,width=25)
            
            #Buttons
            voltar = Button(self.janelas['janelaAtualizarInfAdm'],text='Voltar',bg=azul,fg='white',width=10,command=self.voltarAtualizarInfAdm_click)
            confirmar = Button(framePrincipal,text='Confirmar',bg=azul,fg='white',width=10,command=self.confirmarAtualizarInfAdm_click)
            
            #empacotamento
            logoUsuario.pack()
            framePrincipal.pack()
            usuario.grid(row=0,column=0,sticky='')
            self.entUsuario.grid(row=1,column=0,sticky='',pady=5)
            confirmar.grid(row=2,column=0,sticky='')
    
            labelCreditos.pack(side=BOTTOM)
            voltar.pack(side=BOTTOM,anchor=W)
            self.textoInfAdm.pack(side=BOTTOM,anchor=CENTER)
            
    
    def confirmarAtualizarInfAdm_click(self):
        '''
        Abre a janela de atualizar informações só que atualizará as informações do usuario que o admnistrador solicitou
        '''
        
        bd = ler_usuarios()
        encontrou = False
        for usuario in bd:
            if usuario == self.entUsuario.get():
                self.usuarioTrocarInf = usuario
                self.janelas['janelaAtualizarInfAdm'].withdraw()
                encontrou = True
                
                #Cria a janela atualizar informações, porém dessa vez passa como parametro o usuário digitado anteriormente 
                self.janelas['janelaPrincipal'].withdraw() 
                self.janelas['janelaAtualizarInf']=Tk() 
                self.janelas['janelaAtualizarInf'].title("A melhor janela de todas")
                self.janelas['janelaAtualizarInf']['bg']=azul
                self.janelas['janelaAtualizarInf'].geometry('600x600+350+80')
                self.janelas['janelaAtualizarInf'].wm_iconbitmap('lol1.ico')

                #Frames
                frameLogo = Frame(self.janelas['janelaAtualizarInf'],bg=azul)
                framePrincipal = Frame(self.janelas['janelaAtualizarInf'],bg=azul,bd=10)
                subFrameSenha = Frame(framePrincipal,bg=azul)
                subFrameLol = Frame(framePrincipal,bg=azul)
                
                #Labels
                senha = Label(subFrameSenha,text='Senha',bg=azul,fg='white')
                senhaConfirmar = Label(subFrameSenha,text='Confirmar senha',bg=azul,fg='white')
                nick = Label(framePrincipal, text='Nickname',bg=azul, fg='white')
                time = Label(subFrameLol, text='Time que torce',bg=azul,fg='white')
                campeao = Label(subFrameLol, text='Campeão favorito',bg=azul,fg='white')
                level = Label(subFrameLol, text='Level do invocador',bg=azul,fg='white')
                elo = Label(subFrameLol, text='Elo do invocador ',bg=azul,fg='white')
                logo = Label(frameLogo,text = 'Atualizar Informações',font= 'verdana 16 bold',bg=azul,fg='white' )
                labelCreditos = Label(self.janelas['janelaAtualizarInf'],width= 300,bg=verde,text='Copyright(c) 2018 José Sheldon Brito Fekete',font='arial 8')
                informacao = Label(frameLogo,text='Deixe em vazio apenas as informações\nque não deseja alterar',bg=azul)
                self.textoAtualizarInf = Label(framePrincipal,bg=azul,text='')
                logoConta = Label(framePrincipal, text='Informações da conta',bg=verdeNovo,fg='white',width=80)
                logoLol = Label(framePrincipal,text='Informações sobre o League of Legends',bg=verdeNovo,fg='white',width=80)
                textoSenha = Label(frameLogo,text='Senha atual é um campo obrigatório',bg=azul,fg='red')
                
                #Entrys
                self.entsenhaInf = Entry(subFrameSenha,show='*',bg='light blue',bd=0,fg=cinza,width=25)
                self.entsenhaConfirmarInf = Entry(subFrameSenha,show='*',bg='light blue',bd=0,fg=cinza,width=25)
                self.entnickInf = Entry(framePrincipal,bg='light blue',bd=0,fg=cinza,width=25)
                self.enttimeInf = Entry(subFrameLol,bg='light blue',bd=0,fg=cinza,width=25)
                self.entcampeaoInf = Entry(subFrameLol,bg='light blue',bd=0,fg=cinza,width=25)
                self.entlevelInf = Entry(subFrameLol,bg='light blue',bd=0,fg=cinza,width=25)
                self.enteloInf = Entry(subFrameLol,bg='light blue',bd=0,fg=cinza,width=25)
                    
                #Buttons
                voltarAtualizarInf = Button(self.janelas['janelaAtualizarInf'],text='Voltar', width= 8,command = self.voltarAtualizarInf_click,bg=azulNovo,bd=1,fg='white')
                alterarInformacao = Button(framePrincipal,text='Alterar',bg=azulNovo,fg='white',width=8,command= partial(self.alterarInformacao_click,self.usuarioTrocarInf))
                    

                #Empacotamento
                frameLogo.pack()
                framePrincipal.pack()
                logo.grid(row=0,column=0,sticky='',pady=20)
                informacao.grid(row=1,column=0,sticky='')
                textoSenha.grid(row=2,column=0,sticky='')
                logoConta.grid(row=0,column=0,sticky='',pady=5)



                subFrameSenha.grid(row=3,column=0,sticky='',pady=5)
                    
                senha.grid(row=0,column=0)
                self.entsenhaInf.grid(row=1,column=0,padx=10)
                    
                senhaConfirmar.grid(row=0,column=1)
                self.entsenhaConfirmarInf.grid(row=1,column=1)
                        
                logoLol.grid(row=4,column=0,sticky='',pady=10)
                    
                nick.grid(row=5,column=0,stick='')
                self.entnickInf.grid(row=6,column=0,sticky='')

                subFrameLol.grid(row=7,column=0,sticky='',pady=5)

                time.grid(row=0,column=0)
                self.enttimeInf.grid(row=1,column=0,padx=10,pady=5)
                campeao.grid(row=0,column=1)
                self.entcampeaoInf.grid(row=1,column=1,pady=5)
                elo.grid(row=2,column=0)
                self.enteloInf.grid(row=3,column=0,padx=10)
                level.grid(row=2,column=1)
                self.entlevelInf.grid(row=3,column=1)
                alterarInformacao.grid(row=8,column=0,sticky='',pady=20)
                self.textoAtualizarInf.grid(row=9,column=0,sticky='',pady=10)
                    
                    
                labelCreditos.pack(side=BOTTOM)
                voltarAtualizarInf.pack(side=BOTTOM,anchor=W)
                

                
        if not encontrou: #Se não encontrou passa uma mensagem de erro
            self.textoInfAdm['text']='Não existe esse usuário'
            self.textoInfAdm['fg']='red'
            messagebox.showerror('ERRO!!!','Usuário informado não existe.')
            
    
    def voltarAtualizarInfAdm_click(self):
        '''
        fecha a janela atualizar informações do administrador e volta pra janela principal
        '''
        
        self.janelas['janelaAtualizarInfAdm'].withdraw() 
        self.janelas['janelaPrincipal'].deiconify()
        self.textoPrincipal['text']='O que deseja fazer agora\n%s'%(self.usuarioLogado[1][1])
        self.usuarioTrocarInf='' #limpa a variável do usuario a ser trocado
        self.textoInf['text']=''

        
       
    def alterarInformacao_click(self,usuario):
        '''
        Altera as informações do usuario
        '''
        
        bd = ler_usuarios()

        if int(self.usuarioLogado[1][6]) < 2: #O usuário comum ou gerente tem que saber da senha para atualizar as suas informações
            senha = self.entsenhaAtualInf.get()
            
        if int(self.usuarioLogado[1][6]) >= 2: #O admnistrador recebe a senha correta do usuário a ter as informações atualizadas
            senha = bd[usuario][0]
            
        if senha != bd[usuario][0]: #Se a senha atual estiver incorreta
            self.textoAtualizarInf['text']='Senha informada incorreta'
            self.textoAtualizarInf['fg']='red'

          
        else:
            alterou = False
            if self.entsenhaInf.get() != '' or self.entsenhaConfirmarInf.get() != '': #As senhas precisam ser iguais na hora de confirmar
                if self.entsenhaInf.get() == self.entsenhaConfirmarInf.get():
                    bd[usuario] = (self.entsenhaInf.get(),bd[usuario][1],bd[usuario][2],bd[usuario][3],bd[usuario][4],bd[usuario][5],bd[usuario][6])
                    alterou = True
                    
                else:
                    self.textoAtualizarInf['text']='As senhas não coincidem'
                    self.textoAtualizarInf['fg']='red'
            if self.entnickInf.get() != '':
                bd[usuario] = (bd[usuario][0],self.entnickInf.get(),bd[usuario][2],bd[usuario][3],bd[usuario][4],bd[usuario][5],bd[usuario][6])
                
                alterou = True
            if self.enttimeInf.get() != '':
                bd[usuario] = (bd[usuario][0],bd[usuario][1],self.enttimeInf.get().capitalize(),bd[usuario][3],bd[usuario][4],bd[usuario][5],bd[usuario][6])
                
                alterou = True
            if self.entcampeaoInf.get() != '':
                bd[usuario] = (bd[usuario][0],bd[usuario][1],bd[usuario][2],self.entcampeaoInf.get().capitalize(),bd[usuario][4],bd[usuario][5],bd[usuario][6])
                
                alterou = True
            if self.entlevelInf.get() != '':
                if self.entlevelInf.get().isdigit(): #O level só aceitará números
                    bd[usuario] = (bd[usuario][0],bd[usuario][1],bd[usuario][2],bd[usuario][3],self.entlevelInf.get(),bd[usuario][5],bd[usuario][6])
                    
                    alterou = True
                else:
                    self.textoAtualizarInf['text']='O level só suporta números'
                    self.textoAtualizarInf['fg']='red'
            if self.enteloInf.get() != '': # o elo tem que ser um já existente
                if self.enteloInf.get().capitalize() in ['Bronze','Prata','Ouro','Platina','Diamante','Mestre','Desafiante']:
                    bd[usuario] = (bd[usuario][0],bd[usuario][1],bd[usuario][2],bd[usuario][3],bd[usuario][4],self.enteloInf.get().capitalize(),bd[usuario][6])
                    alterou = True
                else:
                    self.textoAtualizarInf['text']='O elo informado não existe'
                    self.textoAtualizarInf['fg']='red'
        
            if alterou:
                salvar_usuarios(bd)
                '''
                Salvando no log
                '''
                            
                log = 'Alteração nas informações de '+usuario+'.'

                log_exec(log,self.usuarioLogado[0])
                
                self.janelas['janelaAtualizarInf'].withdraw()
                self.textoInf['text']='Informações Atualizadas com sucesso'
                self.textoInf['fg']='light green'
                self.janelas['janelaPrincipal'].deiconify()
            
    def voltarAtualizarInf_click(self):
        '''
        fecha a janela atualizar informações e volta pra janela principal
        '''
        
        self.janelas['janelaAtualizarInf'].withdraw() 
        self.janelas['janelaPrincipal'].deiconify()
        self.textoPrincipal['text']='O que deseja fazer agora\n%s'%(self.usuarioLogado[1][1])
        self.textoInf['text']=''
        self.usuarioTrocarInf = ''


    def deletarUsuario_click(self):
        '''
        Caso o cargo do usuário for igual a de admnistrador:
        Cria e abre a janela de deletar usuários, fecha a janela principal
        Se não for ira dar uma mensagem de erro
        '''
        
        if int(self.usuarioLogado[1][6]) >= 2:
        
            self.janelas['janelaPrincipal'].withdraw() #fecha a janela principal
            self.janelas['janelaDeletarUsuario']=Tk() #Cria a janela deletar usuario
            self.janelas['janelaDeletarUsuario'].title("A melhor janela de todas")
            self.janelas['janelaDeletarUsuario']['bg']=azulEscuro
            #Lado x Altura + Esquerda + Teto
            self.janelas['janelaDeletarUsuario'].geometry('400x400+450+150')
            self.janelas['janelaDeletarUsuario'].resizable(False,False)
            self.janelas['janelaDeletarUsuario'].wm_iconbitmap('lol1.ico')

            #Frames
            framePrincipal = Frame(self.janelas['janelaDeletarUsuario'],bg=azulEscuro)
                

            #Labels
            logoUsuario = Label(self.janelas['janelaDeletarUsuario'],text='Digite o usuário a ser deletado',bg=azulEscuro,bd=20,fg='white',font='verdana 12 bold')
            usuario = Label(framePrincipal,text='Usuário',bg=azulEscuro,fg='white',font='arial 8 bold')
            self.textoDeletarUsuario = Label(self.janelas['janelaDeletarUsuario'],bg=azulEscuro,text='',bd=10)
            labelCreditos = Label(self.janelas['janelaDeletarUsuario'],width= 300,bg=azulNovo,text='Copyright(c) 2018 José Sheldon Brito Fekete',font='arial 8')
                
            #Entry
            self.entDeletarUsuario = Entry(framePrincipal,bg='light blue',fg=cinza,width=30)
                
            #Buttons
            voltar = Button(self.janelas['janelaDeletarUsuario'],text='Voltar',bg=azul,fg='white',width=10,command=self.voltarDeletarUsuario_click)
            deletar = Button(framePrincipal,text='Deletar',bg=azul,fg='white',width=10,command=self.deletarDeletarUsuario_click)
                
            #empacotamento
            logoUsuario.pack()
            framePrincipal.pack()
            usuario.grid(row=0,column=0,sticky='')
            self.entDeletarUsuario.grid(row=1,column=0,sticky='',pady=10)
            deletar.grid(row=2,column=0,sticky='')
        
            labelCreditos.pack(side=BOTTOM)
            voltar.pack(side=BOTTOM,anchor=W)
            self.textoDeletarUsuario.pack(side=BOTTOM,anchor=CENTER)
        else:
            self.textoInf['text']='Seu cargo não permite\nutilizar essa função'
            self.textoInf['fg']='red'
            messagebox.showerror('Permissão insuficiente','Seu cargo nao permite utilizar essa função')

    def deletarDeletarUsuario_click(self):
        '''
        Se o usuário passado for existente ele irá apagado do dicionário e salvado no arquivo, se não irá dar uma mensagem de erro
        '''
        
        bd = ler_usuarios()
        if self.entDeletarUsuario.get() in bd:
            '''
            Se o usuario existir
            '''
            
            check = messagebox.askquestion("Deletar usuário", "Deseja mesmo deletar o usuário") #Abre uma janela e faz a confirmação se o usuário deve mesmo ser apagado
            if check == 'yes':
                del bd[self.entDeletarUsuario.get()] #Apaga o usuário do dicionário
                salvar_usuarios(bd) #Salvar no arquivo
                self.textoDeletarUsuario['text']='Usuario deletado com sucesso'
                self.textoDeletarUsuario['fg']='light green'
                '''
                Salvando no log
                '''
                            
                log = 'O usuario '+self.entDeletarUsuario.get()+' foi deletado.'

                log_exec(log,self.usuarioLogado[0])

                messagebox.showinfo('SUCESSO!!!','Usuário '+self.entDeletarUsuario.get()+' foi deletado.')
                
                self.entDeletarUsuario.delete(0,'end')

                

            else:
                self.entDeletarUsuario.delete(0,'end')
                self.textoDeletarUsuario['text']=''
                
        else:
            self.textoDeletarUsuario['text']='Este usuário não existe'
            self.textoDeletarUsuario['fg']='red'
            messagebox.showerror('Erro!!!','Usuário não existe')
                               

    def voltarDeletarUsuario_click(self):
        '''
        Fecha a janela deletar usuário e abre a janela principal
        '''
        
        self.janelas['janelaDeletarUsuario'].withdraw() 
        self.janelas['janelaPrincipal'].deiconify()
        self.textoPrincipal['text']='O que deseja fazer agora\n%s'%(self.usuarioLogado[1][1])
        self.textoInf['text']=''

    def gerarRelatorio_click(self):
        '''
        Cria um arquivo em txt com o relatório de todos os usuários cadastrados atualmente no banco de dados
        '''
        
        bd = ler_usuarios()
        gerar_relatorio(bd)
        self.textoInf['text']='Seu relatório foi\ngerido com sucesso'
        self.textoInf['fg']='light green'
        messagebox.showinfo('SUCESSO!!!','Seu relatório foi gerido com sucesso')
        '''
        Salvando no log
        '''
                            
        log = 'Gerou um relatório.'

        log_exec(log,self.usuarioLogado[0])
                

programa()
