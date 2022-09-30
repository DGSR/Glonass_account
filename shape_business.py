import simplekml
import json


geo_json = "{\"type\":\"MultiLineString\"," \
           "\"coordinates\":[[[30.321794,59.986508],[30.30937,59.988583]," \
           "[30.303018,59.986573],[30.301237,59.985541]]]}"
poi = "{\"type\":\"Point\",\"coordinates\":[30.320849,59.986325]}"
metro = "{\"type\":\"Point\",\"coordinates\":[30.321772,59.986626]}"
poly = "{\"type\":\"MultiPolygon\"," \
       "\"coordinates\":[[[[30.321836,59.986616],[30.32101,59.986637]," \
       "[30.32027,59.986879],[30.320356,59.987212]," \
       "[30.320656,59.987508],[30.322287,59.987263]," \
       "[30.321836,59.986616]]]]}"


def main():
    kml = simplekml.Kml()
    data = json.loads(geo_json)
    data1 = json.loads(poi)
    data2 = json.loads(metro)
    data3 = json.loads(poly)
    print(data1['coordinates'])
    kml.newlinestring(name="Name", coords=data['coordinates'][0])
    kml.newpoint(name="POI", coords=[data1["coordinates"]])
    kml.newpoint(name="Metro", coords=[data2["coordinates"]])
    kml.newpolygon(name='Poly', outerboundaryis=data3["coordinates"][0][0])
    kml.save('t.kml')


if __name__ == '__main__':
    main()
