
import sys
import os

def StartProject():

    root = input('Entre com o diretorio onde o projeto sera iniciado: ')
    MainDir = os.path.join(root,'Operacao','Tratamento_e_Analise')
    Produtos = os.path.join(root,'Produtos')
    os.makedirs(os.path.join(
        MainDir,
        'Figuras',
        'MetOcean',
        'Correntes'
        ))
    os.makedirs(os.path.join(
        MainDir.replace('Tratamento_e_Analise','Docs'),
        'Relatorio'
        ))
    os.makedirs(os.path.join(
        MainDir,
        'Figuras',
        'MetOcean',
        'Densidade'
        ))
    os.makedirs(os.path.join(
        MainDir,
        'Figuras',
        'Deposicao'
        ))
    os.makedirs(os.path.join(
        MainDir,
        'Figuras',
        'Pluma'
        ))
    os.makedirs(os.path.join(
        MainDir,
        'Sig',
        'Resultados',
        'Individuais'
        ))
    os.makedirs(os.path.join(
        MainDir,
        'Sig',
        'Resultados',
        'Somas'
        ))
    os.makedirs(os.path.join(
        MainDir,
        'Sig',
        'Resultados',
        'Integrados'
        ))
    os.makedirs(os.path.join(
        MainDir,
        'Sig',
        'PontoDeModelagem'
        ))
    os.makedirs(os.path.join(
        MainDir,
        'Diagnosticos'
        ))
    os.makedirs(os.path.join(
        MainDir,
        'Scripts'
        ))
    os.makedirs(os.path.join(
        MainDir,
        'Loc_Data'
        ))
    os.makedirs(os.path.join(
        Produtos,
        'Documento'
        ))
    os.makedirs(os.path.join(
        Produtos,
        'Ilustracoes'
        ))
    os.makedirs(os.path.join(
        Produtos,
        'Shapes'
        ))

if __name__ == '__main__':

    StartProject()
