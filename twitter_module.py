import twitter

api = twitter.Api()

api = twitter.Api(consumer_key='KDAziQL3qu7ZTkvgmi5EYlmgq',
                      consumer_secret='6PqgiMpYusaZxrr8fwc0HlSutowqMwHZYs9ORht1ZIXEE9C9VI',
                      access_token_key='3695679499-YTMSs7lrwe3M1xbM5CBVgn9IwxnQRbpaUJVk99o',
                      access_token_secret='EHNzAtNXChlO8GksPBjiOcbEl2X1ZFxtQmP49AH7KSlNs')

def set_status( status ) :
    """
    Post status on twitter; no max 140 chars
    """
    if len( status ) <= 140 :
        status = api.PostUpdate( status )
        print( "Status posted correctly!!!" )
    else :
        print( "Your status should be max 140 chars long." )

def get_user_timeline() :
    """
    Get home time line
    """
    statuses = api.GetHomeTimeline()
    for s in statuses :
        print( "-------------------------------------------------------------" )
        print( s.user.name )
        print( s.text )
        print( s.created_at )
        print( "retwitted : {0}, favs : {1}".format( s.retweet_count, s.favorite_count ) )
        print( "-------------------------------------------------------------" )
