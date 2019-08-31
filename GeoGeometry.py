from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt


##Works only for JSON because string spliting is different for Atom 

class Gml:
    
    def __init__(self, string):
        self.polygonCoordinates = self.getCoordinates(string)
        polygon1 = Polygon(self.polygonCoordinates)
        x,y = polygon1.exterior.xy
        plt.plot(x,y);
        #plt.show()
        
    ##Function for filling the list of polygon coordinates, takes the string and breaks it into coords
    def getCoordinates(self, string):
        s1 = '<gml:coordinates>'
        s2 = '</gml:coordinates>'
        firstIndex = string.find(s1) + len(s1)
        secondIndex = string.find(s2)-1

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
        point = Point(lat, long)
        if self.checkAntiMeridian(self.polygonCoordinates):
            polygon1, polygon2 = self.splitPolygon(self.polygonCoordinates)
            return polygon1.contains(point) or polygon2.contains(point)
                
        
        polygon = Polygon(self.polygonCoordinates)
        
        
        return polygon.contains(point)

    ##Function for checking if the given polygon is inside of the main polygon
    def polygonInsidePolygon(self, otherPolygon):
        return Polygon(self.polygonCoordinates).contains(otherPolygon)

    def checkAntiMeridian(self, coordsOfPolygon):
        needsSpliting = False
        hasEast = False
        hasWest = False
        for i in coordsOfPolygon:
            if i[1] < 180 and i[1] > 145:
                hasEast = True
                break
            
        for i in coordsOfPolygon:
            if  i[1] > -180 and i[1] < -145:
                hasWest = True
                break
            
        if hasEast and hasWest:
            needsSpliting = True

        return needsSpliting

    def splitPolygon(self, coordsOfPolygon):
        coordsEast = []
        coordsWest = []
        
        for i in coordsOfPolygon:
            if i[1] < 0:
                coordsWest.append(i)
            else:
                coordsEast.append(i)
                
                
            
        


        coordsWest.append(coordsWest[0])

        if len(coordsEast) < 3:
            coordsEast.append((coordsEast[0][0]-0.001, coordsEast[0][1]-0.001))
        if len(coordsWest) < 3:
            coordsWest.append((coordsWest[0][0]+0.001, coordsEast[0][1]+0.001))
##        print('poligon1')
##        print(coordsEast)
##        print()
##        print('poligon2')
##        print(coordsWest)

        return Polygon(coordsEast), Polygon(coordsWest)
