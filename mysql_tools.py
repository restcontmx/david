# -*- coding: utf-8 -*-
"""
This module is for table exportation for model creation
"""
import json, os, errno
from warrior_objects import *

class MySQLArmor :

    def __init__( self, warzone ) :
        # Constructor function
        self.warzone = warzone

    def create_warzone_folder( self ) :
        # This will create a warzone file on the required module
        try :
            os.makedirs( ( "{0}/{1}" ).format( self.warzone.path, "mysql" ) )
            print( "MySQL Armor Ready for War lmL" )
            print( "Remember to add the exportation files on the mysql folder" )
        except OSError as e :
            print( ( "There was an error creating folder on the warzone; {0}" ).format( str( e ) ) )

    def set_models( self, file_path ) :
        # set models with sql file
        # gets the file, reads table by table
        try:
            # open the file
            if ".sql" in file_path :
                print "Opening file..."
                with open( ( "{0}/{1}/{2}" ).format( self.warzone.path, "mysql", file_path ) ) as mysql_file :
                    print "Reading file"
                    file_content = mysql_file.read().split( "CREATE TABLE" )
                    file_content.pop(0)
                    for fc in file_content :
                        fc_ls = fc.split( "\n" )
                        model_name = fc_ls[0].split( "`" )[1]
                        temp_model = Model( model_name, '', [], '' )
                        for field_line in fc_ls :
                            if "int(" in field_line and "AUTO_INCREMENT" in field_line :
                                formats = field_line.split( " " )
                                field_name = formats[2].split( "`" )[1]
                                field_type = number_t
                                field_size = formats[3].split( "(" )[-1]
                                field_size = field_size[:-1]
                                param = Param( field_name, field_type, field_size, true, true, "0", ' ', ' ' )
                                temp_model.params.append( param )
                            elif "int(" in field_line and "AUTO_INCREMENT" not in field_line :
                                formats = field_line.split( " " )
                                field_name = formats[2].split( "`" )[1]
                                field_type = number_t
                                field_size = formats[3].split( "(" )[-1]
                                field_size = field_size[:-1]
                                field_default = formats[5].split( "," )[0].replace( "'", "" ) if "NULL" not in formats[5] else ''
                                param = Param( field_name, field_type, field_size, true, true, field_default, ' ', ' ' )
                                temp_model.params.append( param )
                            elif "varchar(" in field_line :
                                formats = field_line.split( " " )
                                field_name = formats[2].split( "`" )[1]
                                field_type = text_t
                                field_size = formats[3].split( "(" )[-1]
                                field_size = field_size[:-1]
                                field_default = formats[5].split( "," )[0].replace( "'", "" ) if "NULL" not in formats[5] else ''
                                param = Param( field_name, field_type, field_size, true, true, field_default, ' ', ' ' )
                                temp_model.params.append( param )
                            elif "text," in field_line :
                                formats = field_line.split( " " )
                                field_name = formats[2].split( "`" )[1]
                                field_type = text_t
                                param = Param( field_name, field_type, "512", true, true, ' ', ' ', ' ' )
                                temp_model.params.append( param )
                            elif "decimal(" in field_line :
                                formats = field_line.split( " " )
                                field_name = formats[2].split( "`" )[1]
                                field_type = decimal_t
                                field_size = formats[3].split( "(" )[-1]
                                field_size = field_size[:-1]
                                field_default = formats[5].split( "," )[0].replace( "'", "" )
                                param = Param( field_name, field_type, field_size, true, true, field_default, ' ', ' ' )
                                temp_model.params.append( param )
                            elif "datetime" in field_line :
                                formats = field_line.split( " " )
                                field_name = formats[2].split( "`" )[1]
                                field_type = datetime_t
                                param = Param( field_name, field_type, "0", true, true, ' ', ' ', ' ' )
                                temp_model.params.append( param )
                            elif " date " in field_line :
                                formats = field_line.split( " " )
                                field_name = formats[2].split( "`" )[1]
                                field_type = date_t
                                param = Param( field_name, field_type, "0", true, true, ' ', ' ', ' ' )
                                temp_model.params.append( param )
                        self.warzone.models.append( temp_model )
            else :
                print( "The file is not the right extention" )
        except Exception as e:
            print( ( "There was an error openning the file you requested; {0}" ).format( str( e ) ) )
