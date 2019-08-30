from shapely.geometry import Point, Polygon

##Works only for JSON because string spliting is different for Atom 

class Gml:
    
    def __init__(self, string):
        self.polygonCoordinates = self.getCoordinates(string)
        
    ##Function for filling the list of polygon coordinates, takes the string and breaks it into coords
    def getCoordinates(self, string):
        s1 = '<gml:coordinates>'
        s2 = '</gml:coordinates>'
        firstIndex = string.find(s1) + len(s1)
        secondIndex = string.find(s2)

        stringCoords =  string[firstIndex:secondIndex].split(' ')
        listOfCoordsTuples = []

     
        for i in stringCoords:
            listOfCoords = []
            tempCoord = i.split(',')
            
            lat = float(tempCoord[0])
            long = float(tempCoord[1])
            
            listOfCoords.append(lat)
            listOfCoords.append(long)
            
            listOfCoordsTuples.append(tuple(listOfCoords))
        
                   
        return listOfCoordsTuples

    
    
    ##Function for checking if the given coordinate is inside of the polygon
    def coordInsidePolygon(self, lat, long):
        polygon = Polygon(self.poygonCoordinates)
        point = Point(lat, long)
        
        return polygon.contains(point)

    ##Function for checking if the given polygon is inside of the main polygon
    def polygonInsidePolygon(self, otherPolygon):
    
        return Polygon(self.poygonCoordinates).contains(otherPolygon)
