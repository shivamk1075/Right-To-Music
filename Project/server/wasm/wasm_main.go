//go:build js && wasm
// +build js,wasm

package main

import (
	"song-recognition/shazam"
	"song-recognition/utils"
	"syscall/js"
)

func generateFingerprint(this js.Value, args []js.Value) interface{} {
	if len(args) < 2 {
		return js.ValueOf(map[string]interface{}{
			"error": 1,
			"data":  "Expected audio array and sample rate",
		})
	}

	if args[0].Type() != js.TypeObject || args[1].Type() != js.TypeNumber {
		return js.ValueOf(map[string]interface{}{
			"error": 2,
			"data":  "Invalid argument types; Expected audio array and samplerate (type: int)",
		})
	}

	inputArray := args[0]
	sampleRate := args[1].Int()

	audioData := make([]float64, inputArray.Length())
	for i := 0; i < inputArray.Length(); i++ {
		audioData[i] = inputArray.Index(i).Float()
	}

	spectrogram, err := shazam.Spectrogram(audioData, sampleRate)
	if err != nil {
		return js.ValueOf(map[string]interface{}{
			"error": 3,
			"data":  "Error generating spectrogram: " + err.Error(),
		})
	}

	peaks := shazam.ExtractPeaks(spectrogram, float64(len(audioData)/sampleRate))
	fingerprint := shazam.Fingerprint(peaks, utils.GenerateUniqueID())

	fingerprintArray := []interface{}{}
	for address, couple := range fingerprint {
		entry := map[string]interface{}{
			"address":    address,
			"anchorTime": couple.AnchorTimeMs,
		}
		fingerprintArray = append(fingerprintArray, entry)
	}

	return js.ValueOf(map[string]interface{}{
		"error": 0,
		"data":  fingerprintArray,
	})
}

func main() {
	js.Global().Set("generateFingerprint", js.FuncOf(generateFingerprint))
	select {}
}


// # import json
// # import random
// # import numpy as np

// # # Assuming the relevant functions from `shazam` and `utils` have been imported:
// # import shazam.shazam as shazam
// # import shazam.spectrogram as spectrogram1
// # import shazam.fingerprint as fingerprint1
// # import utils.utils as utils

// # def generate_fingerprint(audio_array, sample_rate):
// #     if len(audio_array) < 2:
// #         return json.dumps({
// #             "error": 1,
// #             "data": "Expected audio array and sample rate",
// #         })

// #     if not isinstance(audio_array, list) or not isinstance(sample_rate, int):
// #         return json.dumps({
// #             "error": 2,
// #             "data": "Invalid argument types; Expected audio array and samplerate (type: int)",
// #         })

// #     # Convert audio array from JS equivalent to Python list of floats
// #     audio_data = [float(i) for i in audio_array]

// #     try:
// #         spectrogram = spectrogram1.Spectrogram(audio_data, sample_rate)
// #     except Exception as e:
// #         return json.dumps({
// #             "error": 3,
// #             "data": f"Error generating spectrogram: {str(e)}",
// #         })

// #     peaks = spectrogram1.ExtractPeaks(spectrogram, float(len(audio_data) / sample_rate))
// #     fingerprint = fingerprint1.Fingerprint(peaks, utils.generate_unique_id())

// #     fingerprint_array = []
// #     for address, couple in fingerprint.items():
// #         entry = {
// #             "address": address,
// #             "anchorTime": couple.anchor_time_ms,
// #         }
// #         fingerprint_array.append(entry)

// #     return json.dumps({
// #         "error": 0,
// #         "data": fingerprint_array,
// #     })

// # # Simulating the JavaScript interaction - the following would typically be an event loop for JS calls
// # def main():
// #     # Example for testing the function
// #     audio_array = [random.random() for _ in range(1024)]  # Example audio data
// #     sample_rate = 44100  # Example sample rate

// #     result = generate_fingerprint(audio_array, sample_rate)
// #     print(result)

// # if __name__ == "__main__":
// #     main()
