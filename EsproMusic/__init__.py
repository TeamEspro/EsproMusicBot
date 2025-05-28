from EsproMusic.core.bot import Ritik
from EsproMusic.core.dir import dirr
from EsproMusic.core.git import git
from EsproMusic.core.userbot import Userbot
from EsproMusic.misc import dbb, heroku

from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = Ritik()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
