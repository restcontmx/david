# -*- coding: utf-8 -*-
from warrior_objects import *
from Armor import Armor
import json, os, errno

class AngularJsArmor( Armor ) :

    def __init__( self, warzone ) :
        # Constructor function
        self.warzone = warzone

    def create_warzone_folder( self ) :
        # This will create a warzone file on the required module
        try :
            os.makedirs( ( "{0}/{1}" ).format( self.warzone.path, "angularjs" ) )
            os.makedirs( ( "{0}/{1}" ).format( self.warzone.path, "angularjs/controllers" ) )
            os.makedirs( ( "{0}/{1}" ).format( self.warzone.path, "angularjs/routes" ) )
            os.makedirs( ( "{0}/{1}" ).format( self.warzone.path, "angularjs/views" ) )
            os.makedirs( ( "{0}/{1}" ).format( self.warzone.path, "angularjs/config" ) )
            print( "AngularJS Armor Ready for War lmL" )
        except OSError as e :
            print( ( "There was an error creating folder on the warzone; {0}" ).format( str( e ) ) )

    def create_resources( self ) :
        # This will create all the resources file, route, views, controllers
        # create controller file
        # create route file
        # create views files
        pass

    def set_model_on_resources( self, model ) :
        # set model on the resources files
        # update views files
        # 1 - form file
        # 2 - new file
        # 3 - detail file
        # 4 - edit file
        # 5 - list file
        # update routes files
        # 1 - route file
        # update controllers files
        # 1 - repository structure
        # 2 - controller structure
        pass

    def create_formparams_struct( self, params ) :
        # create parameters structure for form view
        # This will create a param struct on the model
        param_struct = ""
        for p in params :
            p_config = ""
            # check if not relationship
            if p.relationship != " " :
                if p.relationship == MTM :
                    # add to the string something with many to many relationship
                    pass
                elif p.relationship == FK :
                    # add to the string something with foreign key relationship
                    pass
            elif p.type == text_t :
                # add to the string sommething with CharFiled
                pass
            elif p.type == number_t :
                # add to the string something with IntegerField
                pass
            elif p.type == bignumber_t :
                # add to the string something with BigIntegerField
                pass
            elif p.type == decimal_t :
                # add to the string something with DecimalField
                pass
            elif p.type == date_t :
                # add to the string something with DateField
                pass
            elif p.type == datetime_t :
                # add to the string something with DateTimeField
                pass
            elif p.type == bool_t :
                # add to the string something with BooleanField
                pass
        return param_struct

    def create_detailparams_struct( self, params ) :
        # create parameters structure for detail view
        # this will create a param structure of the model
        pass

    def create_routes_files( self ) :
        for m in self.warzone.models :
            min_model_name = m.name.lower()
            model_without_under = m.name.replace( "_", "" )
            mays_model_name = model_without_under.title()
            print( "Creating Routers for %s model" % m.name )
            with open( ( "{0}/{1}/{2}.js" ).format( self.warzone.path, "angularjs/routes/", model_without_under.lower() ), 'ab' ) as model_routesjs :
                cs_temp = open( ROUTE_STRUCT_FILE ).read()
                cs_temp = cs_temp.replace( M_MODEL, min_model_name )
                cs_temp = cs_temp.replace( MAYSMODEL, mays_model_name )
                model_routejs.write( cs_temp )

    def create_controllers_files( self ) :
        # Create controller file
        # this will include the repository and the controller for the angularjs front end
        for m in self.warzone.models :
            min_model_name = m.name.lower()
            model_without_under = m.name.replace( "_", "" )
            mays_model_name = model_without_under.title()
            print( "Creating Controller and Repository for %s model" % m.name )
            with open( ( "{0}/{1}/{2}_controller.js" ).format( self.warzone.path, "angularjs/controllers/", model_without_under ), 'ab' ) as model_controllerjs :
                cs_temp = open( CONTROLLER_STRUCT_FILE ).read()
                cs_temp = cs_temp.replace( M_MODEL, min_model_name )
                cs_temp = cs_temp.replace( MAYSMODEL, mays_model_name )
                cs_temp = cs_temp.replace( NUMBER_PARAMS, self.get_numeric_controller_struct( m ) )
                model_controllerjs.write( cs_temp )

    def get_numeric_controller_struct( self, model ) :
        param_struct = ""
        model_params = json.loads( open( ANGULARJS_MODEL_PARAMS_ROUTE ).read() )
        for p in model.params :
            p_config = ""
            if p.type == number_t or p.type == bignumber_t :
                # add to the string something with IntegerField
                p_config += "\n                        "
                p_config += model_params[ version1_5_2 ][ number_t ][ controller_parse ]
                p_config = p_config.replace( M_MODEL, model.name ).replace( PARAM, p.name )
            elif p.type == decimal_t :
                # add to the string something with DecimalField
                p_config += "\n                        "
                p_config += model_params[ version1_5_2 ][ decimal_t ][ controller_parse ]
                p_config = p_config.replace( M_MODEL, model.name ).replace( PARAM, p.name )
            param_struct += p_config
        return param_struct

    def create_config_file( self ) :
        for m in self.warzone.models :
            pass
