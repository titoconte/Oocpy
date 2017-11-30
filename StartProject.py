
import sys
import os

def main(root):

    MainDir = os.path.join(root,'Operacao','Tratamento_e_Analise')
    Produtos = os.path.join(root,'Produtos')
    os.makedirs(MainDir,'Figuras','MetOcean','Correntes')
    os.makedirs(MainDir.replace('Tratamento_e_Analise','Docs'),'Relatorio')
    os.makedirs(MainDir,'Figuras','MetOcean','Densidade')
    os.makedirs(MainDir,'Figuras','Deposicao')
    os.makedirs(MainDir,'Figuras','Pluma')
    os.makedirs(MainDir,'Sig','Resultados','Individuais')
    os.makedirs(MainDir,'Sig','Resultados','Somas')
    os.makedirs(MainDir,'Sig','Resultados','Integrados')
    os.makedirs(MainDir,'Sig','PontoDeModelagem')
    os.makedirs(MainDir,'Diagnosticos')
    os.makedirs(MainDir,'Scripts')
    os.makedirs(MainDir,'Loc_Data')
    os.makedirs(Produtos,'Documento')
    os.makedirs(Produtos,'Ilustracoes')
    os.makedirs(Produtos,'Shapes')

if __name__ == '__main__':
    main()
