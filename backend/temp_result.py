from datetime import datetime

from backend.google_api.google_route_objects import RouteLeg, RouteLegTransitLine, RouteLegTransitAgency, ResponseBody, \
    Route

result = ResponseBody(origin_address='University of Southern Denmark, SDU', destination_address='ZOB Hamburg',
                      routes=[Route(
                          legs=[RouteLeg(departure_place_name='Campus Odense (Odense Letbane)',
                                         arrival_place_name='Odense Banegård (Odense Letbane)',
                                         departure_datetime=datetime(2024, 1, 15, 16, 48),
                                         arrival_datetime=datetime(2024, 1, 15, 17, 6),
                                         transit_line=RouteLegTransitLine(line_name='L', vehicle_type='Tram',
                                                                          transit_agencies=[
                                                                              RouteLegTransitAgency(
                                                                                  name='Odense Letbane',
                                                                                  uri='https://www.odenseletbane.dk/')]),
                                         price=None),
                                RouteLeg(departure_place_name='Odense st - Gleis 3', arrival_place_name='Fredericia',
                                         departure_datetime=datetime(2024, 1, 15, 17, 10),
                                         arrival_datetime=datetime(2024, 1, 15, 17, 38),
                                         transit_line=RouteLegTransitLine(line_name='ICL', vehicle_type='Train',
                                                                          transit_agencies=[
                                                                              RouteLegTransitAgency(name='DSB',
                                                                                                    uri='http://www.dsb.dk/')]),
                                         price=None),
                                RouteLeg(departure_place_name='Fredericia', arrival_place_name='Flensburg / Flensborg',
                                         departure_datetime=datetime(2024, 1, 15, 17, 45),
                                         arrival_datetime=datetime(2024, 1, 15, 19, 7),
                                         transit_line=RouteLegTransitLine(line_name='IC', vehicle_type='Train',
                                                                          transit_agencies=[
                                                                              RouteLegTransitAgency(
                                                                                  name='Dänische Staatsbahnen',
                                                                                  uri='https://www.thetrainline.com/de/bahnunternehmen/dsb'),
                                                                              RouteLegTransitAgency(name='DSB',
                                                                                                    uri='http://www.dsb.dk/')]),
                                         price=None),
                                RouteLeg(departure_place_name='Flensburg / Flensborg', arrival_place_name='Hamburg Hbf',
                                         departure_datetime=datetime(2024, 1, 15, 19, 15),
                                         arrival_datetime=datetime(2024, 1, 15, 21, 17),
                                         transit_line=RouteLegTransitLine(line_name='RE7', vehicle_type='Train',
                                                                          transit_agencies=[
                                                                              RouteLegTransitAgency(name='DB Regio AG',
                                                                                                    uri='http://www.bahn.de/'),
                                                                              RouteLegTransitAgency(
                                                                                  name='Hamburger Verkehrsverbund (hvv)',
                                                                                  uri='http://www.hvv.de/')]),
                                         price=None)]),
                          Route(legs=[RouteLeg(departure_place_name='Campus Odense (Odense Letbane)',
                                               arrival_place_name='Odense Banegård (Odense Letbane)',
                                               departure_datetime=datetime(2024, 1, 15, 16, 48),
                                               arrival_datetime=datetime(2024, 1, 15, 17, 6),
                                               transit_line=RouteLegTransitLine(line_name='L',
                                                                                vehicle_type='Tram',
                                                                                transit_agencies=[
                                                                                    RouteLegTransitAgency(
                                                                                        name='Odense Letbane',
                                                                                        uri='https://www.odenseletbane.dk/')]),
                                               price=None), RouteLeg(departure_place_name='Odense st - Gleis 3',
                                                                     arrival_place_name='Kolding st',
                                                                     departure_datetime=datetime(2024,
                                                                                                 1, 15,
                                                                                                 17,
                                                                                                 13),
                                                                     arrival_datetime=datetime(2024, 1,
                                                                                               15, 17,
                                                                                               49),
                                                                     transit_line=RouteLegTransitLine(
                                                                         line_name='IC', vehicle_type='Train',
                                                                         transit_agencies=[
                                                                             RouteLegTransitAgency(name='DSB',
                                                                                                   uri='http://www.dsb.dk/')]),
                                                                     price=None),
                                      RouteLeg(departure_place_name='Kolding st',
                                               arrival_place_name='Flensburg / Flensborg',
                                               departure_datetime=datetime(2024, 1, 15, 17, 58),
                                               arrival_datetime=datetime(2024, 1, 15, 19, 7),
                                               transit_line=RouteLegTransitLine(line_name='IC',
                                                                                vehicle_type='Train',
                                                                                transit_agencies=[
                                                                                    RouteLegTransitAgency(
                                                                                        name='Dänische Staatsbahnen',
                                                                                        uri='https://www.thetrainline.com/de/bahnunternehmen/dsb'),
                                                                                    RouteLegTransitAgency(
                                                                                        name='DSB',
                                                                                        uri='http://www.dsb.dk/')]),
                                               price=None),
                                      RouteLeg(departure_place_name='Flensburg / Flensborg',
                                               arrival_place_name='Hamburg Hbf',
                                               departure_datetime=datetime(2024, 1, 15, 19, 15),
                                               arrival_datetime=datetime(2024, 1, 15, 21, 17),
                                               transit_line=RouteLegTransitLine(line_name='RE7',
                                                                                vehicle_type='Train',
                                                                                transit_agencies=[
                                                                                    RouteLegTransitAgency(
                                                                                        name='DB Regio AG',
                                                                                        uri='http://www.bahn.de/'),
                                                                                    RouteLegTransitAgency(
                                                                                        name='Hamburger Verkehrsverbund (hvv)',
                                                                                        uri='http://www.hvv.de/')]),
                                               price=None)]), Route(legs=[
                              RouteLeg(departure_place_name='Campus Odense (Odense Letbane)',
                                       arrival_place_name='Odense Banegård (Odense Letbane)',
                                       departure_datetime=datetime(2024, 1, 15, 16, 48),
                                       arrival_datetime=datetime(2024, 1, 15, 17, 6),
                                       transit_line=RouteLegTransitLine(line_name='L', vehicle_type='Tram',
                                                                        transit_agencies=[
                                                                            RouteLegTransitAgency(name='Odense Letbane',
                                                                                                  uri='https://www.odenseletbane.dk/')]),
                                       price=None),
                              RouteLeg(departure_place_name='Odense st - Gleis 3',
                                       arrival_place_name='Lunderskov st - Gleis 1',
                                       departure_datetime=datetime(2024, 1, 15, 17, 13),
                                       arrival_datetime=datetime(2024, 1, 15, 17, 59),
                                       transit_line=RouteLegTransitLine(line_name='IC', vehicle_type='Train',
                                                                        transit_agencies=[
                                                                            RouteLegTransitAgency(name='DSB',
                                                                                                  uri='http://www.dsb.dk/')]),
                                       price=None),
                              RouteLeg(departure_place_name='Lunderskov st - Gleis 1',
                                       arrival_place_name='Flensburg / Flensborg',
                                       departure_datetime=datetime(2024, 1, 15, 18, 6),
                                       arrival_datetime=datetime(2024, 1, 15, 19, 7),
                                       transit_line=RouteLegTransitLine(line_name='IC', vehicle_type='Train',
                                                                        transit_agencies=[
                                                                            RouteLegTransitAgency(name='DSB',
                                                                                                  uri='http://www.dsb.dk/'),
                                                                            RouteLegTransitAgency(
                                                                                name='Dänische Staatsbahnen',
                                                                                uri='https://www.thetrainline.com/de/bahnunternehmen/dsb')]),
                                       price=None),
                              RouteLeg(departure_place_name='Flensburg / Flensborg', arrival_place_name='Hamburg Hbf',
                                       departure_datetime=datetime(2024, 1, 15, 19, 15),
                                       arrival_datetime=datetime(2024, 1, 15, 21, 17),
                                       transit_line=RouteLegTransitLine(line_name='RE7', vehicle_type='Train',
                                                                        transit_agencies=[
                                                                            RouteLegTransitAgency(name='DB Regio AG',
                                                                                                  uri='http://www.bahn.de/'),
                                                                            RouteLegTransitAgency(
                                                                                name='Hamburger Verkehrsverbund (hvv)',
                                                                                uri='http://www.hvv.de/')]),
                                       price=None)]),
                          Route(legs=[RouteLeg(departure_place_name='Campus Odense (Odense Letbane)',
                                               arrival_place_name='Odense Banegård (Odense Letbane)',
                                               departure_datetime=datetime(2024, 1, 15, 16, 48),
                                               arrival_datetime=datetime(2024, 1, 15, 17, 6),
                                               transit_line=RouteLegTransitLine(line_name='L', vehicle_type='Tram',
                                                                                transit_agencies=[
                                                                                    RouteLegTransitAgency(
                                                                                        name='Odense Letbane',
                                                                                        uri='https://www.odenseletbane.dk/')]),
                                               price=None), RouteLeg(departure_place_name='Odense st - Gleis 3',
                                                                     arrival_place_name='Lunderskov st - Gleis 1',
                                                                     departure_datetime=datetime(2024, 1, 15,
                                                                                                 17, 13),
                                                                     arrival_datetime=datetime(2024, 1, 15,
                                                                                               17, 59),
                                                                     transit_line=RouteLegTransitLine(line_name='IC',
                                                                                                      vehicle_type='Train',
                                                                                                      transit_agencies=[
                                                                                                          RouteLegTransitAgency(
                                                                                                              name='DSB',
                                                                                                              uri='http://www.dsb.dk/')]),
                                                                     price=None),
                                      RouteLeg(departure_place_name='Lunderskov st - Gleis 1',
                                               arrival_place_name='Flensburg / Flensborg',
                                               departure_datetime=datetime(2024, 1, 15, 18, 6),
                                               arrival_datetime=datetime(2024, 1, 15, 19, 7),
                                               transit_line=RouteLegTransitLine(line_name='IC', vehicle_type='Train',
                                                                                transit_agencies=[
                                                                                    RouteLegTransitAgency(name='DSB',
                                                                                                          uri='http://www.dsb.dk/'),
                                                                                    RouteLegTransitAgency(
                                                                                        name='Dänische Staatsbahnen',
                                                                                        uri='https://www.thetrainline.com/de/bahnunternehmen/dsb')]),
                                               price=None), RouteLeg(departure_place_name='Flensburg / Flensborg',
                                                                     arrival_place_name='Hamburg Dammtor',
                                                                     departure_datetime=datetime(2024, 1, 15,
                                                                                                 19, 15),
                                                                     arrival_datetime=datetime(2024, 1, 15,
                                                                                               21, 12),
                                                                     transit_line=RouteLegTransitLine(line_name='RE7',
                                                                                                      vehicle_type='Train',
                                                                                                      transit_agencies=[
                                                                                                          RouteLegTransitAgency(
                                                                                                              name='Hamburger Verkehrsverbund (hvv)',
                                                                                                              uri='http://www.hvv.de/'),
                                                                                                          RouteLegTransitAgency(
                                                                                                              name='DB Regio AG',
                                                                                                              uri='http://www.bahn.de/')]),
                                                                     price=None),
                                      RouteLeg(departure_place_name='Hamburg Dammtor',
                                               arrival_place_name='Hamburg Hbf',
                                               departure_datetime=datetime(2024, 1, 15, 21, 19, 18),
                                               arrival_datetime=datetime(2024, 1, 15, 21, 21),
                                               transit_line=RouteLegTransitLine(line_name='S5',
                                                                                vehicle_type='Commuter train',
                                                                                transit_agencies=[
                                                                                    RouteLegTransitAgency(
                                                                                        name='Hamburger Verkehrsverbund (hvv)',
                                                                                        uri='http://www.hvv.de/')]),
                                               price=None)]), Route(legs=[
                              RouteLeg(departure_place_name='Campus Odense (Odense Letbane)',
                                       arrival_place_name='Odense Banegård (Odense Letbane)',
                                       departure_datetime=datetime(2024, 1, 15, 16, 48),
                                       arrival_datetime=datetime(2024, 1, 15, 17, 6),
                                       transit_line=RouteLegTransitLine(line_name='L', vehicle_type='Tram',
                                                                        transit_agencies=[
                                                                            RouteLegTransitAgency(name='Odense Letbane',
                                                                                                  uri='https://www.odenseletbane.dk/')]),
                                       price=None),
                              RouteLeg(departure_place_name='Odense st - Gleis 3', arrival_place_name='Fredericia',
                                       departure_datetime=datetime(2024, 1, 15, 17, 10),
                                       arrival_datetime=datetime(2024, 1, 15, 17, 38),
                                       transit_line=RouteLegTransitLine(line_name='ICL', vehicle_type='Train',
                                                                        transit_agencies=[
                                                                            RouteLegTransitAgency(name='DSB',
                                                                                                  uri='http://www.dsb.dk/')]),
                                       price=None),
                              RouteLeg(departure_place_name='Fredericia', arrival_place_name='Flensburg / Flensborg',
                                       departure_datetime=datetime(2024, 1, 15, 17, 45),
                                       arrival_datetime=datetime(2024, 1, 15, 19, 7),
                                       transit_line=RouteLegTransitLine(line_name='IC', vehicle_type='Train',
                                                                        transit_agencies=[
                                                                            RouteLegTransitAgency(
                                                                                name='Dänische Staatsbahnen',
                                                                                uri='https://www.thetrainline.com/de/bahnunternehmen/dsb'),
                                                                            RouteLegTransitAgency(name='DSB',
                                                                                                  uri='http://www.dsb.dk/')]),
                                       price=None),
                              RouteLeg(departure_place_name='Flensburg / Flensborg',
                                       arrival_place_name='Hamburg Dammtor',
                                       departure_datetime=datetime(2024, 1, 15, 19, 15),
                                       arrival_datetime=datetime(2024, 1, 15, 21, 12),
                                       transit_line=RouteLegTransitLine(line_name='RE7', vehicle_type='Train',
                                                                        transit_agencies=[
                                                                            RouteLegTransitAgency(
                                                                                name='Hamburger Verkehrsverbund (hvv)',
                                                                                uri='http://www.hvv.de/'),
                                                                            RouteLegTransitAgency(name='DB Regio AG',
                                                                                                  uri='http://www.bahn.de/')]),
                                       price=None),
                              RouteLeg(departure_place_name='Hamburg Dammtor', arrival_place_name='Hamburg Hbf',
                                       departure_datetime=datetime(2024, 1, 15, 21, 19, 18),
                                       arrival_datetime=datetime(2024, 1, 15, 21, 21),
                                       transit_line=RouteLegTransitLine(line_name='S5', vehicle_type='Commuter train',
                                                                        transit_agencies=[
                                                                            RouteLegTransitAgency(
                                                                                name='Hamburger Verkehrsverbund (hvv)',
                                                                                uri='http://www.hvv.de/')]),
                                       price=None)]),
                          Route(legs=[RouteLeg(departure_place_name='Campus Odense (Odense Letbane)',
                                               arrival_place_name='Odense Banegård (Odense Letbane)',
                                               departure_datetime=datetime(2024, 1, 15, 17, 41),
                                               arrival_datetime=datetime(2024, 1, 15, 17, 59),
                                               transit_line=RouteLegTransitLine(line_name='L', vehicle_type='Tram',
                                                                                transit_agencies=[
                                                                                    RouteLegTransitAgency(
                                                                                        name='Odense Letbane',
                                                                                        uri='https://www.odenseletbane.dk/')]),
                                               price=None), RouteLeg(departure_place_name='Odense st - Gleis 3',
                                                                     arrival_place_name='Kolding st',
                                                                     departure_datetime=datetime(2024, 1, 15,
                                                                                                 18, 13),
                                                                     arrival_datetime=datetime(2024, 1, 15,
                                                                                               18, 49),
                                                                     transit_line=RouteLegTransitLine(line_name='IC',
                                                                                                      vehicle_type='Train',
                                                                                                      transit_agencies=[
                                                                                                          RouteLegTransitAgency(
                                                                                                              name='DSB',
                                                                                                              uri='http://www.dsb.dk/')]),
                                                                     price=None),
                                      RouteLeg(departure_place_name='Kolding', arrival_place_name='ZOB Hamburg',
                                               departure_datetime=datetime(2024, 1, 15, 19, 50),
                                               arrival_datetime=datetime(2024, 1, 15, 23, 40),
                                               transit_line=RouteLegTransitLine(line_name='FlixBus N74',
                                                                                vehicle_type='Bus', transit_agencies=[
                                                       RouteLegTransitAgency(name='FlixBus',
                                                                             uri='https://global.flixbus.com/')]),
                                               price=None)])])
