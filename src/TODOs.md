Objective: remove flashbangs

Todos:
 - [x] implement fade-in renderer
    - [x] return color instead of bool with set_led in BrightnessControlledAndOptionalFadeInRenderer
    - [x] fix push_leds; start a procces, let push_leds go through with the first frame and complete the fade-in; let all other draw calls wait until fade-in is finished
    - [x] clamp color in BrightnessControlledAndOptionalFadeInRenderer
    - [x] add global brightness
    - [ ] move config to actual config
    - [ ] set up brightness-and-fade-in-config in config menu
    - [x] merge RendererBase with BrightnessControlledAndOptionalFadeInRenderer
 - [x] add fade-in to game-over-scene

