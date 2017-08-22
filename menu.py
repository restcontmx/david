from django_tools import DjangoArmor
from mysql_tools import MySQLArmor
from angularjs_tools import AngularJsArmor
from warrior import Warzone

import twitter_module as twitter_m
"""
This class runs,
the menu and has the menu functions
"""
class Menu :

    def __init__( self ) :
        self.warzones = []
        self.actual_warzone = None

    def run ( self ) :
        """
        Run the menu function
        """
        instr = ""
        print( "Hi again master, hope you are having an excelent day, " )
        while "david, go to sleep" not in instr :
            instr = raw_input( "What can I do for you?\n> " )
            self.creation_options( instr )
        print "Good night, see you later."

    def creation_options ( self, instr ) :
        """
        This is for warrior options
        """
        if "create warzone" in instr :
            print( "Glad you want to go to war master, let me create a WarZone lmL..." )
            instr = raw_input( "War Zone Name : > " )
            temp_wz = Warzone()
            temp_wz.create_warzone( instr )
            self.warzones.append( temp_wz )
            self.actual_warzone = temp_wz
        elif "set warzone" in instr :
            if len( self.warzones ) > 0 :
                print( "Select between your actual warzones by name :" )
                for wz in self.warzones:
                    wz.print_info()
                instr = raw_input( "> " )
                if "go back" not in instr :
                    for wz in self.warzones :
                        if wz.name == instr :
                            self.actual_warzone = wz
                            print( "Warzone just setted to actual, so go to war..." )
            else :
                print( "You don't have any warzones created." )
        elif "use django armor" in instr :
            print( "Setting Django Armor For War..." )
            daah = DjangoArmor( self.actual_warzone )
            daah.create_warzone_folder()
            daah.create_resources()
        elif "create model" in instr :
            print( "Of course I will create a model for you." )
            instr = raw_input( "Would you like it to be frontend or backend?\n> " )
            if "backend" in instr :
                print( "Ok master let me see what I can do with your instruction...." )
                print( "Don't go away, I'll bee asking you some questions..." )
                instr = raw_input( "In what technology would you like the BE?\n> " )
                if "django" in instr or "Django" in instr :
                    model = self.actual_warzone.create_model()
                    DjangoArmor( self.actual_warzone ).be_model_creation( model )
                else :
                    print( "Sorry master, you haven't done anything else than Django on the BackEnd." )
            elif "frontend" in instr :
                print( "Ok master let me see what I can do with your instruction..." )
                print( "Don't go away, I'll bee asking you some questions..." )
            elif "not now" in instr :
                print( "Alright master, in other time..." )
        elif "use mysql armor" in instr :
            print( "Setting MySQL Armor For War..." )
            daah = MySQLArmor( self.actual_warzone )
            daah.create_warzone_folder()
        elif "use angularjs armor" in instr :
            print( "Setting Angularjs Armor For War..." )
            daah = AngularJsArmor( self.actual_warzone )
            daah.create_warzone_folder()
        elif "create angularjs controllers" in instr :
            print( "Creating Repostiroies and Controllers for AngularJs Armor..." )
            daah = AngularJsArmor( self.actual_warzone )
            daah.create_controllers_files()
        elif "create bunch of backend models in django" in instr :
            print( "Creating a buch of django models" )
            daah = DjangoArmor( self.actual_warzone )
            for m in self.actual_warzone.models :
                print( "Creating model '%s'" % m.name )
                daah.be_model_creation( m )
        elif "export models from mysql" in instr :
            instr = raw_input( "Give me the name of the file on the mysql folder.\n> " )
            MySQLArmor( self.actual_warzone ).set_models( instr )
        elif "update twitter status" in instr :
            instr = raw_input( "Alright; write your 140max status.\n> " )
            twitter_m.set_status( instr )
        elif "get home timeline" in instr :
            print( "Al right there you go timeline..." )
            twitter_m.get_user_timeline()
        elif "not now" in instr :
            print ( "Alright master, in other time..." )
