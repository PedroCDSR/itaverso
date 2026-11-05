"""Recortes exclusivos da missão lateral. Não modifica nenhum asset da praça.

Peças de fachadas: Modern Exteriors/LimeZu, licença registrada em CREDITS.md.
Igreja: desenho original já existente no projeto. Fonte, concha, toldo e fichas: desenho próprio.
"""
from pathlib import Path
from PIL import Image, ImageDraw

RAIZ = Path(__file__).resolve().parents[2]
OBJ = RAIZ / 'public/assets/limezu/objetos'
DESTINO = RAIZ / 'public/assets/missao-urbana'
DESTINO.mkdir(parents=True, exist_ok=True)

def abrir(nome):
    return Image.open(OBJ / (nome + '.png')).convert('RGBA')

def salvar(im, nome):
    im.save(DESTINO / (nome + '.png'), optimize=True)

def repintar(im, cor):
    # Preserva luminosidade, detalhes e contornos das peças originais.
    im = im.copy()
    for y in range(im.height):
        for x in range(im.width):
            r,g,b,a = im.getpixel((x,y))
            if a and max(r,g,b)-min(r,g,b) < 52 and r > 108:
                luz = (r+g+b)/3/220
                im.putpixel((x,y), tuple(min(255,round(c*luz)) for c in cor)+(a,))
    return im

# Remove telhados vistos de cima. Na lateral só a fachada e a cornija ficam visíveis.
clube = abrir('clube')
clube = clube.crop((0, 32, clube.width, clube.height))
im = Image.new('RGBA', (clube.width, clube.height+28))
im.alpha_composite(clube, (0,28)); d=ImageDraw.Draw(im)
d.polygon([(4,27),(clube.width//2,1),(clube.width-4,27)], fill='#d3c5a7', outline='#746e68')
d.line([(6,25),(clube.width//2,5),(clube.width-6,25)], fill='#fff2d5', width=3)
d.rectangle((8,26,clube.width-8,30),fill='#eee2c4')
salvar(im,'clube')

cafe=abrir('cafe'); salvar(cafe.crop((0,72,cafe.width,cafe.height-14)),'cafe')
hotel=abrir('hotel'); hotel=hotel.crop((0,32,hotel.width,hotel.height))
salvar(repintar(hotel,(225,209,176)),'sobrado')
loja=abrir('sob_s8'); salvar(loja.crop((0,28,loja.width,loja.height)),'loja')

# Sobrados da rua: montagem de janela existente sobre alvenaria e molduras.
janela=hotel.crop((14,6,35,27))
def casarao(nome,cor,moldura,largura=184,pedra=False):
    im=Image.new('RGBA',(largura,112)); d=ImageDraw.Draw(im)
    d.rectangle((1,4,largura-2,110),fill=cor,outline='#635f5f')
    d.rectangle((0,0,largura-1,5),fill='#f0e4cf',outline='#847e79')
    d.line((0,7,largura,7),fill='#fff5df',width=2)
    for x in range(14,largura-20,33):
        d.rectangle((x-3,23,x+23,69),fill=moldura)
        im.alpha_composite(janela.resize((19,39),Image.Resampling.NEAREST),(x+1,26))
        d.line((x-2,70,x+24,70),fill='#fff0d5',width=2)
    d.rectangle((2,80,largura-3,111),fill='#a79e8a' if pedra else cor)
    if pedra:
        for y in range(81,112,8):
            d.line((2,y,largura-3,y),fill='#6c706e')
            for x in range((y//8%2)*10,largura,20):
                d.line((x,y,x-2,y+8),fill='#77766d')
                d.line((x+2,y+2,x+14,y+2),fill='#c5b99d')
    else:
        d.line((2,81,largura-3,81),fill=moldura,width=2)
        for x in range(10,largura,44): d.rectangle((x,88,x+29,104),outline=moldura,width=2)
    salvar(im,nome)
casarao('verde','#c2cfb3','#eee8d8')
casarao('azul','#9cc6de','#f1ebdc')
casarao('brancoazul','#e1e4d9','#355c90',240,True)

im=Image.new('RGBA',(152,168)); d=ImageDraw.Draw(im)
d.rectangle((1,1,150,167),fill='#aa775b',outline='#675953')
for y in range(4,150,5):
    d.line((2,y,149,y),fill='#cfab83')
    for x in range((y//5%2)*7,150,14):d.line((x,y,x,y+5),fill='#765b51')
for y in [23,62]:
    for x in [18,65,112]:
        d.rectangle((x-2,y-2,x+22,y+26),fill='#454c59')
        d.rectangle((x+1,y+1,x+19,y+23),fill='#8ca9bd')
        d.line((x,y+11,x+20,y+11),fill='#414756',width=2)
d.rectangle((0,101,151,109),fill='#695f59')
d.rectangle((2,110,149,163),fill='#484c54')
for x in range(6,150,48):
    d.rectangle((x,115,x+40,160),fill='#83a4b2',outline='#d6c7ac',width=3)
    d.line((x+3,146,x+37,121),fill='#bad1d5',width=2)
salvar(im,'tijolos')

im=Image.new('RGBA',(144,88));d=ImageDraw.Draw(im)
d.pieslice((1,1,142,161),180,360,fill='#c4b899',outline='#786f68',width=2)
d.pieslice((8,8,135,158),180,360,fill='#e8dcc2',outline='#f4ebd8',width=3)
d.pieslice((16,16,127,155),180,360,fill='#9f9486',outline='#c9bda4',width=2)
d.rectangle((0,77,143,87),fill='#b6aa91',outline='#756f66')
d.line((4,79,140,79),fill='#f1e6ce',width=2)
salvar(im,'concha')

im=Image.new('RGBA',(144,64));d=ImageDraw.Draw(im)
d.ellipse((0,40,143,63),fill='#8c969b',outline='#586a78',width=2)
d.ellipse((6,42,137,56),fill='#6caec4',outline='#d2dce0',width=2)
for x in [20,45,72,99,124]:
    d.arc((x-16,8,x+16,53),180,360,fill='#e1f4ed',width=2)
    d.line((x-16,30,x-16,48),fill='#8bc7d5')
d.rectangle((69,18,75,51),fill='#bcc6c6')
d.ellipse((54,14,89,24),fill='#d0d9d1',outline='#6e8087')
d.line((72,2,72,15),fill='#efffff',width=2)
salvar(im,'fonte')

im=Image.open(RAIZ/'public/assets/cenario/igreja.png').convert('RGBA');salvar(im,'igreja')

im=Image.new('RGBA',(112,24));d=ImageDraw.Draw(im)
d.polygon([(0,2),(111,2),(105,16),(5,16)],fill='#bb5842',outline='#603b3d')
for x in range(8,112,16):d.polygon([(x,3),(x+7,3),(x+3,15),(x-4,15)],fill='#f5cc78')
d.rectangle((4,16,107,20),fill='#d37a51')
d.line((4,2,108,2),fill='#f8dea2',width=2)
salvar(im,'toldo')

for nome,tamanho in [('ficha',12),('estrela',20)]:
    im=Image.new('RGBA',(tamanho,tamanho));d=ImageDraw.Draw(im)
    if nome=='ficha':
        d.polygon([(3,0),(8,0),(11,3),(11,8),(8,11),(3,11),(0,8),(0,3)],fill='#f1c75d',outline='#8e633b')
        d.polygon([(6,2),(9,6),(6,9),(3,6)],fill='#fff2b1',outline='#c6923f')
    else:
        d.polygon([(10,0),(13,6),(19,7),(15,12),(16,19),(10,16),(4,19),(5,12),(0,7),(7,6)],fill='#ffdc77',outline='#a4733e')
        d.line([(10,3),(12,8),(16,9)],fill='#fff5c6',width=2)
    salvar(im,nome)
print('Assets urbanos gerados em', DESTINO)
