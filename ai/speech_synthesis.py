import os
import azure.cognitiveservices.speech as speechsdk
import appsecrets
import storage.firebase_storage as firebase

# # move these to the Firebase file for more encapsulation
# firebase_remote_path = "ai_content_machine/speech_to_text.mp3" #this needs to be updated to be more dynamic and aligned with long-term success
# mp3_local_path = "output_downloads/speech_to_text.mp3"

def text_to_speech( text ):
    subtext_title = text[0:16]
    child_remote_path = subtext_title + '.mp3'
    full_remote_path = 'ai_content_machine/' + child_remote_path

    full_local_path = 'output_downloads/'+child_remote_path
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(
        subscription = appsecrets.AZURE_SUBSCRIPTION_KEY, 
        region = appsecrets.AZURE_REGION
    )

    # The language of the voice that speaks.
    speech_config.speech_synthesis_voice_name='en-US-JennyNeural'
    audio_config = speechsdk.audio.AudioOutputConfig(filename = full_local_path)
    synthesized_speech = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    # Get text from the console and synthesize to the default speaker.
    # print("Enter some text that you want to speak >")
    # text = input()

    speech_synthesis_result = synthesized_speech.speak_text_async(text).get()
    
    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized!")
        # firebase

    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")

    return full_remote_path            