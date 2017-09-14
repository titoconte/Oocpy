
import os


__all__ = ['GetCoastPolygon','GetUFLine']

module_path = os.path.dirname(__file__)

def GetCoastPolygon():
        return os.path.abspath(
            os.path.join(module_path,'brasil_UF.shp'))
def GetUFLine():
        return os.path.abspath(
            os.path.join(
                module_path,
                'Linha_Divisas_municipais_Litoraneos_TODOBRASIL.shp')
            )
