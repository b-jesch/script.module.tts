import sys
import os
import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs
import json
from voicerss_tts import *

ADDON = xbmcaddon.Addon(id='script.module.tts')
ADDON_NAME = ADDON.getAddonInfo('name')
PROFILE = os.path.join(xbmcvfs.translatePath(ADDON.getAddonInfo('profile')), 'temp')
LOC = ADDON.getLocalizedString

if not xbmcvfs.exists(PROFILE): xbmcvfs.mkdirs(PROFILE)

countries = dict({30050: 'ar-eg', 30051: 'ar-sa', 30052: 'bg-bg', 30053: 'ca-es', 30054: 'zh-cn', 30055: 'zh-hk',
                  30056: 'zh-tw', 30057: 'hr-hr', 30058: 'cs-cz', 30059: 'da-dk', 30060: 'nl-be', 30061: 'nl-nl',
                  30062: 'en-au', 30063: 'en-ca', 30064: 'en-gb', 30065: 'en-in', 30066: 'en-ie', 30067: 'en-us',
                  30068: 'fi-fi', 30069: 'fr-ca', 30070: 'fr-fr', 30071: 'fr-ch', 30072: 'de-at', 30073: 'de-de',
                  30074: 'de-ch', 30075: 'el-gr', 30076: 'he-il', 30077: 'hi-in', 30078: 'hu-hu', 30079: 'id-id',
                  30080: 'it-it', 30081: 'ja-jp', 30082: 'ko-kr', 30083: 'ms-my', 30084: 'nb-no', 30085: 'pl-pl',
                  30086: 'pt-br', 30087: 'pt-pt', 30088: 'ro-ro', 30089: 'ru-ru', 30090: 'sk-sk', 30091: 'sl-si',
                  30092: 'es-mx', 30093: 'es-es', 30094: 'sv-se', 30095: 'ta-in', 30096: 'th-th', 30097: 'tr-tr',
                  30098: 'vi-vn'})


def jsonrpc(query):
    rpc = {"jsonrpc": "2.0", "id": 1}
    rpc.update(query)
    try:
        response = json.loads(xbmc.executeJSONRPC(json.dumps(rpc)))
        if 'result' in response:
            return response['result']
    except TypeError as e:
        xbmc.log('[%s]: Error executing JSON RPC: %s' % (ADDON_NAME, str(e)), xbmc.LOGERROR)
    return False


class TTS(object):
    def __init__(self):
        self.api_key = ADDON.getSetting('api_key')
        self.ssl = True if ADDON.getSetting('ssl').lower() == 'true' else False
        self.language = countries[int(ADDON.getSetting('language'))]
        self.voice = LOC(int(ADDON.getSetting(ADDON.getSetting('language')))).split()[0]
        self.speed = ADDON.getSetting('speed')

        xbmc.log('[%s]: using voice %s from %s (%s, speed: %s)' % (ADDON_NAME, self.voice,
                                                                   LOC(int(ADDON.getSetting('language'))),
                                                                   self.language, self.speed), xbmc.LOGINFO)
        self.text = ''
        self.codec = 'WAV'
        self.format = '22khz_16bit_mono'

    def say(self, text=None):

        if text is not None: self.text = text
        params = dict({'key': self.api_key, 'src': self.text, 'hl': self.language, 'ssl': self.ssl, 'v': self.voice,
                       'r': self.speed, 'c': self.codec, 'f': self.format})
        try:
            result = speech(params)
            if result.get('error', False): raise RuntimeError(result['error'])
        except RuntimeError as e:
            xbmc.log('[%s]: %s' % (ADDON_NAME, str(e)), xbmc.LOGERROR)
            return False

        with open(os.path.join(PROFILE, 'speech.%s' % self.codec.lower()), 'wb') as bs_out:
            bs_out.write(result['response'])

        # determine active players
        query = dict({'method': 'Player.GetActivePlayers', 'params': {}})
        res = jsonrpc(query)
        if res:
            xbmc.playSFX(os.path.join(PROFILE, 'speech.%s' % self.codec.lower()), useCached=False)
        else:
            xbmc.Player().play(os.path.join(PROFILE, 'speech.%s' % self.codec.lower()))
        return True


if __name__ == '__main__':

    TextToSpeech = TTS()
    TextToSpeech.text = LOC(30020)
    try:
        if sys.argv[1].split('=')[0] == 'text': TextToSpeech.text = sys.argv[1].split('=')[1]
        elif sys.argv[1] == 'test':
            text = xbmcgui.Dialog().input(LOC(30016), type=xbmcgui.INPUT_ALPHANUM)
            if text != '': TextToSpeech.text = text
    except IndexError:
        pass
    if not TextToSpeech.say(): xbmcgui.Dialog().notification(ADDON_NAME, LOC(30015), icon=xbmcgui.NOTIFICATION_ERROR)
