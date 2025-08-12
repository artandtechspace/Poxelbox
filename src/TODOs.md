Objective: remove flashbangs

Todos:
 - [ ] implement fade-in renderer
    - [ ] return color instead of bool with set_led in BrightnessControlledAndOptionalFadeInRenderer
    - [ ] fix push_leds; start a procces, let push_leds go through with the first frame and complete the fade-in; let all other draw calls wait until fade-in is finished
    - [ ] clamp color in BrightnessControlledAndOptionalFadeInRenderer
    - [ ] add global brightness
    - [ ] move config to actual config
    - [ ] set up BrightnessControlledAndOptionalFadeInRenderer-config in config menu
    - [ ] merge RendererBase with BrightnessControlledAndOptionalFadeInRenderer
 - [ ] add fade-in to game-over-scene
 - [ ] global brightness setting in renderer
 - [ ] global brightness of renderer using config
