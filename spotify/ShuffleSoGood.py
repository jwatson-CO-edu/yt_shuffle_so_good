import os, pickle, time
from datetime import datetime
from time import sleep
now = time.time

import numpy as np
from scipy.spatial import cKDTree
from IPython.display import clear_output

import spotipy
import spotipy.util as util


########## SPOTIFY: DATABASE OPERATIONS ############################################################

def init_session_database( dataPrefix  = "Study-Music-Data_" ):
    """ Init Session Database """
    _DATA_POSTFIX = ".pkl"
    data = {
        'time'     : now()  , # Data Structure Creation Time
        'playlists': dict() , # Study Playlist Info
        'collectID': set([]), # Currently accepted track IDs
        'review'   : dict() , # Review Playlist Info
        'reviewID' : set([]), # Previously reviewed track IDs
        'artists'  : dict() , # Study Artist Info
        'queries'  : dict() , # Queries made during music searches
        'genres'   : dict() , # Study Genre Info
        # 2024-08-11: Track info does NOT contain play count
    }
    # Pre-emptively Name Session File #
    timestamp = datetime.now().strftime( '%Y-%m-%dT%H:%M:%S' )
    outFilNam = dataPrefix + timestamp + _DATA_POSTFIX
    outPath   = os.path.join( 'data/', str( outFilNam ) )
    return data, timestamp, outFilNam, outPath



########## SPOTIFY: CLIENT CONNECTION ##############################################################

class SpotifyClient:
    """ Manage the connection to Spotify API """

    def __init__( self ):
        """ Init vars && connection """
        ## Client ##
        self.token = None
        self.spot  = None
        ## Client Info ##
        # FIXME: STORE ALL OF THIS IN A JSON CONFIG FILE
        self.IDpath        = "../keys/spot_ID.txt"
        self.secretPath    = "../keys/spot_SECRET.txt"
        self.CLIENT_ID     = ""
        self.CLIENT_SECRET = ""
        self.CLIENT_SCOPE  = "user-follow-modify playlist-modify-private playlist-modify-public"
        self.USER_NAME     = "31ytgsr7wdmiaroy77msqpiupdsi"
        self.REDIR_URI     = "https://github.com/jwatson-CO-edu/yt_shuffle_so_good"
        self.AUTH_URL      = 'https://accounts.spotify.com/api/token'
        self.BASE_URL      = 'https://api.spotify.com/v1/'
        ## API Info ##
        self._RESPONSE_LIMIT =  100
        self._ARTIST_Q_LIM   =   50
        self._MAX_OFFSET     = 1000
        self._T_LOGIN_S      = 60.0 * 45 #5 #10 #20 # 25 # 50
        self.tLastAuth       = 0.0
        ## API Secrets ##
        with open( self.IDpath , 'r' ) as f:
            self.CLIENT_ID = f.readlines()[0].strip()
        with open( self.secretPath , 'r' ) as f:
            self.CLIENT_SECRET = f.readlines()[0].strip()
        ## Connect ##
        self.check_API_token()
        
    
    def check_API_token( self ):
        tNow    = now()
        elapsed = tNow - self.tLastAuth
        if elapsed >= self._T_LOGIN_S:
            self.token = util.prompt_for_user_token(
                username      = self.USER_NAME,
                scope         = self.CLIENT_SCOPE,
                client_id     = self.CLIENT_ID,
                client_secret = self.CLIENT_SECRET,
                redirect_uri  = self.REDIR_URI
            )
            self.spot = spotipy.Spotify( auth = self.token )
            print( self.token )
            clear_output( wait = True )
            sleep( 2 )
            print( "TOKEN OBTAINED" )
            self.tLastAuth = tNow
        else:
            print( f"TOKEN STILL VALID, AGE: {elapsed/60.0:.2f} MINUTES" )



########## SPOTIFY: MUSIC VECTOR SPACE #############################################################

## Vector Representation ##
_MIN_LEN_S       = 60.0 + 45.0
_V_NUM_FEATURES  = 10
_V_SPEECH_FACTOR =  (1.0/0.3724) * (2.0/3.0) * 5.0
_V_INSTR_FACTOR  =  1.0 * 5.0
_V_ACOUST_FACTOR =  1.0
_V_DANCE_FACTOR  =  1.0 /  0.8701
_V_DURATN_FACTOR =  1.0 / 1000.0 / _MIN_LEN_S / 18.7821619
_V_ENERGY_FACTOR =  1.0
_V_LIVENS_FACTOR =  1.0 /   0.9173
_V_LOUDNS_FACTOR =  1.0 /  38.53
_V_TEMPO_FACTOR  =  1.0 / (174.331-45.7) * (3.0/4.0) * 3.0
_V_VALENC_FACTOR =  1.0


def get_track_vector( track ):
    """ Express the track characteristics as a vector """
    return np.array([
        track['speechiness'] * _V_SPEECH_FACTOR,
        track['instrumentalness'] * _V_INSTR_FACTOR,
        track['acousticness'] * _V_ACOUST_FACTOR,
        track['danceability'] * _V_DANCE_FACTOR,
        track['duration_ms'] * _V_DURATN_FACTOR,
        track['energy'] * _V_ENERGY_FACTOR,
        track['liveness'] * _V_LIVENS_FACTOR,
        track['loudness'] * _V_LOUDNS_FACTOR,
        (track['tempo']-45.7) * _V_TEMPO_FACTOR,
        track['valence'] * _V_VALENC_FACTOR,
    ])


def get_tracks_as_vectors( tracks ):
    """ Convert all tracks to vectors """
    Mrows  = len( tracks )
    if Mrows > 0:
        Ncols  = len( get_track_vector( tracks[0] ) )
        rtnMtx = np.zeros( (Mrows, Ncols,) ) 
        for i, trk in enumerate( tracks ):
            rtnMtx[i,:] = get_track_vector( trk )
        return rtnMtx
    else:
        return list()

        
def genre_vector_ops( gnre ):
    """ Calculate track vectors and properties derived from them """
    gnre['vectors'] = get_tracks_as_vectors( gnre['tracks'] )
    gnre['len']     = len( gnre['tracks'] )
    if gnre['len'] > 1:
        cntr = np.mean( gnre['vectors'], axis = 0 )
        dim  = len( cntr )
        for i in range( gnre['len'] ):
            pnt_i   = gnre['vectors'][i,:]
            dist_i  = np.linalg.norm( np.subtract( cntr, pnt_i ) )
            alpha_i = np.exp( -dist_i )
            cntr    = cntr * (1.0 - alpha_i) + pnt_i * alpha_i
        gnre['center'] = cntr # 2024-08-16: This is probably guaranteed to be inside the convex hull
        gnre['kdTree'] = cKDTree( gnre['vectors'], balanced_tree = False, compact_nodes = False )
    elif gnre['len'] > 0:
        gnre['center'] = gnre['vectors'][0]
        gnre['kdTree'] = cKDTree( gnre['vectors'], balanced_tree = False, compact_nodes = False )
    else:
        gnre['center'] = None
        gnre['kdTree'] = None


########## SPOTIFY: FILE OPERATIONS ################################################################

def update_music_database( db, fDb ):
    """ Update the database without overwriting important info """
    
    db['playlists'].update( fDb['playlists'] )
    
    db['collectID'] = db['collectID'].union( fDb['collectID'] )
    
    db['review'].update( fDb['review'] )
    
    db['reviewID'] = db['reviewID'].union( fDb['reviewID'] )

    for artID, artDct in fDb['artists'].items():
        dct_i = dict()
        dct_i.update( artDct )
        if artID in db['artists']:
            dct_i.update( db['artists'][ artID ] )
            dct_i['releases'] = artDct['releases']
            dct_i['releases'].extend( db['artists'][ artID ]['releases'] )
        db['artists'][ artID ] = dct_i

    for query in fDb['queries']:
        db['queries'][ query ] = db['queries'].get( query, 0 ) + fDb['queries'][ query ]

    db['genres'].update( fDb['genres'] )

    return db
    

def load_music_database( data, dataDir, dataPrefix, staleTime_s = 31*24*60*60, forceLoad = False ):
    """ Find the latest music database, test for freshness, and set current db if fresh """
    db      = None
    dbFiles = [os.path.join( dataDir, f ) for f in os.listdir( dataDir ) if (dataPrefix in str(f))]
    if len( dbFiles ):
        dbFiles.sort( reverse = True )
        with open( dbFiles[0], 'rb' ) as f:
            db = pickle.load( f )
        if (((data['time'] - db['time']) <= staleTime_s) or forceLoad):
            
            # data.update( db )
            db = update_music_database( data, db )
            
            print( f"Loaded {dbFiles[0]}!" )
        else:
            print( f"File {dbFiles[0]} was STALE by {(data['time']-db['time']-staleTime_s)/_MOD_T_DAY_S} days!" )
    return db


def save_music_database( dataDct, outPath ):
    """ Pickle `dataDct` to store current music collection data as well as search activity """
    print( f"About to write {outPath} ..." )
    with open( outPath, 'wb' ) as f:
        pickle.dump( dataDct, f )
    print( "COMPLETE!" )


