"""Café do Vadinho (foto do Pedro): fachada creme com venezianas brancas, térreo aberto e escuro, toldo escuro
com a placa oval e mesinhas de madeira na calçada. Peças do Modern Exteriors repintadas; só a placa é desenho próprio.
Usado por ferramentas/mapas/gerar_praca.py (função gerar()).
"""
import colorsys, sys
from PIL import Image, ImageDraw


def gerar():
    P='/home/user/itaverso/itamania/referencias/licenciados/modern-exteriors/'
    M=P+'ME_Theme_Sorter_16x16/5_Floor_Modular_Building_Singles_16x16/ME_Singles_Floor_Modular_Building_16x16_'
    C=P+'Modern_Exteriors_Complete_Singles_16x16/'
    ld=lambda f: Image.open(f).convert('RGBA')

    def creme(im):
        """Repinta paredes cinzas/azuladas de creme, mantendo luz e sombra; vidro, contorno e detalhes ficam."""
        im=im.copy(); px=im.load()
        for y in range(im.height):
            for x in range(im.width):
                r,g,b,a=px[x,y]
                if a==0: continue
                h,l,s=colorsys.rgb_to_hls(r/255,g/255,b/255)
                if s<0.28 and 0.30<l<0.80:
                    nl=min(0.93,0.42+l*0.62)
                    rr,gg,bb=colorsys.hls_to_rgb(0.12,nl,0.42)
                    px[x,y]=(int(rr*255),int(gg*255),int(bb*255),a)
        return im

    def escuro(im):
        """Toldo: madeira vira lona grafite."""
        im=im.copy(); px=im.load()
        for y in range(im.height):
            for x in range(im.width):
                r,g,b,a=px[x,y]
                if a==0: continue
                l=(r*0.3+g*0.59+b*0.11)/255
                v=int(30+l*70); px[x,y]=(v,v,int(v*1.05),a)
        return im

    telhado=ld(M+'Roof_5.png')
    andar=creme(ld(M+'Middle_Floor_17.png'))


    def veneziana(im):
        # vidro azul das janelas vira veneziana branca (listras horizontais), como no andar de cima do café na foto
        im=im.copy(); px=im.load()
        for y in range(im.height):
            for x in range(im.width):
                r,g,b,a=px[x,y]
                if a and b>r+25 and b>g+5:
                    v=236 if y%2==0 else 214
                    px[x,y]=(v,v,v-4,a)
        return im


    andar=veneziana(andar)
    terreo=creme(ld(M+'Ground_Floor_Condo_9.png'))


    def aberto(im):
        # térreo aberto e escuro, como na foto: o vidro vira o interior em sombra
        im=im.copy(); px=im.load()
        for y in range(im.height):
            for x in range(im.width):
                r,g,b,a=px[x,y]
                if a and b>r+15:
                    v=int(34+(r+g+b)/3*0.18)
                    px[x,y]=(v,v-2,v-4,a)
        return im


    terreo=aberto(terreo)
    W=telhado.width
    H=telhado.height+andar.height+terreo.height+40
    img=Image.new('RGBA',(W+40,H),(0,0,0,0))
    y=0
    img.alpha_composite(telhado,(20,y)); y+=telhado.height
    img.alpha_composite(andar,(20,y)); y+=andar.height
    img.alpha_composite(terreo,(20,y)); yt=y; y+=terreo.height
    # toldo escuro na frente do térreo: faixa de lona (borda de cima + borda da frente do toldo do pacote) e um poste à
    # direita até a calçada, como na foto
    tor=escuro(ld(C+'24_Additional_Houses_Terraced_House_Canopy_16x16.png'))
    faixa=Image.new('RGBA',(114,18),(0,0,0,0))
    faixa.alpha_composite(tor.crop((4,12,118,22)),(0,0)); faixa.alpha_composite(tor.crop((4,32,118,40)),(0,10))
    poste=tor.crop((8,44,16,52))
    ty=yt-6
    img.alpha_composite(faixa,(20 + W - 114 - 1, ty))
    for py in range(ty+18, yt+terreo.height+4, 8):
        img.alpha_composite(poste,(20+W-8, py))
    # placa oval preta com o nome (única peça desenhada por nós: letras de 3x5)
    F={'C':['111','100','100','100','111'],'a':['000','011','101','101','011'],'f':['011','100','110','100','100'],'é':['010','111','101','110','011'],
       'd':['001','001','011','101','011'],'o':['000','010','101','101','010'],'V':['101','101','101','101','010'],'i':['1','0','1','1','1'],
       'n':['000','110','101','101','101'],'h':['100','100','110','101','101'],' ':['0','0','0','0','0']}
    txt='Café do Vadinho'
    larg=sum(len(F[c][0])+1 for c in txt)-1
    ow,oh=larg+10,11
    ox,oy=20+W//2-ow//2, ty+4
    d=ImageDraw.Draw(img)
    d.ellipse((ox,oy,ox+ow,oy+oh),fill=(22,22,26,255),outline=(70,70,76,255))
    x=ox+5
    for c in txt:
        for j,lin in enumerate(F[c]):
            for i,v in enumerate(lin):
                if v=='1': img.putpixel((x+i,oy+3+j),(240,232,212,255))
        x+=len(F[c][0])+1
    # calçada: mesinhas e cadeiras de madeira, vaso e cardápio
    mesa=ld(C+'21_Beach_16x16_Ship_Bar_Table.png'); cad=ld(C+[f for f in __import__('os').listdir(C) if 'Ship_Bar_Chair' in f][0])
    vaso=ld(C+'24_Additional_Houses_Terraced_House_Potted_Plant_16x16.png')
    quadro=ld(C+[f for f in sorted(__import__('os').listdir(C)) if 'Camping_16x16_Wood_Board' in f][1])
    base=y+20
    img2=Image.new('RGBA',(img.width,base+4),(0,0,0,0)); img2.alpha_composite(img); img=img2
    img.alpha_composite(vaso,(20,base-vaso.height))
    for mx in (40,84):
        img.alpha_composite(cad,(mx-cad.width-1,base-cad.height-1)); img.alpha_composite(mesa,(mx,base-mesa.height)); img.alpha_composite(cad,(mx+mesa.width+1,base-cad.height-1))
    img=img.crop(img.getbbox())

    return img
