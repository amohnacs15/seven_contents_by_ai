import sys
sys.path.append("../src")

import azure.cognitiveservices.speech as speechsdk
import appsecrets as appsecrets
import storage.firebase_storage as firebase
import audioread

def text_to_speech( text ):
    subtext_title = text[0:32]
    child_remote_path = subtext_title + '.mp3'
    full_remote_path = 'ai_content_machine/' + child_remote_path

    full_local_path = 'src/output_downloads/'+child_remote_path
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(
        subscription = appsecrets.AZURE_SUBSCRIPTION_KEY, 
        region = appsecrets.AZURE_REGION
    )

    # The language of the voice that speaks.
    speech_config.speech_synthesis_voice_name='en-US-JennyNeural'
    audio_config = speechsdk.audio.AudioOutputConfig(filename = full_local_path)
    synthesized_speech = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    speech_synthesis_result = synthesized_speech.speak_text_async(text).get()
    
    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized!")
        firebase.upload_mp3(
            remote_storage_path = full_remote_path,
            local_path = full_local_path
        )
        audio = audioread.audio_open(full_local_path)
        return { 
            "speech_duration": audio.duration,
            "speech_remote_path": full_remote_path
        }
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")
    
    return {
        "speech_duration": '',
        "speech_remote_path": ''
    }    
