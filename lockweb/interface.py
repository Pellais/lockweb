#importação do Tkinter -------------------
from asyncio.windows_events import NULL
from dataclasses import replace
from email.policy import default
from gettext import find
from tkinter import*
from tkinter import Tk, StringVar, ttk
from tkinter import messagebox
from re import sub
from config import connect




def lock():
    #importação para csv
    import csv

    #colors ---------------------------------
    co0 = "#000000"   # preta
    co1 = "#feffff"   # branca
    co2 = "#3fb5a3"   # verde
    co3 = "#fc766d"   # vermelha / red
    co4 = "#403d3d"   # letra
    co5 = "#4a88e8"   # azul/blue

    #criando janela 
    janela = Tk ()
    janela.geometry('333x470+360+140')
    janela.config(background=co1)
    janela.resizable(width=FALSE, height=FALSE)
    janela.title('Lockweb v1.2')

    ###### Definindo funções ######
    global iniciar
    
    iniciar = BooleanVar()

    # Função ver site
    def exibir():
        lista.delete(0, END)
        # Acessando arquivo csv
        with open('.\config\sites.csv') as file:
            ler = csv.reader(file)
            for x in ler:
                lista.insert(END, x)

    # Função salvar site
    def salvar_site(i):
        url = str(i)
        treated_url = url
        protocols_to_block = ['http', 'https']

        for protocol in protocols_to_block:
            if(url.find(protocol) > -1):
                treated_url = url.replace(protocol, '')
                treated_url = sub('[^A-Za-z0-9.]+', '', treated_url)

        if treated_url.find("://") == -1:
            #Acessando arquivo csv
            treated_url = sub('[^A-Za-z0-9.]+', '', treated_url)


            with open('.\config\sites.csv', 'r') as file:
                site_to_check = file.readlines()
                treated_site_to_check = []

                for site in site_to_check:
                    treated_site_to_check.append(site.replace('\n', ''))

            if treated_url in treated_site_to_check:
                messagebox.showerror(title='Erro', message='Este site já existe!')
                e_site.delete(0, END)
            elif treated_url == '':
                messagebox.showerror(title='Erro', message='Você inseriu apenas caracteres proibidos, insira uma url.')
            else:
                with open('.\config\sites.csv', 'a+', newline='') as file2:
                    w = csv.writer(file2)
                    w.writerow([treated_url])
        else:
            messagebox.showerror(title='Erro', message='Digite apenas sites HTTP/HTTPS.')

    # Função adicionar site à lista
    def adicionar():
        url = e_site.get()

        if url == '':
            messagebox.showerror(title='Erro', message='O campo está vázio, digite um domínio ou url completa do site!')
            e_site.delete(0, END)
                
        else:
            e_site.delete(0, END)
            salvar_site(url)
            exibir()

    # Função remover site csv
    def excluir_csv(l):

        def incluir(l):
            #Acessando arquivo csv
            with open('.\config\sites.csv', 'w', newline='') as file:
                w = csv.writer(file)
                w.writerows(l)
            exibir()
        nv_lista = []
        with open('.\config\sites.csv','r') as file:
            r = csv.reader(file)
            for z in r:
                nv_lista.append(z)
                for campo in z:
                    if(campo==l):
                        nv_lista.remove(z)
        incluir(nv_lista)

    # Função remover site
    def remover():
        elemento = lista.get(ACTIVE)
        sites =[]
        for y in elemento:
            sites.append(y)
        excluir_csv(sites[0])

    # Função bloqueador 
    def bloqueador():
        # Caminho do arquivo
        local = r'C:\Windows\System32\drivers\etc\hosts'
        redirecionar = '127.0.0.1'
        websites = []

        # Acessando arquivo csv
        with open('.\config\sites.csv') as file:
            ler_csv = csv.reader(file)
            for s in ler_csv:
                websites.append(s[0])
        
        if(iniciar.get()==True):
            with open(local, 'r+') as arquivo:
                conteudo = arquivo.read()
                for site in websites:
                    if(site in conteudo):
                        pass
                    else:
                        arquivo.write(redirecionar +'   '+site+'\n')
        else:
            with open(local, 'r+') as arquivo:
                conteudo = arquivo.readlines()
                arquivo.seek(0)
                for line in conteudo:
                    if not any(site in line for site in websites):
                        arquivo.write(line)
                arquivo.truncate()

    # Função bloquear
    def bloquear_site():
        iniciar.set(True)
        messagebox.showinfo(title='Info', message='Sites da lista bloqueados! Para que as alterações façam efeito, renicie seu navegador.')
        bloqueador()

    # Função Desbloquear
    def desbloquear_site():
        iniciar.set(False)
        messagebox.showinfo(title='Info', message='Sites da lista desbloqueados!')
        bloqueador()

    #### Frames ###### 
    frame_logo = Frame(janela,width=400, height=70, bg=co1, relief="flat")
    frame_logo.grid(row=0, column=0,pady=1, padx=0, sticky=NSEW)

    frame_corpo = Frame(janela,width=0, height=400,bg=co1, relief="flat")
    frame_corpo.grid(row=1, column=0,pady=1, padx=0, sticky=NSEW)

    #### Logo ######
    logo = PhotoImage(file=r'.\images\logor.png')
    Label(frame_logo,image=logo,background=co1).place(x=43, y=0)

    fonte = PhotoImage(file=r'.\images\font.png')
    Label(frame_logo, image=fonte, background=co1).place(x=106,y=15)

    l_linha = Label(frame_logo, text='',width=400, height=1, anchor=NW, bg=co0)
    l_linha.place(x=0, y=67)

    ##### Caixa de Texto, label e botão ######
    l_site = Label(frame_corpo, text='*Digite o site que deseja bloquear:', height=1, anchor=NE, font=('Ivy 11 bold'), bg=co1, fg=co4)
    l_site.place(x=1, y=10)

    e_site = Entry(frame_corpo, width=20, justify='left' , font=('' , 15), highlightthickness=1, relief=SOLID)
    e_site.place(x=11, y=42)

    b_adicionar = Button(frame_corpo,text="Adicionar", command=adicionar, height=1, bg=co5, fg=co1, font=('Ivy 10 bold'), relief=RAISED, overrelief=RIDGE, cursor='hand2')
    b_adicionar.place(x=240, y=42)
    
    #### Listbox e botões ######
    lista = Listbox(frame_corpo, font=('Arial 9 bold'),width=43,height=15, highlightthickness=1, relief=SOLID)
    lista.place(x=11, y=80)

    b_bloquear = Button(frame_corpo, text='Bloquear', command=bloquear_site, height=1, font=('Ivy 10 bold'), relief=RAISED, overrelief=RIDGE, bg=co0, fg=co1, cursor='hand2')
    b_bloquear.place(x=20, y=340)

    b_desbloquear = Button(frame_corpo,text='Desbloquear', command=desbloquear_site, height=1, font=('Ivy 10 bold'), relief=RAISED, overrelief=RIDGE, bg=co2, fg=co1, cursor='hand2')
    b_desbloquear.place(x=120, y=340)

    b_remover = Button(frame_corpo, text='Remover', command=remover, height=1, font=('Ivy 10 bold'), relief=RAISED, overrelief=RIDGE, bg=co3, fg=co1, cursor='hand2')
    b_remover.place(x=240, y=340)

    exibir()

    janela.mainloop ()
