from tkinter import *
from tkinter import messagebox
from turtle import title
from config import connect
import interface
import hashlib

####### Tela de login #######

print('[ OK ] Interfaces')  
janela = Tk()

janela.geometry('300x400+360+140')
janela.resizable(False, False)
janela.config(bg='#FFFFFF')
janela.title('Login')
janela.iconbitmap('.\images\icone.ico')

frm = Frame(janela, width=200, height=300,bg='#FFFFFF' )
frm.place(x=50, y=20)

img = PhotoImage(file='.\images\login1.png')
Label(frm, image=img, bg='#FFFFFF').place(x=50,y=10)


###### Entrada do usuario ######

lb_usuario = Label(frm, width=15, text='Usuário', fg='black', bg='#FFFFFF', font='Arial 9')
lb_usuario.place(x=18, y=130)
entr_usuario = Entry(frm, width=15, fg='black', border=0,font=('Arial',9))
entr_usuario.place(x=50, y=150)

Frame(frm, width=120, height=2, bg='black').place(x=50,y=170)


###### Entrada da senha ######

lb_senha = Label(frm, width=15, text='Senha', fg='black', bg='#FFFFFF', font='Arial 9')
lb_senha.place(x=13, y=190)

entr_senha = Entry(frm, width=15, fg='black', show='*', border=0,font=('Arial',9))
entr_senha.place(x=50, y=210)

Frame(frm, width=120, height=2, bg='black').place(x=50,y=230)


###### Botão Entrar ######
def MD5(password): #função criptografar senha no banco de dados       
        return hashlib.md5(password.encode("utf")).hexdigest()

def logar(): # função para validar login 
    usuario = entr_usuario.get()
    passw = MD5(entr_senha.get())

    if(usuario=='' or passw==''):
        messagebox.showerror(title='Erro', message='Campo usuário ou senha vazio!',)
    else:
        connect.cursor.execute("""
        SELECT * FROM Usuario WHERE(NAME = ? AND SENHA = ?)
        """,(usuario, passw))
        verificalogin = connect.cursor.fetchone()

        if(verificalogin):
                janela.destroy()
                interface.lock()
               
        else:
            messagebox.showerror(title='Erro Login', message='Usuário ou senha incorretos!')
         
    
        
btn_entrar = Button(frm, width=10, pady=5, text='Entrar', cursor='hand2', border=0, bg='#B8B8B8', font=('Arial',8), command=logar)
btn_entrar.place(x=40, y=270)



###### Botão Cadastrar ######

###### Tela de Cadastro ######
def window():
    janela.attributes('-alpha', 0)
    cad = Tk()
    cad.geometry('300x120+370+279')
    cad.resizable(False,False)
    cad.config(bg='#bdbebf')
    cad.title('Cadastro')
    cad.iconbitmap(r'.\images\user.ico')

    ###### Labels ######
    lbl_nome = Label(cad, width=15, text='Nome', fg='black', bg='#bdbebf', font='Arial 9 bold')
    lbl_nome.place(x=0, y=20)

    lbl_sen = Label(cad, width=15, text='Senha', fg='black', bg='#bdbebf', font='Arial 9 bold')
    lbl_sen.place(x=0, y=60)

    ###### Caixas de Entradas ######
    ent_nome = Entry(cad, width=15, fg='black', border=3 ,font=('Arial',9))
    ent_nome.place(x=80, y=20)

    ent_senha = Entry(cad, width=15, fg='black',  show= '*', border=3 ,font=('Arial',9))
    ent_senha.place(x=80, y=60)

    ###### Botões ######

    def cadastrar(): #função cadastrar usuario no banco de dados
        nome = ent_nome.get()
        senha = ent_senha.get()

        if(nome =='' or senha ==''):
            messagebox.showerror(title='Erro', message='Campo nome ou senha vazio!')
        else:
            query_verifica_usuario = "select * from Usuario;"
            verifica_usuario = connect.cursor.execute(query_verifica_usuario)

            if (bool(tuple(verifica_usuario))):
                messagebox.showwarning(title='Atenção!', message='Limite de usuários ultrapassado! Favor realizar login.')
            else:
                connect.cursor.execute("""
                    INSERT INTO Usuario(NAME, SENHA) VALUES(?, ?)
                    """, (nome, MD5(senha)))
                connect.conn.commit()
                messagebox.showinfo(title='Registro', message='Usuário cadastrado com sucesso!')
                ent_nome.delete(0,END)
                ent_senha.delete(0,END)
                # cad.destroy()
                #janela.attributes('-alpha', 1)
         
    def sair(): #função sair da tela de cadastro
     cad.destroy()
     janela.attributes('-alpha', 1)
    
    
    btn_cad = Button(cad, width=10, pady=2, text='Cadastre-se', cursor='hand2', relief='groove', bg='#3e6987', font='Arial 8 bold', command=cadastrar)
    btn_cad.place(x=210, y=20)

    btn_can = Button(cad, width=10, pady=2, text='Sair', cursor='hand2', relief='groove', bg='#3e6987', font='Arial 8 bold', command=sair)
    btn_can.place(x=210, y=60)
    cad.mainloop()
###### Fim da Tela Cadastro #####

btn_cadastrar = Button(frm, width=10, pady=5, text='Cadastrar', cursor='hand2', border=0, bg='#B8B8B8', font=('Arial',8), command=window)
btn_cadastrar.place(x=120, y=270)

janela.mainloop()

