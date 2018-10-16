
<CsoundSynthesizer>
<CsOptions>

-iadc:sysdefault:CARD=Device -odac:hw:2,0 -+rtmidi=portmidi -+rtaudio=alsa -B2048 -b2048 -M0
;-odac:hw:2,0 -+rtmidi=virtual -+rtaudio=alsa -B2048 -b2048 -Ma

</CsOptions>
<CsInstruments>

sr     = 44032
kr     = 256
nchnls = 1
0dbfs  = 1


;gisaw   ftgen   1, 0, 2048, 10, 1, 0.5, 0.3, 0.25, 0.2  ;sawtooth-like

instr 1

asig  in                ;get the signal in
;asyn poscil .6, 150, gisaw      ;excitation signal of 150 Hz

;gisine ftgen 0, 0, 4096, 10, 1

maxalloc 1, 12


;massign 0,     1
;Output  Opcode Arguments    (optional comment)

        ;instr    1

;kbend   linseg 1, 6, .75
;kbend   port kbend, 0.001
;
;kpb     pchbend 0, 1600
;
;        iamp = .2
;        icps cpsmidi
;output Opcode   amp     freq    fnc         ;comment
;a1      oscil    .2,     icps + kpb,   gisine      ;OSC
;        outs     a1,a1
;        endin
aRM     =   asig
        outs  aRM
        endin


</CsInstruments>
<CsScore>

;f 0 180; 16 10 1
i 1 0 10
e

</CsScore>
</CsoundSynthesizer>

