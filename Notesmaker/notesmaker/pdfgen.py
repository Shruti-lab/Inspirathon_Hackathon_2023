import asyncio
from fpdf import FPDF
title='Notes'

class PDF(FPDF):
    def header(self):
        self.image('./static/images/logo.png',5,5,30)
        #setting title in middle
        doc_w= self.w
        self.set_x((doc_w - 20)/2)

        #font
        self.set_font('helvetica','B',20)
        #padding self.cell(80)
        #title
        self.set_draw_color(0,80,180) #border
        self.set_text_color(220,50,50)
        self.set_line_width(1)
        self.cell(25,10,title,border=True,ln=1,align='C')
        #line break
        self.ln(10)
        
    def footer(self):
        #set position of footer
        self.set_y(-15)
        self.set_font('helvetica','I',10)
        #set page number
        self.cell(0,10,f'Page{self.page_no()}/{{nb}}',align='C')

    def chapter_body(self,txt):
        # with open(name,'rb') as fh:
        #     txt=fh.read().decode('latin-1')

        self.set_font('times','',15)
        self.multi_cell(0,10,txt[:len(txt)//2])
        #line break
        self.ln()
        self.image('board0.png')
        self.ln()
        self.image('board1.png')
        self.ln()
        self.multi_cell(0,10,txt[len(txt)//2:])
        self.ln()
        self.image('board2.png')
        self.ln()
        self.image('board3.png')


def generatepdf(text):
    #create pdf object
    #layout('P'->potrait,'L'->landscape)
    #unit('mm','cm','in')
    #format('A3','A4'(default),'A5','Letter','Legal',(100,150))
    pdf=PDF('P','mm','Letter')
    pdf.set_auto_page_break(auto=True, margin = 15)
    pdf.alias_nb_pages()

    #add page
    pdf.add_page()

    # specify fonts ('times','couries','helvetica','symbol','zpfdingbats')
    #'B'->bold, 'U'->underline , 'I'->Italics, ''->regular, combination ->('BU')
    pdf.chapter_body(text)

    #add text
    #w=>width, h->height


    # for i in range(1,50):
    #     pdf.cell(0,10,f'This is line {i}',ln=True)
    pdf.output('static/notes.pdf')

if __name__=='__pdf__':
    generatepdf()