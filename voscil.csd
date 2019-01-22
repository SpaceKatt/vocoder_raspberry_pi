
<CsoundSynthesizer>
<CsOptions>

-iadc:hw:2,0 -odac:hw:1,0 -+rtmidi=portmidi -+rtaudio=alsa -B2048 -b2048 -M0
;-odac:hw:2,0 -+rtmidi=virtual -+rtaudio=alsa -B2048 -b2048 -Ma

</CsOptions>
<CsInstruments>

sr     = 44032
kr     = 256
nchnls = 1
0dbfs  = 1

gisaw   ftgen   1, 0, 2048, 10, 1, 0.5, 0.3, 0.25, 0.2  ;sawtooth-like
gisine ftgen 0, 0, 4096, 10, 1

instr 1

asig  in                ;get the signal in

; pitch bender
kpb     pchbend 0, 1600
;
        iamp = .2
        ; midi in
        icps cpsmidi

asyn poscil 2, icps + kpb, gisaw      ;excitation signal of 150 Hz
;asyn poscil .6, 150, gisaw      ;excitation signal of 150 Hz


maxalloc 1, 12


;Output  Opcode Arguments    (optional comment)

        ;instr    1

;kbend   linseg 1, 6, .75
;kbend   port kbend, 0.001
;


; Original
;famp pvsanal asig, 1024, 256, 1024, 1   ;analyse in signal
;fexc pvsanal asyn, 1024, 256, 1024, 1   ;analyse excitation signal

famp pvsanal asyn, 1024, 256, 1024, 1   ;analyse in signal
fexc pvsanal asig, 1024, 256, 1024, 1   ;analyse excitation signal

ftps pvsvoc  famp, fexc, 1, 1       ;cross it

atps pvsynth ftps           ;synthesise it                      
;     fout  "test_render.wav", 18, atps
     outs atps
     endin

;output Opcode   amp     freq    fnc         ;comment
;a1      oscil    .2,     icps + kpb,   gisine      ;OSC
;        outs     a1,a1
;        endin



;; Simple mic
;aRM     =   asig
;        outs  aRM
;        endin


</CsInstruments>
<CsScore>

f 0 180; 16 10 1
;i 1 0 10
;e

</CsScore>
</CsoundSynthesizer>

