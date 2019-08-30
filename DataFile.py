from GeoGeometry import Gml
class DataFile:

    def __init__(self, data):
        self.id = data['Id']
        self.name = data['Name']
        self.value = data['__metadata']['media_src']
        self.polygon = Gml(data['ContentGeometry'])
        
        return

    
