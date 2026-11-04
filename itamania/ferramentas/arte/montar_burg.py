"""Cesar Burg (fotos do Pedro): prédio branco, moldura amarela grossa nas portas de vidro, piso xadrez e
letreiro azul "cesar burg". Peças do Modern Exteriors repintadas; moldura, xadrez e letreiro são desenho próprio.
Usado por ferramentas/mapas/gerar_praca.py (função gerar()).
"""
import colorsys, sys
from PIL import Image


def gerar():
    P='/home/user/itaverso/itamania/referencias/licenciados/modern-exteriors/'
    M=P+'ME_Theme_Sorter_16x16/5_Floor_Modular_Building_Singles_16x16/ME_Singles_Floor_Modular_Building_16x16_'
    ld=lambda f: Image.open(f).convert('RGBA')

    def branco(im, vidro_ok=True):
        """Paredes viram branco/cinza bem claro (mantém luz e sombra); vidro fica azul-claro vivo."""
        im=im.copy(); px=im.load()
        for y in range(im.height):
            for x in range(im.width):
                r,g,b,a=px[x,y]
                if a==0: continue
                h,l,s=colorsys.rgb_to_hls(r/255,g/255,b/255)
                vidro = vidro_ok and b>r+25 and b>g and l>0.45
                if vidro:
                    rr,gg,bb=colorsys.hls_to_rgb(0.56,min(0.88,0.55+l*0.4),0.75)
                    px[x,y]=(int(rr*255),int(gg*255),int(bb*255),a)
                elif 0.36<l<0.85 and s<0.45:
                    v=int(min(250,150+l*120)); px[x,y]=(v,v,min(255,v+4),a)
        return im

    telhado=branco(ld(M+'Roof_10.png'), vidro_ok=False)
    for nome,pos in (('Roof_Props_8',(10,18)),('Roof_Props_9',(66,30))):
        telhado.alpha_composite(ld(M+nome+'.png'),pos)
    andar=branco(ld(M+'Middle_Floor_13.png'))
    terreo=branco(ld(M+'Ground_Floor_Condo_9.png'))
    W=terreo.width

    # portas de vidro: acha as regiões azuis do térreo e põe a moldura amarela e o piso xadrez por dentro
    AM=(255,196,28,255); AM2=(255,224,90,255); AZ=(52,92,232,255); AZ2=(30,52,160,255)
    px=terreo.load()
    # vão das portas (fixo): de x 10 a 101, do alto da faixa até o chão
    x0,y0,x1,y1=10,12,101,terreo.height-3
    # miolo: interior claro com piso xadrez embaixo, pilar branco no meio, moldura amarela grossa em volta
    for y in range(y0+3,y1+1):
        for x in range(x0+3,x1-2):
            if y>y1-5:
                px[x,y]=(250,250,250,255) if ((x//2)+(y//2))%2==0 else (34,34,40,255)
            else:
                px[x,y]=(206,236,250,255) if (x+y)%7 else (236,248,255,255)
    meio=(x0+x1)//2
    for y in range(y0+3,y1+1):
        for x in range(meio-2,meio+3): px[x,y]=(244,244,248,255) if x<meio+2 else (214,214,222,255)
    for y in range(y0,y1+1):
        for x in range(x0,x1+1):
            borda = x<x0+3 or x>x1-3 or y<y0+3
            if borda: px[x,y]= AM2 if (y==y0 or x==x0) else AM

    # letreiro azul "cesar burg" (letras minúsculas arredondadas, 4x5) na faixa branca acima das portas
    # letras grossas 5x6, minúsculas e arredondadas como o logo
    F={'c':['01110','11000','11000','11000','11000','01110'],'e':['01110','11011','11111','11000','11000','01111'],
       's':['01111','11000','01110','00011','00011','11110'],'a':['01110','00011','01111','11011','11011','01111'],
       'r':['11110','11011','11000','11000','11000','11000'],'b':['11000','11000','11110','11011','11011','11110'],
       'u':['11011','11011','11011','11011','11011','01111'],'g':['01111','11011','11011','01111','00011','11110'],
       ' ':['000','000','000','000','000','000']}
    txt='cesar burg'
    larg=sum(len(F[c][0])+1 for c in txt)-1
    img=Image.new('RGBA',(W,telhado.height+andar.height+terreo.height+12),(0,0,0,0))
    y=0
    img.alpha_composite(telhado,(0,y)); y+=telhado.height
    img.alpha_composite(andar,(0,y)); y+=andar.height
    img.alpha_composite(terreo,(0,y)); yt=y; y+=terreo.height
    lx=W//2-larg//2; ly=yt+y0-9
    for c in txt:
        for j,lin in enumerate(F[c]):
            for i,v in enumerate(lin):
                if v=='1':
                    img.putpixel((lx+i,ly+j),AZ)
                    if img.getpixel((lx+i,ly+j+1))[:3]!=AZ[:3]: img.putpixel((lx+i,ly+j+1),AZ2)
        lx+=len(F[c][0])+1

    return img
