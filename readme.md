## script.module.tts ##

A text to speech wrapper using the TTS engine from Voice RSS

## Requirements ##

You need a valid API key from Voice RSS. The price depends on the number of requests to the TTS Engine and varies from 
free use (max. 350 requests/day) up to commercial use. A pricing list can be found at https://www.voicerss.org/pricing

After receiving the API key, this must be entered in the setup of the module and the TTS Engine is ready for use. To check 
the functionality simply click the addon icon. The other settings in the setup of the module are self-explanatory.

## Usage ##

Add this module as a dependency in the addon.xml to the addon that should use the TTS engine

    <requires>
	    <import addon="xbmc.python" version="3.0.0" />
        <import optional="true" addon="script.module.tts" version="1.0.1" />
    </requires>

## Usage in your script ##

    from tts_wrapper import TTS
    text_to_speech = TTS()
    ...

    # assign text to the engine
    text_to_speech.text = 'Say hello to the world'

    # and let the engine speak
    text_to_speech.say()

or:

    text_to_speech.say('Hello world, today is a good day')
    

Audio is output through Kodi's internal player unless it outputs other sound from a video or audio source. Otherwise 
the output is done via the SFX player. 