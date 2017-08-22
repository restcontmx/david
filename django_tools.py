# -*- coding: utf-8 -*-
from warrior_objects import *
from Armor import Armor
import json, os, errno

"""
This will create all the django dependencies
"""
class DjangoArmor( Armor ) :

    def __init__( self, warzone ) :
        # Constructor function
        self.warzone = warzone

    def be_model_creation( self, model ) :
        # This creates a model in the backend,
        # this means that creates APIViews, urls, serializers, models
        print( "Getting ready to war with Django Armor..." )
        try :
            self.set_model_on_resources( model )
        except Exception as e :
            print( "There was an error creating model file; {0}".format( str( e ) ) )

    def create_warzone_folder( self ) :
        # This will create a warzone file on the required module
        try :
            os.makedirs( ( "{0}/{1}" ).format( self.warzone.path, "django" ) )
            print( "Django Armor Ready for War lmL" )
        except OSError as e :
            print( ( "There was an error creating folder on the warzone; {0}" ).format( str( e ) ) )

    def create_resources( self ) :
        # This will create all the resources file for the models, Serializers, etc.
        # model file
        model_format = open( DJANGO_MODEL_IMPORTS_ROUTE )
        models_file = open( ( "{0}/{1}/models.py" ).format( self.warzone.path, "django" ), 'w+' )
        models_file.write( model_format.read() )
        models_file.close()
        model_format.close()
        # serializers file
        serializer_format = open( DJANGO_SERIALIZER_IMPORTS_ROUTE )
        serializers_file = open( ( "{0}/{1}/serializers.py" ).format( self.warzone.path, "django" ), 'w+' )
        serializers_file.write( serializer_format.read() )
        serializers_file.close()
        serializer_format.close()
        # urls file
        url_format = open( DJANGO_URL_IMPORTS_ROUTE )
        urls_file = open( ( "{0}/{1}/urls.py" ).format( self.warzone.path, "django" ), 'w+' )
        urls_file.write( url_format.read() )
        urls_file.close()
        url_format.close()
        # APIViews file
        apiview_format = open( DJANGO_APIVIEW_IMPORTS_ROUTE )
        apiviews_file = open( ( "{0}/{1}/api_views.py" ).format( self.warzone.path, "django" ), 'w+' )
        apiviews_file.write( apiview_format.read() )
        apiviews_file.close()
        apiview_format.close()

    def set_model_on_resources( self, model ) :
        # Set Model on the resources files
        # update model file
        with open( ( "{0}/{1}/models.py" ).format( self.warzone.path, "django" ), 'ab' ) as models_file :
            model_struct_file = open( MODEL_STRUCT_FILE )
            model_struct = model_struct_file.read()
            model_struct = model_struct.replace( MODEL, model.name )
            model_struct = model_struct.replace( DESCRIPTION, model.description )
            model_struct = model_struct.replace( PARAMS, self.create_params_struct( model.params ) )
            models_file.write( "\n" )
            models_file.write( model_struct )
            model_struct_file.close()
        # update serializer file
        with open( ( "{0}/{1}/serializers.py" ).format( self.warzone.path, "django" ), 'ab' ) as serializers_file :
            serializer_struct_file = open( SERIALIZER_STRUCT_FILE )
            serializer_struct = serializer_struct_file.read()
            serializer_struct = serializer_struct.replace( MODEL, model.name )
            serializer_struct = serializer_struct.replace( DESCRIPTION, model.description )
            serializer_relationships = ""
            fields = "'id', "
            for p in model.params :
                if p.relationship == FK :
                    serializer_relationships += ( "\t\t{0} = {1}Serializer( many = False )\n" ).format( p.name, p.relationship_model )
                elif p.relationship == MTM :
                    serializer_relationships += ( "\t\t{0} = {1}Serializer( many = True )\n" ).format( p.name, p.relationship_model )
                fields += ( "'{0}', " ).format( p.name )
            fields += "'location', 'timestamp', 'updated', "
            serializer_struct = serializer_struct.replace( FIELDS, fields )
            serializer_struct = serializer_struct.replace( RELATIONSHIPS, serializer_relationships )
            # set relationship parameters
            serializers_file.write( "\n" )
            serializers_file.write( serializer_struct )
            serializer_struct_file.close()
        # update api views file
        with open( ( "{0}/{1}/api_views.py" ).format( self.warzone.path, "django" ), 'ab' ) as apiviews_file :
            apiview_struct_file = open( API_VIEW_STRUCT_FILE )
            apiview_struct = apiview_struct_file.read()
            apiview_struct = apiview_struct.replace( MODEL, model.name )
            apiview_struct = apiview_struct.replace( DESCRIPTION, model.description )
            create_params, update_params, mtm_params = self.create_apiviewparams_struct( model.params )
            apiview_struct = apiview_struct.replace( CREATE_PARAMS, create_params )
            apiview_struct = apiview_struct.replace( UPDATE_PARAMS, update_params )
            apiview_struct = apiview_struct.replace( MTM_PARAMS, mtm_params )
            apiviews_file.write( "\n" )
            apiviews_file.write( apiview_struct )
            apiview_struct_file.close()
        # update urls file
        with open( ( "{0}/{1}/urls.py" ).format( self.warzone.path, "django" ), 'w' ) as urls_file :
            urls_struct_file = open( DJANGO_URL_IMPORTS_ROUTE )
            urls_struct = urls_struct_file.read()
            urls_struct = urls_struct.replace( URLPATTERNS_CONTENT, self.create_urlmodels_struct() )
            urls_file.write( urls_struct )
            urls_struct_file.close()

    def create_urlmodels_struct( self ) :
        # create url models structure
        # This will create a string of all the urls for each model
        urls_struct = ""
        with open( DJANGO_MODEL_PARAMS_ROUTE ) as model_params_file :
            model_params = json.loads( model_params_file.read() )
            for m in self.warzone.models :
                # i have to add the string from the file
                urls_struct += ( "\t\t# {0} urls\n" ).format( m.name )
                temporal_struct = model_params[version1_8][urls][url_list_create].replace( MODEL, m.name )
                temporal_struct = temporal_struct.replace( M_NAME, m.name.lower() )
                urls_struct += ( "\t\t{0},\n" ).format( temporal_struct )
                temporal_struct = model_params[version1_8][urls][url_update_retrieve_delete].replace( MODEL, m.name )
                temporal_struct = temporal_struct.replace( M_NAME, m.name.lower() )
                urls_struct += ( "\t\t{0},\n\n" ).format( temporal_struct )
        return urls_struct

    def create_apiviewparams_struct( self, params ) :
        # create api view parameters structure
        # this creates a string with all the api view param structure
        create_params = ""
        update_params = ""
        mtm_params = ""
        model_params = json.loads( open( DJANGO_MODEL_PARAMS_ROUTE ).read() )
        for p in params :
            # check if not relationship
            if p.relationship != " " :
                if p.relationship == MTM :
                    # add to the string something with many to many relationship
                    temporal_struct = model_params[ version1_8 ][MTM][apiview].replace( P_NAME, p.name )
                    temporal_struct = temporal_struct.replace( MTM_MODEL, p.relationship_model )
                    mtm_params += ( "\t\t\t\tinstance.{0}\n" ).format( temporal_struct )
                elif p.relationship == FK :
                    # add to the string something with foreign key relationship
                    temporal_struct = model_params[ version1_8 ][FK][apiview].replace( P_NAME, p.name )
                    temporal_struct = temporal_struct.replace( FK_MODEL, p.relationship_model )
                    create_params += ( "\t\t\t\t{0} = {1},\n" ).format( p.name, temporal_struct )
                    update_params += ( "\t\t\t\tinstance.{0} = {1}\n" ).format( p.name, temporal_struct )
            elif p.type == text_t :
                # add to the string sommething with CharFiled
                temporal_struct = model_params[version1_8][text_t][apiview].replace( P_NAME, p.name )
                create_params += ( "\t\t\t\t{0} = {1},\n" ).format( p.name, temporal_struct )
                update_params += ( "\t\t\t\tinstance.{0} = {1}\n" ).format( p.name, temporal_struct )
            elif p.type == number_t :
                # add to the string something with IntegerField
                temporal_struct = model_params[version1_8][number_t][apiview].replace( P_NAME, p.name )
                create_params += ( "\t\t\t\t{0} = {1},\n" ).format( p.name, temporal_struct )
                update_params += ( "\t\t\t\tinstance.{0} = {1}\n" ).format( p.name, temporal_struct )
            elif p.type == bignumber_t :
                # add to the string something with BigIntegerField
                temporal_struct = model_params[version1_8][bignumber_t][apiview].replace( P_NAME, p.name )
                create_params += ( "\t\t\t\t{0} = {1},\n" ).format( p.name, temporal_struct )
                update_params += ( "\t\t\t\tinstance.{0} = {1}\n" ).format( p.name, temporal_struct )
            elif p.type == decimal_t :
                # add to the string something with DecimalField
                temporal_struct = model_params[version1_8][decimal_t][apiview].replace( P_NAME, p.name )
                create_params += ( "\t\t\t\t{0} = {1},\n" ).format( p.name, temporal_struct )
                update_params += ( "\t\t\t\tinstance.{0} = {1}\n" ).format( p.name, temporal_struct )
            elif p.type == date_t :
                # add to the string something with DateField
                temporal_struct = model_params[version1_8][date_t][apiview].replace( P_NAME, p.name )
                create_params += ( "\t\t\t\t{0} = {1},\n" ).format( p.name, temporal_struct )
                update_params += ( "\t\t\t\tinstance.{0} = {1}\n" ).format( p.name, temporal_struct )
            elif p.type == datetime_t :
                # add to the string something with DateTimeField
                temporal_struct = model_params[version1_8][datetime_t][apiview].replace( P_NAME, p.name )
                create_params += ( "\t\t\t\t{0} = {1},\n" ).format( p.name, temporal_struct )
                update_params += ( "\t\t\t\tinstance.{0} = {1}\n" ).format( p.name, temporal_struct )
        return create_params, update_params, mtm_params

    def create_params_struct( self, params ) :
        # create parameters structure
        # This will create a param struct on the model
        param_struct = ""
        model_params = json.loads( open( DJANGO_MODEL_PARAMS_ROUTE ).read() )
        for p in params :
            p_config = ""
            # check if not relationship
            if p.relationship != " " :
                if p.relationship == MTM :
                    # add to the string something with many to many relationship
                    p_config += p.relationship_model
                    temporal_struct = model_params[version1_8][MTM][format_t].replace( P_NAME, p.name )
                    temporal_struct = temporal_struct.replace( P_CONFIG, p_config )
                    param_struct += ( PARAM_FORMAT ).format( temporal_struct )
                elif p.relationship == FK :
                    # add to the string something with foreign key relationship
                    p_config += p.relationship_model
                    temporal_struct = model_params[version1_8][FK][format_t].replace( P_NAME, p.name )
                    temporal_struct = temporal_struct.replace( P_CONFIG, p_config )
                    param_struct += ( PARAM_FORMAT ).format( temporal_struct )
            elif p.type == text_t :
                # add to the string sommething with CharFiled
                p_config += "max_length = {0}, ".format( p.size if p.size.isdigit() else 100 )
                p_config += "null = False, " if p.isNull == false else "null = True, "
                p_config += "blank = False, " if p.isEmpty == false else "blank = True, "
                p_config += ( DEFAULT_FORMAT_STR ).format( p.default )
                temporal_struct = model_params[version1_8][text_t][format_t].replace( P_NAME, p.name )
                temporal_struct = temporal_struct.replace( P_CONFIG, p_config )
                param_struct += ( PARAM_FORMAT ).format( temporal_struct )
            elif p.type == number_t :
                # add to the string something with IntegerField
                p_config += "null = False, " if p.isNull == false else "null = True, "
                p_config += "blank = False, " if p.isEmpty == false else "blank = True, "
                p_config += ( DEFAULT_FORMAT_NUM ).format( p.default if p.default.isdigit() else 0 )
                temporal_struct = model_params[version1_8][number_t][format_t].replace( P_NAME, p.name )
                temporal_struct = temporal_struct.replace( P_CONFIG, p_config )
                param_struct += ( PARAM_FORMAT ).format( temporal_struct )
            elif p.type == bignumber_t :
                # add to the string something with BigIntegerField
                p_config += "null = False, " if p.isNull == false else "null = True, "
                p_config += "blank = False, " if p.isEmpty == false else "blank = True, "
                p_config += ( DEFAULT_FORMAT_NUM ).format( p.default if p.default.isdigit() else 0 )
                temporal_struct = model_params[version1_8][bignumber_t][format_t].replace( P_NAME, p.name )
                temporal_struct = temporal_struct.replace( P_CONFIG, p_config )
                param_struct += ( PARAM_FORMAT ).format( temporal_struct )
            elif p.type == decimal_t :
                # add to the string something with DecimalField
                digits, decimals = p.size.split( "," )
                p_config += ( "max_digits = {0}, " ).format( digits if digits.isdigit() else 5 )
                p_config += ( "decimal_places = {0}, " ).format( decimals if decimals.isdigit() else 2 )
                p_config += "null = False, " if p.isNull == false else "null = True, "
                p_config += "blank = False, " if p.isEmpty == false else "blank = True, "
                p_config += ( DEFAULT_FORMAT_NUM ).format( p.default if p.default.isdigit() else 0 )
                temporal_struct = model_params[version1_8][decimal_t][format_t].replace( P_NAME, p.name )
                temporal_struct = temporal_struct.replace( P_CONFIG, p_config )
                param_struct += ( PARAM_FORMAT ).format( temporal_struct )
            elif p.type == date_t :
                # add to the string something with DateField
                p_config += "null = False, " if p.isNull == false else "null = True, "
                p_config += "blank = False " if p.isEmpty == false else "blank = True "
                temporal_struct = model_params[version1_8][date_t][format_t].replace( P_NAME, p.name )
                temporal_struct = temporal_struct.replace( P_CONFIG, p_config )
                param_struct += ( PARAM_FORMAT ).format( temporal_struct )
            elif p.type == datetime_t :
                # add to the string something with DateTimeField
                p_config += "null = False, " if p.isNull == false else "null = True, "
                p_config += "blank = False " if p.isEmpty == false else "blank = True "
                temporal_struct = model_params[version1_8][datetime_t][format_t].replace( P_NAME, p.name )
                temporal_struct = temporal_struct.replace( P_CONFIG, p_config )
                param_struct += ( PARAM_FORMAT ).format( temporal_struct )
            elif p.type == bool_t :
                # add to the string something with BooleanField
                param_struct += ( PARAM_FORMAT ).format( model_params[version1_8][bool_t][format_t] )
        return param_struct
